"""The `eval` command: measure the system instead of arguing about it.

Its own module rather than a fourth command in `core` because it is the entry point
to a whole subsystem — it loads golden sets, validates them against the live index,
drives the real pipelines, writes comparable artefacts, renders the quality report
and can fail a build. That is more surface than `ask` and `search` have between them.

**`./osc eval` is the canonical quality command.** With no arguments it runs the
single-turn suite *and* the conversational suite, compares both against their
committed baselines, prints the report and exits non-zero on a regression. Answering
"is OSC any good?" should not require remembering four flags.

    ./osc eval                        the whole quality picture, gated
    ./osc eval --retrieval-only       fast and free: no model calls
    ./osc eval --no-gate              measure without judging
    ./osc eval --suite conversational just the multi-turn suite
    ./osc eval --judge                adds LLM-as-judge faithfulness

`make test` asks whether the system is correct; this asks whether it is good. They
are different questions, and a system can pass every test while answering every
question badly.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any

import typer

from ..container import Container
from ..errors import EvaluationError
from ..evaluation import (
    ConversationalEvaluator,
    ConversationalSet,
    Evaluator,
    FaithfulnessJudge,
    GoldenSet,
    load_conversational_set,
    load_golden_set,
)
from ..evaluation.gate import GateReport, evaluate_gate
from ..evaluation.report import render_report
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
    traced_command,
)

app = typer.Typer()

SUITES_DIR = Path("evaluation/suites")
BASELINES_DIR = Path("evaluation/baselines")
DEFAULT_RESULTS_DIR = Path("evaluation/results")


class Suite(StrEnum):
    """Which suites to run.

    `all` is the default because the canonical command should cover the system, and
    a developer who has to remember to also run the conversational suite is a
    developer who will not.
    """

    ALL = "all"
    SCHEMA = "schema"
    CONVERSATIONAL = "conversational"


@app.command(rich_help_panel=UNDERSTANDING)
def eval(
    profile: ProfileOption = None,
    suite: Annotated[
        Suite, typer.Option("--suite", "-s", help="Which suite to run.")
    ] = Suite.ALL,
    golden_set: Annotated[
        Path | None,
        typer.Option(
            "--golden-set",
            "-g",
            help="Run one specific suite file instead of the standard ones.",
        ),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Write the result JSON here."),
    ] = None,
    baseline: Annotated[
        Path | None,
        typer.Option(
            "--baseline",
            "-b",
            help="Compare against this result JSON instead of the committed baseline.",
        ),
    ] = None,
    gate: Annotated[
        bool,
        typer.Option(
            "--gate/--no-gate",
            help="Exit non-zero on a regression beyond tolerance against the baseline.",
        ),
    ] = True,
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
    """Score the golden sets against the current configuration.

    Writes a result file per suite so runs can be compared, prints the quality
    report, and — unless `--no-gate` — exits non-zero when a metric has regressed
    beyond the tolerance derived for it.
    """
    with traced_command():
        settings = load(profile, verbose=verbose)
        plan = _plan(suite, golden_set, retrieval_only)

        # One `--output` and two suites means the second silently overwrites the
        # first, and the surviving file is labelled with only one suite's name. A
        # refusal is better than a result file that quietly lost half a run.
        if output is not None and len(plan) > 1:
            raise EvaluationError(
                f"--output names one file but {len(plan)} suites are planned "
                f"({', '.join(path.stem for _, path in plan)}), and the second would "
                f"overwrite the first. Either drop --output — each suite writes its "
                f"own timestamped file under {DEFAULT_RESULTS_DIR}/ — or run one "
                f"suite at a time with --suite."
            )

        payloads: dict[str, dict[str, Any]] = {}
        gates: dict[str, GateReport] = {}
        failed = False

        for kind, path in plan:
            report = _run_suite(
                kind=kind,
                path=path,
                settings=settings,
                retrieval_only=retrieval_only,
                use_judge=judge,
                concurrency=concurrency,
                tag=tag,
            )
            destination = output or _default_output(report, path)
            _write(report, destination)
            payloads[path.stem] = report

            suite_gate = None
            if gate:
                reference = baseline or _default_baseline(path, retrieval_only)
                if reference.is_file():
                    suite_gate = evaluate_gate(
                        _read_json(reference), report, baseline_name=reference.name
                    )
                    gates[path.stem] = suite_gate
                    failed = failed or not suite_gate.passed
                else:
                    error_console.print(
                        f"[yellow]no baseline at {reference} — nothing to gate "
                        f"{path.stem} against. Commit this run to create one.[/yellow]"
                    )

            if not as_json:
                render_report(
                    report,
                    console=console,
                    error_console=error_console,
                    gate=suite_gate,
                    destination=str(destination),
                )

        if as_json:
            console.print_json(
                json.dumps(
                    {
                        "suites": payloads,
                        "gates": {name: report.to_dict() for name, report in gates.items()},
                        "passed": not failed,
                    }
                )
            )

        if failed:
            error_console.print("\n[red]evaluation gate failed[/red]")
            raise typer.Exit(code=1)


def _plan(suite: Suite, override: Path | None, retrieval_only: bool) -> list[tuple[str, Path]]:
    """Which suites to run, as (kind, path) pairs.

    An explicit `--golden-set` wins over `--suite`, and its kind is inferred from
    the filename rather than guessed from the contents: a mislabelled file should
    fail loudly at load time, not be silently run as the other kind.
    """
    if override is not None:
        kind = "conversational" if "conversational" in override.stem else "schema"
        return [(kind, override)]

    plan: list[tuple[str, Path]] = []
    if suite in (Suite.ALL, Suite.SCHEMA):
        plan.append(("schema", SUITES_DIR / "schema.yaml"))
    if suite in (Suite.ALL, Suite.CONVERSATIONAL):
        # A conversational run measures whether history reaches retrieval and
        # generation. With generation skipped there is no conversation to have —
        # every turn would be a bare retrieval call — so the suite is dropped
        # rather than run in a form that reports meaningless numbers.
        if retrieval_only:
            error_console.print(
                "[dim]skipping the conversational suite: --retrieval-only has no "
                "turns to take.[/dim]"
            )
        else:
            plan.append(("conversational", SUITES_DIR / "conversational.yaml"))
    return plan


def _run_suite(
    *,
    kind: str,
    path: Path,
    settings: Settings,
    retrieval_only: bool,
    use_judge: bool,
    concurrency: int,
    tag: str | None,
) -> dict[str, Any]:
    if kind == "conversational":
        conversational = load_conversational_set(path)
        if tag is not None:
            conversational = conversational.model_copy(
                update={"cases": _filtered(conversational.cases, tag, path)}
            )
        return run(
            _execute_conversational(
                settings=settings,
                conversational=conversational,
                name=path.name,
                use_judge=use_judge,
                concurrency=concurrency,
            )
        )

    golden = load_golden_set(path)
    if tag is not None:
        golden = golden.model_copy(update={"cases": _filtered(golden.cases, tag, path)})
    return run(
        _execute(
            settings=settings,
            golden=golden,
            golden_set_name=path.name,
            retrieval_only=retrieval_only,
            use_judge=use_judge,
            concurrency=concurrency,
        )
    )


def _filtered[T: Any](cases: list[T], tag: str, path: Path) -> list[T]:
    selected = [case for case in cases if tag in case.tags]
    if not selected:
        raise EvaluationError(
            f"No case in {path} carries the tag {tag!r}. Available tags: "
            f"{', '.join(sorted({t for c in cases for t in c.tags})) or '(none)'}."
        )
    return selected


async def _execute(
    *,
    settings: Settings,
    golden: GoldenSet,
    golden_set_name: str,
    retrieval_only: bool,
    use_judge: bool,
    concurrency: int,
) -> dict[str, Any]:
    """Build the real system, check the golden set against it, and run."""
    async with Container(settings) as container:
        await _assert_resolvable(container, golden.referenced_documents, golden.corpus)

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
        report = await evaluator.run(golden, name=golden_set_name, concurrency=concurrency)
        return report.to_dict()


async def _execute_conversational(
    *,
    settings: Settings,
    conversational: ConversationalSet,
    name: str,
    use_judge: bool,
    concurrency: int,
) -> dict[str, Any]:
    async with Container(settings) as container:
        await _assert_resolvable(
            container, conversational.referenced_documents, conversational.corpus
        )
        evaluator = ConversationalEvaluator(
            conversation=container.conversation,
            retrieval=container.retrieval,
            settings=settings,
            judge=FaithfulnessJudge(container.fast_llm) if use_judge else None,
        )
        report = await evaluator.run(conversational, name=name, concurrency=concurrency)
        return report.to_dict()


async def _assert_resolvable(
    container: Container, referenced: set[str], corpus: str
) -> None:
    """Refuse to run a suite that names documents the index does not hold.

    A mistyped path and a genuine retrieval miss both score zero, and only one of
    them is a bug in the search stack. Catching it here turns thirty minutes of
    "why did recall collapse?" into one line naming the file — and, when the suite
    declares its corpus, into the command that fixes it.
    """
    store = container.vector_store
    if not isinstance(store, StoreInspector):
        return  # A store with no introspection cannot answer; run anyway.

    documents = await store.list_documents(limit=10_000)
    indexed = {str(summary.metadata.get("relative_path", "")) for summary in documents} - {""}
    if not indexed:
        raise EvaluationError(
            "The index is empty, so every case would score zero. "
            + (f"Run `./osc ingest {corpus}` first." if corpus else "Run `make ingest` first.")
        )

    missing = referenced - indexed
    if missing:
        remedy = (
            f"\n\nThis suite is scored against `{corpus}`. Index it with:\n"
            f"  ./osc ingest {corpus}"
            if corpus
            else "\n\nEither the corpus has moved or a path is mistyped."
        )
        raise EvaluationError(
            "The suite names documents that are not in the index:\n  "
            + "\n  ".join(sorted(missing))
            + remedy
            + "\n\n`./osc documents` lists what is indexed."
        )


def _default_output(report: dict[str, Any], suite: Path) -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    slug = str(report["configuration"]["llm"]).replace("/", "-").replace(":", "-")
    return DEFAULT_RESULTS_DIR / f"{stamp}-{suite.stem}-{slug}.json"


def _default_baseline(suite: Path, retrieval_only: bool) -> Path:
    """The committed baseline this suite is judged against.

    Retrieval-only runs report no generation metrics, so they get their own
    baseline. Comparing a retrieval-only run against a full one would silently
    compare the intersection of two different measurements.
    """
    variant = "retrieval" if retrieval_only else "full"
    return BASELINES_DIR / f"{suite.stem}-{variant}.json"


def _write(report: dict[str, Any], destination: Path) -> None:
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise EvaluationError(f"Could not write the result to {destination}: {exc}") from exc


def _read_json(path: Path) -> dict[str, Any]:
    try:
        parsed: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        return parsed
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"Could not read baseline {path}: {exc}") from exc
