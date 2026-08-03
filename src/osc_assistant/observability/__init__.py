"""Observability: tracing, persistence, and the rendering of traces.

Three modules with one dependency direction. `trace` collects and knows nothing
else; `store` persists and imports `trace` for its types; `render` presents and
imports `trace` for its types. Nothing imports `render` or `store` from `trace`,
which is why this package `__init__` is the only place that composes them —
`configure_observability` is that composition.

The public surface is deliberately small. Instrumented code needs `span`, `trace`
and `annotate`; tooling needs `RECORDER`, `active_trace_store` and the renderers;
startup needs `configure_observability`.
"""

from __future__ import annotations

from pathlib import Path

from .render import render_summary, render_waterfall
from .store import DEFAULT_TRACE_DIR, TraceStore, trace_from_dict
from .trace import (
    RECORDER,
    Span,
    Trace,
    annotate,
    annotate_text,
    configure_tracing,
    current_trace_id,
    set_trace_sink,
    span,
    trace,
)

_store: TraceStore | None = None


def configure_observability(
    *,
    enabled: bool = True,
    capacity: int = 50,
    log_traces: bool = True,
    capture_text: bool = True,
    max_spans: int = 500,
    persist: bool = True,
    trace_dir: Path | str = DEFAULT_TRACE_DIR,
    max_trace_bytes: int = 5_000_000,
) -> None:
    """Install the whole observability stack. Safe to call more than once.

    Persistence is on by default and applies to every process, not only the CLI.
    A server keeps its ring buffer as well — that is what serves `/api/traces`
    without touching disk on a read — but writing traces down means the CLI and the
    service share one history, so `./osc traces` shows what the local server did as
    readily as what the last `./osc ask` did.
    """
    global _store
    configure_tracing(
        enabled=enabled,
        capacity=capacity,
        log_traces=log_traces,
        capture_text=capture_text,
        max_spans=max_spans,
    )
    if enabled and persist:
        _store = TraceStore(Path(trace_dir), max_bytes=max_trace_bytes)
        set_trace_sink(_store.append)
    else:
        _store = None
        set_trace_sink(None)


def active_trace_store() -> TraceStore | None:
    """The store traces are being written to, if persistence is enabled."""
    return _store


__all__ = [
    "RECORDER",
    "Span",
    "Trace",
    "TraceStore",
    "active_trace_store",
    "annotate",
    "annotate_text",
    "configure_observability",
    "configure_tracing",
    "current_trace_id",
    "render_summary",
    "render_waterfall",
    "set_trace_sink",
    "span",
    "trace",
    "trace_from_dict",
]
