# Trace Store Tests

> 25 nodes · cohesion 0.18

## Key Concepts

- **test_trace_store.py** (21 connections) — `tests/test_trace_store.py`
- **Path** (14 connections)
- **_store()** (13 connections) — `tests/test_trace_store.py`
- **_trace()** (11 connections) — `tests/test_trace_store.py`
- **test_disabling_tracing_disables_persistence()** (6 connections) — `tests/test_trace_store.py`
- **test_a_malformed_line_does_not_hide_the_good_ones()** (5 connections) — `tests/test_trace_store.py`
- **test_a_trace_written_by_one_process_is_readable_by_another()** (5 connections) — `tests/test_trace_store.py`
- **test_an_unwritable_directory_does_not_raise()** (5 connections) — `tests/test_trace_store.py`
- **test_rotation_keeps_the_previous_file_readable()** (5 connections) — `tests/test_trace_store.py`
- **test_the_file_rotates_rather_than_growing()** (5 connections) — `tests/test_trace_store.py`
- **_isolated_tracing()** (4 connections) — `tests/test_trace_store.py`
- **test_a_trace_is_retrievable_by_id_and_by_unique_prefix()** (4 connections) — `tests/test_trace_store.py`
- **test_clear_removes_both_files()** (4 connections) — `tests/test_trace_store.py`
- **test_recent_respects_its_limit()** (4 connections) — `tests/test_trace_store.py`
- **test_traces_are_returned_newest_first()** (4 connections) — `tests/test_trace_store.py`
- **test_tracing_writes_through_to_the_configured_store()** (4 connections) — `tests/test_trace_store.py`
- **test_reading_an_absent_file_is_empty_rather_than_an_error()** (3 connections) — `tests/test_trace_store.py`
- **fixture** (1 connections)
- **Persisted trace tests. The store exists so a one-shot CLI command's trace…** (1 connections) — `tests/test_trace_store.py`
- **Discarding everything at the moment the limit is hit is reliably the moment…** (1 connections) — `tests/test_trace_store.py`
- **A truncated final line is expected: the writer may have been killed.** (1 connections) — `tests/test_trace_store.py`
- **Instrumentation must never be the reason a request fails.** (1 connections) — `tests/test_trace_store.py`
- **Nothing should be written by a process that is not tracing.** (1 connections) — `tests/test_trace_store.py`
- **The whole point: the CLI exits, and the trace is still there.** (1 connections) — `tests/test_trace_store.py`
- **Bounded by rotation because appending is O(1) and rewriting is not.** (1 connections) — `tests/test_trace_store.py`

## Relationships

- [Trace Sink & JSONL Parsing](Trace_Sink_%26_JSONL_Parsing.md) (6 shared connections)
- [Observability Installation & Isolation](Observability_Installation_%26_Isolation.md) (2 shared connections)
- [Persistent Trace Store](Persistent_Trace_Store.md) (2 shared connections)
- [Trace Configuration & CLI Trace](Trace_Configuration_%26_CLI_Trace.md) (2 shared connections)
- [Observability Entry & Trace Rendering](Observability_Entry_%26_Trace_Rendering.md) (1 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (1 shared connections)
- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (1 shared connections)

## Source Files

- `tests/test_trace_store.py`

## Audit Trail

- EXTRACTED: 121 (97%)
- INFERRED: 4 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*