# Trace Store Tests

> 30 nodes

## Key Concepts

- **test_trace_store.py** (21 connections) — `tests/test_trace_store.py`
- **Path** (14 connections)
- **_store()** (13 connections) — `tests/test_trace_store.py`
- **active_trace_store()** (11 connections) — `src/osc_assistant/observability/__init__.py`
- **_trace()** (11 connections) — `tests/test_trace_store.py`
- **test_disabling_tracing_disables_persistence()** (6 connections) — `tests/test_trace_store.py`
- **test_a_trace_written_by_one_process_is_readable_by_another()** (5 connections) — `tests/test_trace_store.py`
- **test_the_file_rotates_rather_than_growing()** (5 connections) — `tests/test_trace_store.py`
- **test_rotation_keeps_the_previous_file_readable()** (5 connections) — `tests/test_trace_store.py`
- **test_a_malformed_line_does_not_hide_the_good_ones()** (5 connections) — `tests/test_trace_store.py`
- **test_an_unwritable_directory_does_not_raise()** (5 connections) — `tests/test_trace_store.py`
- **test_an_error_survives_the_round_trip()** (5 connections) — `tests/test_trace_store.py`
- **_isolated_tracing()** (4 connections) — `tests/test_trace_store.py`
- **test_traces_are_returned_newest_first()** (4 connections) — `tests/test_trace_store.py`
- **test_recent_respects_its_limit()** (4 connections) — `tests/test_trace_store.py`
- **test_a_trace_is_retrievable_by_id_and_by_unique_prefix()** (4 connections) — `tests/test_trace_store.py`
- **test_clear_removes_both_files()** (4 connections) — `tests/test_trace_store.py`
- **test_tracing_writes_through_to_the_configured_store()** (4 connections) — `tests/test_trace_store.py`
- **test_persistence_can_be_turned_off()** (4 connections) — `tests/test_trace_store.py`
- **test_reading_an_absent_file_is_empty_rather_than_an_error()** (3 connections) — `tests/test_trace_store.py`
- **The store traces are being written to, if persistence is enabled.** (1 connections) — `src/osc_assistant/observability/__init__.py`
- **fixture** (1 connections)
- **Persisted trace tests. The store exists so a one-shot CLI command's trace…** (1 connections) — `tests/test_trace_store.py`
- **The whole point: the CLI exits, and the trace is still there.** (1 connections) — `tests/test_trace_store.py`
- **Bounded by rotation because appending is O(1) and rewriting is not.** (1 connections) — `tests/test_trace_store.py`
- *... and 5 more nodes in this community*

## Relationships

- [Tracing & Retrieval Instrumentation](Tracing_%26_Retrieval_Instrumentation.md) (6 shared connections)
- [Observability Composition & Rendering](Observability_Composition_%26_Rendering.md) (5 shared connections)
- [Trace Fetching & Persistence](Trace_Fetching_%26_Persistence.md) (4 shared connections)
- [Trace Store](Trace_Store.md) (3 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (1 shared connections)

## Source Files

- `src/osc_assistant/observability/__init__.py`
- `tests/test_trace_store.py`

## Audit Trail

- EXTRACTED: 140 (95%)
- INFERRED: 7 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*