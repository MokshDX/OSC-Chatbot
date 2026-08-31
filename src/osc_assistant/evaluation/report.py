"""Renders an evaluation run as the quality report.

Separate from `runner` and `conversational` for the reason `metrics` is separate
from both: producing a number and presenting it are different jobs, and the
presentation is the part that changes when someone asks a new question of the same
data. Nothing here computes a metric. It reads a report's `summary` and per-case
records and arranges them.

## What the layout is for

The report answers four questions in the order a reader actually asks them:

1. **Did it pass?** One line, at the top, in colour. Everything else is detail.
2. **What is strong and what is weak?** The scorecard, grouped by concern, with a
   bar per bounded metric. The bars are the reason this is not just a list of
   numbers: eight scores in a column are eight comparisons the reader has to do in
   their head, and eight bars are one glance. They are drawn only for metrics in
   [0, 1], where the bar length means something; latency and token counts get no
   bar, because a bar with no defined maximum encodes nothing.
3. **Where is it weak?** Category performance, sorted worst first, then the worst
   individual cases with their trace ids — which is the bridge from "the number
   moved" to "here is the request that moved it".
4. **What changed?** The gate's findings, each with the tolerance it was judged
   against and the sentence explaining where that tolerance came from.

The audience is deliberately mixed. A manager reads items 1 and 3 and stops; an
engineer reads 3 and 4 and goes to `./osc trace <id>`. Both are served by the same
output because the ordering, not a separate view, is what separates them.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from rich.console import Console
from rich.table import Table

from .gate import GateReport
from .metrics import numeric_summary, scored_records

# Metric name -> the section it belongs under. Order here is the order on screen.
# Grouping is by the concern a reader has, not by which module computed the number:
# `groundedness` and `citation_precision` are one question ("can I trust the
# citations?") and sit together even though one is set arithmetic over chunk ids and
# the other is set arithmetic over documents.
SECTIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Retrieval", ("recall@", "precision@", "ndcg@", "hit_rate@", "mrr")),
    ("Answer", ("fact_match", "faithfulness")),
    ("Citations", ("citation_coverage", "groundedness", "citation_precision")),
    ("Abstention", ("abstention_accuracy",)),
    (
        "Conversation",
        (
            "follow_up_resolution",
            "follow_up_resolution_no_context",
            "follow_up_lift",
            "context_switch_recovery",
            "context_switch_recovery_no_context",
            "context_pollution",
            "session_isolation",
        ),
    ),
    (
        "System",
        (
            "latency_p50_seconds",
            "latency_p95_seconds",
            "latency_mean_seconds",
            "throughput_per_second",
            "input_tokens_total",
            "output_tokens_total",
        ),
    ),
)

_BAR_WIDTH = 18

# Thresholds for the bar colour. Not a grading scale — they exist so that a column
# of bars separates "fine", "watch" and "broken" without the reader comparing
# numbers. A metric near 1.0 that *should* be near 1.0 and one that is doing well at
# 0.6 both read green here, which is why the category table below is what a
# conclusion should be drawn from.
_GOOD, _FAIR = 0.85, 0.6


def render_report(
    report: Mapping[str, Any],
    *,
    console: Console,
    error_console: Console,
    gate: GateReport | None = None,
    destination: str = "",
) -> None:
    """Print the full quality report for one run."""
    summary = numeric_summary(report.get("summary", {}))
    records = scored_records(report)

    _render_header(report, gate, error_console)
    _render_scorecard(summary, console)
    _render_categories(records, console)
    _render_worst_cases(records, console, error_console)
    _render_errors(report, console)
    if gate is not None:
        _render_gate(gate, console, error_console)
    if destination:
        error_console.print(f"\n[dim]written to {destination}[/dim]")


# --------------------------------------------------------------------- sections


def _render_header(
    report: Mapping[str, Any], gate: GateReport | None, out: Console
) -> None:
    configuration = report.get("configuration", {})
    counts = (
        f"{report.get('case_count', 0)} cases"
        if "turn_count" not in report
        else f"{report.get('case_count', 0)} conversations · "
        f"{report.get('turn_count', 0)} turns"
    )
    failed = report.get("failed_count", report.get("failed_turns", 0))

    if gate is not None:
        verdict = (
            "[bold green]GATE PASSED[/bold green]"
            if gate.passed
            else "[bold red]GATE FAILED[/bold red]"
        )
        out.print(f"\n{verdict}  [dim]vs {gate.baseline_name}[/dim]")

    out.print(
        f"[bold]{report.get('golden_set', 'golden set')}[/bold] · {counts}"
        + (f" · [red]{failed} failed[/red]" if failed else "")
        + f" · {float(report.get('duration_seconds', 0.0)):.1f}s"
    )
    retrieval = configuration.get("retrieval", {})
    chunking = configuration.get("chunking", {})
    out.print(
        f"[dim]llm={configuration.get('llm')} embeddings={configuration.get('embeddings')} "
        f"chunker={chunking.get('strategy')}/{chunking.get('chunk_size')} "
        f"retrieval={retrieval.get('strategy')}/top_k={retrieval.get('top_k')} "
        f"rewrite={retrieval.get('rewrite_queries')} "
        f"reranker={configuration.get('reranker')}[/dim]\n"
    )


def _render_scorecard(summary: Mapping[str, float], console: Console) -> None:
    """Every metric, grouped by concern, with a bar where a bar means something."""
    scorecard = Table(box=None, pad_edge=False, show_header=True, header_style="dim")
    scorecard.add_column("metric", style="bold", min_width=34)
    scorecard.add_column("value", justify="right", min_width=9)
    scorecard.add_column("", min_width=_BAR_WIDTH)

    placed: set[str] = set()
    for section, prefixes in SECTIONS:
        names = [
            name
            for name in summary
            if name not in placed and any(name.startswith(prefix) for prefix in prefixes)
        ]
        if not names:
            continue
        placed.update(names)
        scorecard.add_row(f"[dim]{section}[/dim]", "", "")
        for name in sorted(names):
            value = summary[name]
            scorecard.add_row(f"  {name}", _format(value), _bar(name, value))
    console.print(scorecard)


def _render_categories(records: Sequence[Mapping[str, Any]], console: Console) -> None:
    """Per-tag performance, worst first.

    This is the section that turns a score into an action. A `recall@5` of 0.86
    across the suite is not something anyone can work on; "the `draft-order` tag
    scores 0.55 across nine cases and everything else is above 0.9" is.

    Sorted ascending and capped, because the interesting end of this table is the
    top of it and a reader scanning twenty rows for the minimum is doing the
    report's job.
    """
    by_tag: dict[str, list[Mapping[str, Any]]] = {}
    for record in records:
        for tag in record.get("tags", []):
            by_tag.setdefault(str(tag), []).append(record)
    if not by_tag:
        return

    rows: list[tuple[str, int, float | None, float | None, float | None]] = []
    for tag, group in by_tag.items():
        # Abstention cases name no relevant documents, so their recall is 0 by
        # construction. Averaging them in would rank the abstention categories as
        # the worst-performing part of the system in every report, permanently, and
        # for a reason that has nothing to do with retrieval — the same class of lie
        # as `fact_match` scoring 1.0 on a run that generated no answers. A category
        # with nothing retrievable to score renders as a dash.
        retrievable = [record for record in group if record.get("relevant_documents")]
        rows.append(
            (
                tag,
                len(group),
                _mean(retrievable, "recall") if retrievable else None,
                _mean(retrievable, "hit") if retrievable else None,
                _fact_match(group),
            )
        )
    # Unscorable categories sort last: they are not weak, they are not measured this
    # way, and putting them at the top of a "weakest first" table is the whole
    # problem being avoided.
    rows.sort(key=lambda row: (row[2] is None, row[2] if row[2] is not None else 0.0))

    table = Table(
        title="performance by category (weakest first)",
        title_style="dim",
        title_justify="left",
        box=None,
        pad_edge=False,
        header_style="dim",
    )
    table.add_column("category", min_width=24)
    table.add_column("cases", justify="right")
    table.add_column("recall", justify="right")
    table.add_column("", min_width=_BAR_WIDTH)
    table.add_column("hit", justify="right")
    table.add_column("facts", justify="right")

    console.print()
    for tag, count, recall, hit, facts in rows:
        table.add_row(
            tag,
            str(count),
            "—" if recall is None else f"{recall:.2f}",
            "" if recall is None else _bar("recall", recall),
            "—" if hit is None else f"{hit:.2f}",
            "—" if facts is None else f"{facts:.2f}",
        )
    console.print(table)

    scored = [row for row in rows if row[2] is not None]
    if scored:
        console.print(
            f"[dim]strongest:[/dim] {', '.join(row[0] for row in scored[::-1][:3])}\n"
            f"[dim]weakest:  [/dim] {', '.join(row[0] for row in scored[:3])}"
        )


def _render_worst_cases(
    records: Sequence[Mapping[str, Any]], console: Console, out: Console
) -> None:
    """The individual cases that scored worst, with their trace ids.

    Abstention cases are excluded: they name no relevant documents, so their recall
    is 0 by construction and they would occupy every row of a table meant to show
    retrieval failures.
    """
    scorable = [record for record in records if record.get("relevant_documents")]
    worst = sorted(
        scorable, key=lambda record: (record.get("recall", 0.0), record.get("reciprocal_rank", 0.0))
    )[:8]
    if not worst or worst[0].get("recall", 0.0) >= 1.0:
        return

    table = Table(
        title="weakest cases",
        title_style="dim",
        title_justify="left",
        box=None,
        pad_edge=False,
        header_style="dim",
    )
    table.add_column("case", min_width=30)
    table.add_column("recall", justify="right")
    table.add_column("mrr", justify="right")
    table.add_column("missing facts", min_width=18)
    table.add_column("trace")

    console.print()
    for record in worst:
        identifier = (
            f"{record['case_id']}:{record['ordinal']}"
            if "ordinal" in record
            else str(record.get("id", ""))
        )
        missing = ", ".join(str(fact) for fact in record.get("missing_facts", []))
        table.add_row(
            identifier,
            f"{record.get('recall', 0.0):.2f}",
            f"{record.get('reciprocal_rank', 0.0):.2f}",
            missing[:18] or "—",
            str(record.get("trace_id", ""))[:12],
        )
    console.print(table)
    out.print("[dim]expand one with: ./osc trace <id>[/dim]")


def _render_errors(report: Mapping[str, Any], console: Console) -> None:
    raw = report.get("cases") or report.get("turns") or []
    errored = [record for record in raw if isinstance(record, dict) and record.get("error")]
    if not errored:
        return

    table = Table(
        title="errored cases",
        title_style="dim",
        title_justify="left",
        box=None,
        pad_edge=False,
        header_style="dim",
    )
    table.add_column("case")
    table.add_column("error")
    console.print()
    for record in errored[:10]:
        table.add_row(str(record.get("id") or record.get("case_id", "")), str(record["error"]))
    console.print(table)


def _render_gate(gate: GateReport, console: Console, out: Console) -> None:
    """Regressions and improvements, each with the tolerance that judged it."""
    if gate.configuration_differences:
        out.print("\n[yellow]configuration differs from the baseline:[/yellow]")
        for key, (before, after) in gate.configuration_differences.items():
            out.print(f"  [dim]{key}: {before} → {after}[/dim]")

    moved = gate.regressions + gate.improvements
    if moved:
        table = Table(
            title="changes against the baseline",
            title_style="dim",
            title_justify="left",
            box=None,
            pad_edge=False,
            header_style="dim",
        )
        table.add_column("metric", min_width=30)
        table.add_column("baseline", justify="right")
        table.add_column("current", justify="right")
        table.add_column("delta", justify="right")
        table.add_column("tolerance", justify="right")
        table.add_column("verdict")

        console.print()
        for finding in sorted(moved, key=lambda f: (f.status != "regressed", f.metric)):
            colour = "red" if finding.status == "regressed" else "green"
            label = finding.status + ("" if finding.severity == "blocking" else " (warn)")
            table.add_row(
                finding.metric,
                _format(finding.baseline),
                _format(finding.current),
                f"[{colour}]{finding.delta:+.4g}[/{colour}]",
                f"±{finding.tolerance:.3g}",
                f"[{colour}]{label}[/{colour}]",
            )
        console.print(table)

    for finding in gate.regressions:
        out.print(f"\n[red]{finding.metric}[/red] regressed {finding.delta:+.4g}")
        out.print(f"  [dim]tolerance {finding.tolerance:.4g} — {finding.rationale}[/dim]")
        if finding.affected_cases:
            shown = ", ".join(finding.affected_cases[:6])
            more = (
                f" (+{len(finding.affected_cases) - 6} more)"
                if len(finding.affected_cases) > 6
                else ""
            )
            out.print(f"  [dim]cases:      {shown}{more}[/dim]")
        if finding.affected_categories:
            out.print(f"  [dim]categories: {', '.join(finding.affected_categories)}[/dim]")

    for trade_off in gate.trade_offs:
        out.print(f"\n[red]trade-off:[/red] {trade_off}")
        out.print("  [dim]an improvement bought with a regression is not an improvement[/dim]")

    if gate.passed and not gate.regressions:
        out.print("\n[green]no regression beyond tolerance[/green]")


# ----------------------------------------------------------------------- pieces


def _bar(name: str, value: float) -> str:
    """A proportional bar, but only for metrics that are proportions.

    Latency and token totals have no defined maximum, so a bar for them would encode
    the author's guess at a ceiling rather than the data.
    """
    if not _is_bounded(name) or not 0.0 <= value <= 1.0:
        return ""
    filled = round(value * _BAR_WIDTH)
    colour = "green" if value >= _GOOD else "yellow" if value >= _FAIR else "red"
    return f"[{colour}]{'█' * filled}[/{colour}][dim]{'·' * (_BAR_WIDTH - filled)}[/dim]"


def _is_bounded(name: str) -> bool:
    return not any(
        token in name for token in ("latency", "tokens", "throughput", "scored", "lift")
    )


def _format(value: float) -> str:
    return f"{value:.4g}"




def _mean(records: Sequence[Mapping[str, Any]], key: str) -> float:
    values = [float(record.get(key, 0.0)) for record in records]
    return sum(values) / len(values) if values else 0.0


def _fact_match(records: Sequence[Mapping[str, Any]]) -> float | None:
    """Fact match over the records that actually expect a fact.

    `None` rather than 0.0 when none do — the category table renders it as a dash,
    because a category with no fact expectations scoring zero would read as a
    failure of the model rather than as an absence of the measurement.
    """
    with_facts = [record for record in records if record.get("expected_facts")]
    if not with_facts:
        return None
    return sum(1.0 for record in with_facts if not record.get("missing_facts")) / len(with_facts)
