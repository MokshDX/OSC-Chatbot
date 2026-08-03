"""Tracing tests.

The load-bearing properties are that a trace describes the *tree* correctly (a
span's parent and depth), that it survives an exception rather than swallowing it,
and that it is bounded — a tracer that leaks memory or hides failures is worse than
none, because it is trusted.
"""

from __future__ import annotations

import pytest

from osc_assistant.observability import (
    RECORDER,
    Trace,
    annotate,
    configure_tracing,
    current_trace_id,
    render_summary,
    render_waterfall,
    span,
    trace,
)


@pytest.fixture(autouse=True)
def _reset_tracing() -> None:
    configure_tracing(enabled=True, capacity=10, log_traces=False, capture_text=True)
    RECORDER.clear()


def test_a_trace_records_its_spans_in_start_order() -> None:
    with trace("answer"):
        with span("retrieve"):
            pass
        with span("generate"):
            pass

    recorded = RECORDER.recent()[0]
    assert [entry.name for entry in recorded.spans] == ["answer", "retrieve", "generate"]


def test_nested_spans_record_parent_and_depth() -> None:
    """The tree is what distinguishes a trace from a list of timings."""
    with trace("answer"), span("retrieve"), span("search"):
        pass

    root, retrieve, search = RECORDER.recent()[0].spans
    assert root.parent_id is None and root.depth == 0
    assert retrieve.parent_id == root.span_id and retrieve.depth == 1
    assert search.parent_id == retrieve.span_id and search.depth == 2


def test_nested_trace_extends_the_outer_one() -> None:
    """`retrieve` opens a trace of its own, but must not fork one inside `answer`.

    Retrieval is both a whole operation (`osc-assistant search`) and a stage of a
    larger one (`ask`). If the inner call started a second trace, half of every
    answer's timing would be recorded somewhere else.
    """
    with trace("answer"), trace("retrieve"):
        pass

    assert len(RECORDER) == 1
    recorded = RECORDER.recent()[0]
    assert recorded.name == "answer"
    assert [entry.name for entry in recorded.spans] == ["answer", "retrieve"]


def test_an_exception_is_recorded_and_re_raised() -> None:
    with pytest.raises(RuntimeError, match="store down"), trace("answer"), span("search"):
        raise RuntimeError("store down")

    recorded = RECORDER.recent()[0]
    assert recorded.failed
    assert recorded.spans[-1].error == "RuntimeError: store down"


def test_attributes_are_attached_to_the_innermost_span() -> None:
    with trace("answer"), span("search"):
        annotate(hits=12)

    assert RECORDER.recent()[0].spans[-1].attributes["hits"] == 12


def test_spans_outside_a_trace_are_inert() -> None:
    """Instrumented code must be callable from a library context or a test."""
    with span("orphan") as stage:
        stage.set(anything=1)
        stage.set_text("query", "hello")

    assert len(RECORDER) == 0
    assert stage.attributes == {}
    assert current_trace_id() == ""


def test_capture_text_off_records_the_length_only() -> None:
    """A deployment can keep every timing while recording no corpus content."""
    configure_tracing(enabled=True, capacity=10, log_traces=False, capture_text=False)

    with trace("answer") as recorded:
        with span("retrieve") as stage:
            stage.set_text("question", "how much annual leave?")
        assert recorded.trace_id

    attributes = RECORDER.recent()[0].spans[-1].attributes
    assert "question" not in attributes
    assert attributes["question_chars"] == len("how much annual leave?")


def test_disabled_tracing_records_nothing() -> None:
    configure_tracing(enabled=False)

    with trace("answer"), span("retrieve"):
        pass

    assert len(RECORDER) == 0
    configure_tracing(enabled=True, capacity=10, log_traces=False)


def test_span_count_is_capped_and_the_overflow_is_reported() -> None:
    """A corpus-wide ingestion must not grow one trace without bound."""
    configure_tracing(enabled=True, capacity=10, log_traces=False, max_spans=5)

    with trace("ingest"):
        for index in range(20):
            with span(f"document-{index}"):
                pass

    recorded = RECORDER.recent()[0]
    assert len(recorded.spans) == 5
    assert recorded.spans_dropped == 16  # 20 documents, 4 of which still fitted


def test_the_recorder_is_bounded_and_returns_newest_first() -> None:
    configure_tracing(enabled=True, capacity=3, log_traces=False)

    for index in range(5):
        with trace(f"call-{index}"):
            pass

    assert [entry.name for entry in RECORDER.recent()] == ["call-4", "call-3", "call-2"]


def test_a_trace_is_retrievable_by_id_and_by_unique_prefix() -> None:
    """Trace ids are pasted by hand out of a log line or a support ticket."""
    with trace("answer") as recorded:
        trace_id = recorded.trace_id

    assert RECORDER.get(trace_id) is not None
    assert RECORDER.get(trace_id[:6]) is not None
    assert RECORDER.get("nonexistent") is None


def test_the_slowest_span_ignores_parents() -> None:
    """A parent's duration contains its children, so ranking all spans says nothing."""
    with trace("answer"):
        with span("retrieve"), span("search"):
            pass
        with span("generate"):
            for _ in range(50_000):
                pass

    slowest = RECORDER.recent()[0].slowest()
    assert slowest is not None and slowest.name == "generate"


def test_a_trace_serialises_to_json_safe_primitives() -> None:
    import json

    with trace("answer"), span("search"):
        annotate(hits=3, scores=[0.1, 0.2])

    payload = RECORDER.recent()[0].to_dict()
    assert json.loads(json.dumps(payload))["spans"][1]["attributes"]["hits"] == 3


def test_the_waterfall_renders_every_span_and_marks_failures() -> None:
    with pytest.raises(RuntimeError), trace("answer"), span("search"):
        raise RuntimeError("boom")

    recorded = RECORDER.recent()[0]
    output = render_waterfall(recorded)
    assert "answer" in output and "search" in output
    assert "FAILED" in output and "RuntimeError: boom" in output
    assert recorded.trace_id in render_summary(recorded)


def test_an_empty_trace_renders_without_raising() -> None:
    from datetime import UTC, datetime

    empty = Trace(trace_id="x", name="empty", started_at=datetime.now(UTC))
    assert "no spans" in render_waterfall(empty)
