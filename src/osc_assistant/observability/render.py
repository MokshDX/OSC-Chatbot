"""Rendering a trace for a human.

Separate from `trace` because collection and presentation change for different
reasons: a new stage adds a span, a nicer terminal changes only this file. It also
keeps the tracer free of any terminal dependency, so it stays usable from a library
or a test.
"""

from __future__ import annotations

from .trace import Span, Trace

_BAR_WIDTH = 28
_INTERESTING_ATTRIBUTES = 4


def render_waterfall(trace: Trace, *, bar_width: int = _BAR_WIDTH) -> str:
    """Draw the trace as an indented waterfall.

    Bars are positioned by `offset_ms` and sized by `duration_ms`, which is what
    makes the difference between "these two stages ran back to back" and "this one
    stage dominated" visible at a glance — the question a flat list of durations
    cannot answer.
    """
    if not trace.spans:
        return f"{trace.name}: no spans recorded"

    total = max(trace.duration_ms, 0.001)
    name_width = max(len(_label(span)) for span in trace.spans) + 2

    header = (
        f"trace {trace.trace_id}  {trace.name}  "
        f"{trace.duration_ms:.0f}ms  {'FAILED' if trace.failed else 'ok'}"
    )
    lines = [header, "─" * (name_width + bar_width + 22)]

    for span in trace.spans:
        start = int(bar_width * span.offset_ms / total)
        # At least one cell, so a sub-millisecond stage is still visible as a step
        # in the sequence rather than vanishing.
        width = max(1, int(bar_width * span.duration_ms / total))
        bar = " " * min(start, bar_width - 1)
        bar += "█" * min(width, bar_width - len(bar))
        marker = "✗" if span.error else " "
        lines.append(
            f"{_label(span):<{name_width}}{bar:<{bar_width}} "
            f"{span.duration_ms:>8.1f}ms {marker}"
        )
        for detail in _details(span):
            lines.append(f"{'':<{name_width}}{detail}")

    return "\n".join(lines)


def render_summary(trace: Trace) -> str:
    """One line: id, name, duration, span count, outcome."""
    status = "FAILED" if trace.failed else "ok"
    return (
        f"{trace.trace_id}  {trace.started_at:%H:%M:%S}  {trace.name:<12} "
        f"{trace.duration_ms:>8.1f}ms  {len(trace.spans):>2} spans  {status}"
    )


def _label(span: Span) -> str:
    return "  " * span.depth + span.name


def _details(span: Span) -> list[str]:
    """The first few attributes, plus any error.

    Truncated on purpose: a waterfall is a map, not a dump. The full attribute set
    is one `--json` away.
    """
    lines = []
    items = list(span.attributes.items())[:_INTERESTING_ATTRIBUTES]
    if items:
        lines.append("  " + "  ".join(f"{key}={_short(value)}" for key, value in items))
    if span.error:
        lines.append(f"  error: {span.error}")
    return lines


def _short(value: object) -> str:
    text = str(value)
    if isinstance(value, float):
        text = f"{value:.4g}"
    return text if len(text) <= 60 else text[:57] + "..."
