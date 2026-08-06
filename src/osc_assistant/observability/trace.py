"""Execution tracing: how a request actually spent its time.

Structured logs already answered *what* happened. They could not answer *where the
time went*, *what the data looked like between two stages*, or *which stage failed*
— because each log line is independent and carries no relationship to the others.
This module supplies that missing relationship: a trace is a tree of spans, one per
significant stage, each with a duration, attributes describing how the data changed,
and an error if it raised.

    answer
    ├── retrieve
    │   ├── rewrite
    │   ├── embed_query
    │   ├── search
    │   └── rerank
    └── generate

Three design decisions worth knowing:

**Not OpenTelemetry.** OTel is the right answer once traces leave the process and
land in a collector, and this module is deliberately shaped like it (spans, parent
ids, attributes) so that day is a exporter and not a rewrite. Today it would add a
large dependency and an agent to run for a capability — reading a trace in a
terminal — that fits in this file.

**Not LangChain callbacks.** LangChain's callback system only observes LangChain
runs, and most of this pipeline is not one. A tracer that could not see chunking,
pgvector's SQL fusion or the abstention decision would leave exactly the parts we
most need to debug invisible. LangChain-backed components report into *this* tracer
instead, which keeps one trace tree per request regardless of what implements a
stage.

**Instrumentation lives in the pipelines, not the adapters.** Every provider call
is made from a pipeline, so wrapping the call sites covers all 30-odd providers
without a single adapter importing this module. Provider adapters therefore stay
pure translation, and a new provider is traced the day it is written.

Spans are free when nothing is tracing: `span()` outside a trace returns a detached
span that is never recorded, so instrumented code is safe to call from a library
context or a test.
"""

from __future__ import annotations

import time
import uuid
from collections import deque
from collections.abc import Callable, Iterator
from contextlib import contextmanager, suppress
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from ..logging import TRACE, get_logger

log = get_logger(__name__)

MAX_TEXT_ATTRIBUTE_CHARS = 400
"""Text attributes are truncated to keep one trace loggable as a single line."""


@dataclass(slots=True)
class TraceConfig:
    """Process-wide tracing behaviour, set once from settings at startup.

    Module-level configuration mirrors the standard library's `logging`: tracing is
    a cross-cutting concern that every module reaches for, and threading a config
    object through thirty call sites would be worse than one explicit `configure`.
    """

    enabled: bool = True
    capacity: int = 50
    log_traces: bool = True
    log_spans: bool = True
    """Emit one TRACE-level log record as each span completes.

    This is the whole of the logging system's pipeline coverage. Every stage of
    ingestion and question answering is already a span carrying structured
    attributes, so subscribing to span completion gives retrieval, reranking,
    embedding, generation, parsing and chunking their log lines without a single
    new call site in any of those modules — and without a second, drifting set of
    instrumentation to keep in step with the first.

    At TRACE it costs nothing unless someone asks for it: the record is built only
    after the level check passes.
    """
    capture_text: bool = True
    max_spans: int = 500
    """Hard cap per trace, so one long operation cannot grow without bound.

    A corpus-wide ingestion opens several spans per document, and a few thousand
    documents would otherwise produce a trace large enough to matter — held in the
    ring buffer, multiplied by its capacity. Past the cap, spans become detached
    and the count of what was dropped is recorded on the trace, so the totals on
    the root span stay accurate even when the detail stops.
    """


_config = TraceConfig()


def configure_tracing(
    *,
    enabled: bool = True,
    capacity: int = 50,
    log_traces: bool = True,
    log_spans: bool = True,
    capture_text: bool = True,
    max_spans: int = 500,
) -> None:
    """Install tracing configuration. Safe to call more than once."""
    global _config
    _config = TraceConfig(
        enabled=enabled,
        capacity=capacity,
        log_traces=log_traces,
        log_spans=log_spans,
        capture_text=capture_text,
        max_spans=max_spans,
    )
    RECORDER.resize(capacity)


_sink: Callable[[Trace], None] | None = None


def set_trace_sink(sink: Callable[[Trace], None] | None) -> None:
    """Install a destination for completed traces, or `None` to remove one.

    A callable rather than a concrete store so this module stays free of any
    persistence concern: `store` imports `trace` for its types, and a dependency in
    the other direction would be a cycle. Composition happens in the package
    `__init__`, which is the one place that knows about both.
    """
    global _sink
    _sink = sink


# ------------------------------------------------------------------------- spans


@dataclass(slots=True)
class Span:
    """One stage of processing, timed.

    `offset_ms` is measured from the start of the trace rather than from an
    absolute clock, which is what lets a renderer draw a waterfall and show that
    two stages ran back to back rather than concurrently.
    """

    name: str
    span_id: str
    parent_id: str | None
    depth: int
    offset_ms: float
    duration_ms: float = 0.0
    attributes: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    recorded: bool = True

    def set(self, **attributes: Any) -> None:
        """Attach structured facts about what this stage did.

        Values should be small and machine-comparable — counts, ids, model names,
        scores. Use `set_text` for anything that came from a document or a user.
        """
        if self.recorded:
            self.attributes.update(attributes)

    def set_text(self, key: str, value: str) -> None:
        """Attach human text (a query, an answer, a chunk excerpt).

        Kept separate from `set` because text is the only part of a trace that can
        carry corpus content or a user's question. Deployments handling sensitive
        material set `observability.capture_text: false` and keep the shape of every
        trace — stage, duration, counts — while recording only the length of the
        text itself.
        """
        if not self.recorded:
            return
        if _config.capture_text:
            self.attributes[key] = _truncate(value)
        else:
            self.attributes[f"{key}_chars"] = len(value)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "depth": self.depth,
            "offset_ms": round(self.offset_ms, 2),
            "duration_ms": round(self.duration_ms, 2),
            "attributes": self.attributes,
        }
        if self.error is not None:
            payload["error"] = self.error
        return payload


@dataclass(slots=True)
class Trace:
    """Everything one operation did, as a flat list of spans in start order.

    Flat rather than nested: `parent_id` and `depth` already describe the tree, and
    a flat list serialises to JSON without recursion and renders as a waterfall
    without flattening.
    """

    trace_id: str
    name: str
    started_at: datetime
    spans: list[Span] = field(default_factory=list)
    duration_ms: float = 0.0
    spans_dropped: int = 0

    @property
    def failed(self) -> bool:
        return any(span.error is not None for span in self.spans)

    @property
    def root(self) -> Span | None:
        return self.spans[0] if self.spans else None

    def slowest(self) -> Span | None:
        """The leaf span that consumed the most wall time.

        Leaves only: a parent's duration includes its children, so ranking every
        span would always crown the root and say nothing.
        """
        parents = {span.parent_id for span in self.spans}
        leaves = [span for span in self.spans if span.span_id not in parents]
        return max(leaves, key=lambda span: span.duration_ms, default=None)

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "name": self.name,
            "started_at": self.started_at.isoformat(),
            "duration_ms": round(self.duration_ms, 2),
            "failed": self.failed,
            "spans_dropped": self.spans_dropped,
            "spans": [span.to_dict() for span in self.spans],
        }


_current_trace: ContextVar[Trace | None] = ContextVar("osc_current_trace", default=None)
_current_span: ContextVar[Span | None] = ContextVar("osc_current_span", default=None)
_trace_started: ContextVar[float] = ContextVar("osc_trace_started", default=0.0)


class TraceRecorder:
    """A bounded ring of recent traces, for `osc-assistant trace` and `/api/traces`.

    In-process and lossy on restart, which is the correct trade for its purpose:
    answering "what did that request just do?" seconds after it happened, without
    standing up storage. Durable traces belong in a collector, and the exporter
    seam for that is `Trace.to_dict`.
    """

    def __init__(self, capacity: int = 50) -> None:
        self._traces: deque[Trace] = deque(maxlen=capacity)

    def record(self, trace: Trace) -> None:
        self._traces.append(trace)

    def resize(self, capacity: int) -> None:
        self._traces = deque(self._traces, maxlen=capacity)

    def recent(self, limit: int | None = None) -> list[Trace]:
        """Most recent first."""
        traces = list(reversed(self._traces))
        return traces[:limit] if limit is not None else traces

    def get(self, trace_id: str) -> Trace | None:
        """Look up by full id, or by a unique prefix — trace ids are pasted by hand."""
        for trace in reversed(self._traces):
            if trace.trace_id == trace_id:
                return trace
        matches = [trace for trace in self._traces if trace.trace_id.startswith(trace_id)]
        return matches[-1] if len(matches) == 1 else None

    def clear(self) -> None:
        self._traces.clear()

    def __len__(self) -> int:
        return len(self._traces)


RECORDER = TraceRecorder()


@contextmanager
def trace(name: str, **attributes: Any) -> Iterator[Trace]:
    """Begin a root trace for one operation (a request, a CLI command, a sync).

    Nesting is tolerated and does not start a second trace: an `answer` trace
    already contains `retrieve`, so calling the retrieval pipeline directly inside
    it must extend that tree rather than fork a new one.
    """
    existing = _current_trace.get()
    if existing is not None:
        with span(name, **attributes):
            yield existing
        return

    if not _config.enabled:
        yield Trace(trace_id="", name=name, started_at=datetime.now(UTC))
        return

    current = Trace(trace_id=uuid.uuid4().hex[:16], name=name, started_at=datetime.now(UTC))
    trace_token = _current_trace.set(current)
    started_token = _trace_started.set(time.perf_counter())
    try:
        with span(name, **attributes):
            yield current
    finally:
        root = current.root
        current.duration_ms = root.duration_ms if root else 0.0
        _reset(_current_trace, trace_token)
        _reset(_trace_started, started_token)
        RECORDER.record(current)
        if _sink is not None:
            _sink(current)
        if _config.log_traces:
            _log_trace(current)


@contextmanager
def span(name: str, **attributes: Any) -> Iterator[Span]:
    """Time one stage inside the active trace.

    Outside a trace this yields a detached span that records nothing, so pipeline
    code carries no `if tracing_enabled` branches and stays readable.
    """
    current = _current_trace.get()
    if current is None or len(current.spans) >= _config.max_spans:
        if current is not None:
            current.spans_dropped += 1
        yield Span(
            name=name, span_id="", parent_id=None, depth=0, offset_ms=0.0, recorded=False
        )
        return

    parent = _current_span.get()
    entry = Span(
        name=name,
        span_id=uuid.uuid4().hex[:12],
        parent_id=parent.span_id if parent else None,
        depth=parent.depth + 1 if parent else 0,
        offset_ms=(time.perf_counter() - _trace_started.get()) * 1000,
        attributes=dict(attributes),
    )
    current.spans.append(entry)
    token = _current_span.set(entry)
    started = time.perf_counter()
    try:
        yield entry
    except Exception as exc:
        # Recorded, then re-raised: the trace exists to explain failures, and a
        # tracer that swallowed one would be worse than no tracer at all.
        entry.error = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        entry.duration_ms = (time.perf_counter() - started) * 1000
        _log_span(entry, current.trace_id)
        _reset(_current_span, token)


def _reset[T](variable: ContextVar[T], token: Token[T]) -> None:
    """Restore `variable`, tolerating a close in a foreign context.

    The streaming answer path is an async generator. If a client disconnects
    mid-stream the generator is closed by the garbage collector, which may run the
    `finally` in a different context than the one that created the token — and
    `ContextVar.reset` raises for that. An SSE disconnect is routine, so it must not
    produce an exception during cleanup; the abandoned context is discarded anyway.
    """
    # pragma: no cover below - requires an abandoned async generator to reach.
    with suppress(ValueError):
        variable.reset(token)


def current_trace_id() -> str:
    """The active trace id, or `""` when nothing is tracing.

    Returned to clients and printed by the CLI so a user can quote one identifier
    and an engineer can pull up exactly what happened.
    """
    current = _current_trace.get()
    return current.trace_id if current else ""


def annotate(**attributes: Any) -> None:
    """Attach attributes to the innermost active span, if there is one.

    The counterpart to `span(...) as stage; stage.set(...)`, for code that is inside
    a stage it did not open — which is most of it, since `trace()` yields the trace
    rather than its root span.
    """
    active = _current_span.get()
    if active is not None:
        active.set(**attributes)


def annotate_text(key: str, value: str) -> None:
    """Attach human text to the innermost active span, honouring `capture_text`."""
    active = _current_span.get()
    if active is not None:
        active.set_text(key, value)


def _log_span(entry: Span, trace_id: str) -> None:
    """Emit one completed span as a TRACE record.

    Guarded by `isEnabledFor` before anything is built, so a run at the default
    INFO level pays one integer comparison per span and constructs no dictionary.

    Never raises. Instrumentation that can break the thing it observes is a
    liability precisely because it is trusted — and this runs inside a `finally`,
    where an exception would replace whatever the stage was actually failing with.
    """
    if not _config.log_spans:
        return
    try:
        if not log.isEnabledFor(TRACE):
            return
        log.log(
            TRACE,
            "span.complete",
            extra={
                "trace_id": trace_id,
                "span": entry.name,
                "span_id": entry.span_id,
                "parent_id": entry.parent_id,
                "depth": entry.depth,
                "duration_ms": round(entry.duration_ms, 2),
                "offset_ms": round(entry.offset_ms, 2),
                "error": entry.error,
                **entry.attributes,
            },
        )
    except Exception:  # pragma: no cover - logging must never break a traced stage
        pass


def _log_trace(current: Trace) -> None:
    """Emit the whole trace as one structured record.

    One line per operation rather than one per span: a span tree is only meaningful
    whole, and splitting it across records puts the burden of reassembly on whatever
    reads the logs.
    """
    slowest = current.slowest()
    log.info(
        "trace.complete",
        extra={
            "trace_id": current.trace_id,
            "trace_name": current.name,
            "duration_ms": round(current.duration_ms, 2),
            "failed": current.failed,
            "span_count": len(current.spans),
            "slowest_span": slowest.name if slowest else None,
            "spans": [span.to_dict() for span in current.spans],
        },
    )


def _truncate(value: str) -> str:
    if len(value) <= MAX_TEXT_ATTRIBUTE_CHARS:
        return value
    return value[:MAX_TEXT_ATTRIBUTE_CHARS] + f"… (+{len(value) - MAX_TEXT_ATTRIBUTE_CHARS})"
