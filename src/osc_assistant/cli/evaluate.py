"""The `eval` command: measure the system instead of arguing about it.

Its own module rather than a fourth command in `core` because it is the entry point
to a whole subsystem — it loads a golden set, validates it against the live index,
drives the real pipelines, writes a comparable artefact and can fail a build. That
is more surface than `ask` and `search` have between them.

Three usage shapes, in the order a team grows into them:

    ./osc eval                                  measure the default profile
    ./osc eval --profile config/experiments/hosted-anthropic.yaml --output a.json
    ./osc eval --baseline a.json --fail-under recall@5=0.9

The third is the one that matters: it is how "every retrieval change ships with a
measured improvement" stops being a convention and becomes a build step.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

import typer

from ..container import Container
from ..errors import EvaluationError
from ..evaluation import (
    Evaluator,
    FaithfulnessJudge,
    GoldenSet,
    load_golden_set,
    unresolvable_documents,
)
from ..evaluation.runner import EvaluationReport, compare
from ..protocols import StoreInspector
from ..settings import Settings
from ._shared import (
    UNDERSTANDING,
    JsonOption,
    ProfileOption,
    VerboseOption,
    console,
    error_console,
    load,
    run,
    table,
    traced_command,
)

app = typer.Typer()

DEFAULT_GOLDEN_SET = Path("evaluation/golden-set.yaml")
DEFAULT_RESULTS_DIR = Path("evaluation/results")

# Metrics where a *lower* number is the better one. Everything else is a quality
# score in [0, 1] or a count, and improves upwards. Without this table a comparison
# would report a latency regression as green.
LOWER_IS_BETTER = {
    "latency_p50_seconds",
    "latency_p95_seconds",
    "latency_mean_seconds",
    "input_tokens_total",
    "output_tokens_total",
}


@app.command(rich_help_panel=UNDERSTANDING)
def eval(
    profile: ProfileOption = None,
    golden_set: Annotated[
        Path, typer.Option("--golden-set", "-g", help="Golden set YAML to run.")
    ] = DEFAULT_GOLDEN_SET,
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Write the result JSON here. Defaults to a timestamped file.",
        ),
    ] = None,
    baseline: Annotated[
        Path | None,
        typer.Option("--baseline", "-b", help="Compare against a previous result JSON."),
    ] = None,
    fail_under: Annotated[
        list[str] | None,
        typer.Option(
            "--fail-under",
            help="Exit non-zero if a metric is below a threshold, e.g. 'recall@5=0.9'. Repeatable.",
        ),
    ] = None,
    retrieval_only: Annotated[
        bool,
        typer.Option(
            "--retrieval-only",
            help="Skip generation. Fast, free, and enough to compare chunkers or embeddings.",
        ),
    ] = False,
    judge: Annotated[
        bool,
        typer.Option("--judge", help="Score faithfulness with an LLM judge. Doubles model calls."),
    ] = False,
    concurrency: Annotated[
        int, typer.Option("--concurrency", "-c", min=1, help="Cases to run in parallel.")
    ] = 1,
    tag: Annotated[
        str | None, typer.Option("--tag", help="Run only cases carrying this tag.")
    ] = None,
    as_json: JsonOption = False,
    verbose: VerboseOption = False,
) -> None:
    """Score the golden set against the current configuration.

    Writes a result file so runs can be compared, prints a summary table, and — with
    `--fail-under` — exits non-zero on a regression so CI can hold the line.
    """
    with traced_command():
        settings = load(profile, verbose=verbose)
        golden = load_golden_set(golden_set)

        if tag is not None:
            selected = [case for case in golden.cases if tag in case.tags]
            if not selected:
                raise EvaluationError(
                    f"No case in {golden_set} carries the tag {tag!r}. "
                    f"Available tags: "
                    f"{', '.join(sorted({t for c in golden.cases for t in c.tags})) or '(none)'}."
                )
            golden = golden.model_copy(update={"cases": selected})

        report = run(
            _execute(
                settings=settings,
                golden=golden,
                golden_set_name=golden_set.name,
                retrieval_only=retrieval_only,
                use_judge=judge,
                concurrency=concurrency,
            )
        )

        destination = output or _default_output(report)
        _write(report, destination)

        if as_json:
            console.print_json(json.dumps(report.to_dict()))
        else:
            _print_report(report, destination)
            if baseline is not None:
                _print_comparison(baseline, report)

        _enforce_thresholds(report, fail_under or [])


async def _execute(
    *,
    settings: Settings,
    golden: GoldenSet,
    golden_set_name: str,
    retrieval_only: bool,
    use_judge: bool,
    concurrency: int,
) -> EvaluationReport:
    """Build the real system, check the golden set against it, and run."""
    async with Container(settings) as container:
        await _assert_golden_set_is_resolvable(container, golden)

        evaluator = Evaluator(
            retrieval=container.retrieval,
            settings=settings,
            answerer=None if retrieval_only else container.answerer,
            # The judge deliberately uses `fast_llm` rather than `llm`: judging a
            # model's output with the identical model mostly measures self-agreement,
            # and `fast_llm` is the seam an operator can point at a stronger model
            # without changing what is being evaluated.
            judge=FaithfulnessJudge(container.fast_llm) if use_judge else None,
        )
        return await evaluator.run(golden, name=golden_set_name, concurrency=concurrency)


async def _assert_golden_set_is_resolvable(container: Container, golden: GoldenSet) -> None:
    """Refuse to run a golden set that names documents the index does not hold.

    A mistyped path and a genuine retrieval miss both score zero, and only one of
    them is a bug in the search stack. Catching it here turns thirty minutes of
    "why did recall collapse?" into one line naming the file.
    """
    store = container.vector_store
    if not isinstance(store, StoreInspector):
        return  # A store with no introspection cannot answer; run anyway.

    documents = await store.list_documents(limit=10_000)
    indexed = {
        str(summary.metadata.get("relative_path", "")) for summary in documents
    } - {""}
    if not indexed:
        raise EvaluationError(
            "The index is empty, so every case would score zero. "
            "Run `make ingest` first."
        )

    missing = unresolvable_documents(golden, indexed)
    if missing:
        raise EvaluationError(
            "The golden set names documents that are not in the index:\n  "
            + "\n  ".join(sorted(missing))
            + "\n\nEither the corpus has moved or a path is mistyped. "
            "`./osc documents` lists what is indexed."
        )


def _default_output(report: EvaluationReport) -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    slug = report.configuration["llm"].replace("/", "-").replace(":", "-")
    return DEFAULT_RESULTS_DIR / f"{stamp}-{slug}.json"


def _write(report: EvaluationReport, destination: Path) -> None:
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise EvaluationError(f"Could not write the result to {destination}: {exc}") from exc


def _print_report(report: EvaluationReport, destination: Path) -> None:
    configuration = report.configuration
    error_console.print(
        f"[bold]{report.golden_set}[/bold] · {report.case_count} cases"
        + (f" · [red]{report.failed_count} failed[/red]" if report.failed_count else "")
        + f" · {report.duration_seconds:.1f}s"
    )
    error_console.print(
        f"llm={configuration['llm']} embeddings={configuration['embeddings']} "
        f"chunker={configuration['chunking']['strategy']} "
        f"retrieval={configuration['retrieval']['strategy']}/"
        f"top_k={configuration['retrieval']['top_k']} "
        f"reranker={configuration['reranker']}\n"
    )

    scores = table("metric", "value")
    for name, value in report.summary.items():
        scores.add_row(name, f"{value:.4g}")
    console.print(scores)

    worst = sorted(
        (case for case in report.cases if case.scored and case.relevant_documents),
        key=lambda case: (case.recall, case.reciprocal_rank),
    )[:5]
    if worst and worst[0].recall < 1.0:
        # The five weakest cases, with their trace ids. This is the bridge from
        # "the number moved" to "here is the request that made it move".
        console.print()
        failures = table("weakest case", "recall", "mrr", "trace")
        for case in worst:
            failures.add_row(
                case.id, f"{case.recall:.2f}", f"{case.reciprocal_rank:.2f}", case.trace_id[:12]
            )
        console.print(failures)
        error_console.print("\n[dim]expand one with: ./osc trace <id>[/dim]")

    errored = [case for case in report.cases if not case.scored]
    if errored:
        console.print()
        problems = table("errored case", "error")
        for case in errored[:10]:
            problems.add_row(case.id, case.error or "")
        console.print(problems)

    error_console.print(f"\n[dim]written to {destination}[/dim]")


def _print_comparison(baseline_path: Path, report: EvaluationReport) -> None:
    try:
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"Could not read baseline {baseline_path}: {exc}") from exc

    deltas = compare(baseline, report.to_dict())
    if not deltas:
        error_console.print(f"[yellow]no comparable metrics in {baseline_path}[/yellow]")
        return

    console.print()
    comparison = table("metric", "baseline", "current", "delta", title=f"vs {baseline_path.name}")
    for name, before, after in deltas:
        change = after - before
        improved = (change < 0) if name in LOWER_IS_BETTER else (change > 0)
        colour = "green" if improved else ("red" if change else "dim")
        comparison.add_row(
            name, f"{before:.4g}", f"{after:.4g}", f"[{colour}]{change:+.4g}[/{colour}]"
        )
    console.print(comparison)

    differences = {
        key: (baseline.get("configuration", {}).get(key), value)
        for key, value in report.configuration.items()
        if baseline.get("configuration", {}).get(key) != value
    }
    if differences:
        error_console.print("\n[dim]configuration differences:[/dim]")
        for key, (before, after) in differences.items():
            error_console.print(f"  [dim]{key}: {before} → {after}[/dim]")


def _enforce_thresholds(report: EvaluationReport, thresholds: list[str]) -> None:
    """Exit non-zero if any `metric=minimum` is not met.

    Parsed here rather than in the runner because it is a policy about a run, not a
    property of one: the same numbers are a pass in a local experiment and a
    failure in CI, and only the caller knows which it is.
    """
    if not thresholds:
        return

    breaches: list[str] = []
    for threshold in thresholds:
        name, separator, raw = threshold.partition("=")
        if not separator:
            raise EvaluationError(
                f"--fail-under expects 'metric=value', got {threshold!r}. "
                f"Example: --fail-under recall@{report.top_k}=0.9"
            )
        try:
            minimum = float(raw)
        except ValueError as exc:
            raise EvaluationError(f"--fail-under {threshold!r}: {raw!r} is not a number.") from exc

        name = name.strip()
        if name not in report.summary:
            raise EvaluationError(
                f"--fail-under names an unknown metric {name!r}. "
                f"This run reported: {', '.join(sorted(report.summary))}."
            )
        actual = report.summary[name]
        if actual < minimum:
            breaches.append(f"{name} = {actual:.4g}, below the required {minimum:.4g}")

    if breaches:
        error_console.print("\n[red]evaluation gate failed:[/red]")
        for breach in breaches:
            error_console.print(f"  {breach}")
        raise typer.Exit(code=1)
    error_console.print("\n[green]evaluation gate passed[/green]")
