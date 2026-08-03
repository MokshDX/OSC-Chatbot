"""Persisted trace tests.

The store exists so a one-shot CLI command's trace outlives the process that made
it. Three properties carry that: a trace written by one process is readable by
another, the file cannot grow without bound, and nothing about writing it can break
the request it is describing.

That last one gets the most attention here. Instrumentation that can fail the
system it observes is worse than no instrumentation, because it is trusted.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from osc_assistant.observability import (
    Trace,
    active_trace_store,
    annotate,
    configure_observability,
    span,
    trace,
    trace_from_dict,
)
from osc_assistant.observability.store import TraceStore


@pytest.fixture(autouse=True)
def _isolated_tracing(tmp_path: Path):
    configure_observability(
        enabled=True, log_traces=False, persist=True, trace_dir=tmp_path / "traces"
    )
    yield
    configure_observability(enabled=True, log_traces=False, persist=False)


def _store(tmp_path: Path, **kwargs) -> TraceStore:
    return TraceStore(tmp_path / "traces", **kwargs)


def _trace(name: str = "answer", trace_id: str = "abc123") -> Trace:
    return Trace(
        trace_id=trace_id,
        name=name,
        started_at=datetime.now(UTC),
        duration_ms=12.5,
    )


def test_a_trace_written_by_one_process_is_readable_by_another(tmp_path: Path) -> None:
    """The whole point: the CLI exits, and the trace is still there."""
    _store(tmp_path).append(_trace())

    reader = _store(tmp_path)
    found = reader.recent()

    assert [entry.trace_id for entry in found] == ["abc123"]
    assert found[0].name == "answer"


def test_traces_are_returned_newest_first(tmp_path: Path) -> None:
    store = _store(tmp_path)
    for index in range(3):
        store.append(_trace(trace_id=f"trace-{index}"))

    assert [entry.trace_id for entry in store.recent()] == ["trace-2", "trace-1", "trace-0"]


def test_recent_respects_its_limit(tmp_path: Path) -> None:
    store = _store(tmp_path)
    for index in range(10):
        store.append(_trace(trace_id=f"trace-{index}"))

    assert len(store.recent(limit=3)) == 3


def test_a_trace_is_retrievable_by_id_and_by_unique_prefix(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.append(_trace(trace_id="0123456789abcdef"))

    assert store.get("0123456789abcdef") is not None
    assert store.get("012345") is not None
    assert store.get("ffffff") is None


def test_the_file_rotates_rather_than_growing(tmp_path: Path) -> None:
    """Bounded by rotation because appending is O(1) and rewriting is not."""
    store = _store(tmp_path, max_bytes=800)
    for index in range(40):
        store.append(_trace(trace_id=f"trace-{index}"))

    assert store.path.is_file()
    assert store.rotated_path.is_file()
    # Two files, each bounded: the ceiling is roughly twice the threshold.
    total = sum(path.stat().st_size for path in (store.path, store.rotated_path))
    assert total < 800 * 3


def test_rotation_keeps_the_previous_file_readable(tmp_path: Path) -> None:
    """Discarding everything at the moment the limit is hit is reliably the moment
    someone is trying to read a trace, which is why two files are kept."""
    store = _store(tmp_path, max_bytes=600)
    for index in range(30):
        store.append(_trace(trace_id=f"trace-{index}"))

    found = {entry.trace_id for entry in store.recent()}
    assert len(found) > 1
    assert "trace-29" in found


def test_a_malformed_line_does_not_hide_the_good_ones(tmp_path: Path) -> None:
    """A truncated final line is expected: the writer may have been killed."""
    store = _store(tmp_path)
    store.append(_trace(trace_id="good-1"))
    with store.path.open("a", encoding="utf-8") as handle:
        handle.write('{"trace_id": "trunc\n')
        handle.write("\n")
    store.append(_trace(trace_id="good-2"))

    assert {entry.trace_id for entry in store.recent()} == {"good-1", "good-2"}


def test_an_unwritable_directory_does_not_raise(tmp_path: Path) -> None:
    """Instrumentation must never be the reason a request fails."""
    blocked = tmp_path / "blocked"
    blocked.write_text("not a directory", encoding="utf-8")

    store = TraceStore(blocked / "traces")
    store.append(_trace())  # must not raise

    assert store.recent() == []


def test_clear_removes_both_files(tmp_path: Path) -> None:
    store = _store(tmp_path, max_bytes=600)
    for index in range(30):
        store.append(_trace(trace_id=f"trace-{index}"))

    store.clear()

    assert store.recent() == []
    assert not store.path.exists() and not store.rotated_path.exists()


def test_reading_an_absent_file_is_empty_rather_than_an_error(tmp_path: Path) -> None:
    assert _store(tmp_path).recent() == []
    assert _store(tmp_path).get("anything") is None


# ------------------------------------------------------------------ round trip


def test_a_trace_survives_serialisation_intact() -> None:
    """One format for the file and the HTTP body, so one parser serves both."""
    with trace("answer", mode="buffered"), span("retrieve"):
        annotate(hits=5, chunk_ids=["a", "b"])

    original = active_trace_store().recent()[0]  # type: ignore[union-attr]
    rebuilt = trace_from_dict(json.loads(json.dumps(original.to_dict())))

    assert rebuilt.trace_id == original.trace_id
    assert rebuilt.name == original.name
    assert [entry.name for entry in rebuilt.spans] == [
        entry.name for entry in original.spans
    ]
    assert rebuilt.spans[1].attributes["hits"] == 5
    assert rebuilt.spans[1].parent_id == rebuilt.spans[0].span_id


def test_an_error_survives_the_round_trip() -> None:
    """Diagnosing a failure after the fact is the main reason to persist at all."""
    with pytest.raises(RuntimeError), trace("answer"), span("search"):
        raise RuntimeError("store down")

    rebuilt = trace_from_dict(active_trace_store().recent()[0].to_dict())  # type: ignore[union-attr]

    assert rebuilt.failed
    assert rebuilt.spans[-1].error == "RuntimeError: store down"


# --------------------------------------------------------------- configuration


def test_tracing_writes_through_to_the_configured_store(tmp_path: Path) -> None:
    with trace("answer"):
        pass

    store = active_trace_store()
    assert store is not None
    assert store.path.parent == tmp_path / "traces"
    assert len(store.recent()) == 1


def test_persistence_can_be_turned_off() -> None:
    configure_observability(enabled=True, log_traces=False, persist=False)

    with trace("answer"):
        pass

    assert active_trace_store() is None


def test_disabling_tracing_disables_persistence(tmp_path: Path) -> None:
    """Nothing should be written by a process that is not tracing."""
    configure_observability(
        enabled=False, persist=True, trace_dir=tmp_path / "off", log_traces=False
    )

    with trace("answer"):
        pass

    assert active_trace_store() is None
    assert not (tmp_path / "off").exists()
