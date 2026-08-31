# Answerer & Abstention Policy

> 35 nodes

## Key Concepts

- **test_trace_store.py** (21 connections) — `tests/test_trace_store.py`
- **Path** (14 connections)
- **_store()** (13 connections) — `tests/test_trace_store.py`
- **_trace()** (11 connections) — `tests/test_trace_store.py`
- **configure_observability()** (10 connections) — `src/osc_assistant/observability/__init__.py`
- **active_trace_store()** (9 connections) — `src/osc_assistant/observability/__init__.py`
- **test_a_trace_survives_serialisation_intact()** (6 connections) — `tests/test_trace_store.py`
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
- **Path** (1 connections)
- **Install the whole observability stack. Safe to call more than once. Persistence…** (1 connections) — `src/osc_assistant/observability/__init__.py`
- **The store traces are being written to, if persistence is enabled.** (1 connections) — `src/osc_assistant/observability/__init__.py`
- *... and 10 more nodes in this community*

## Relationships

- [Doctor Health Checks](Doctor_Health_Checks.md) (8 shared connections)
- [AccessLock & BulkImportExport Schemas](AccessLock_%26_BulkImportExport_Schemas.md) (7 shared connections)
- [Trace Store File Handling](Trace_Store_File_Handling.md) (4 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (1 shared connections)

## Source Files

- `src/osc_assistant/observability/__init__.py`
- `tests/test_trace_store.py`

## Audit Trail

- EXTRACTED: 155 (95%)
- INFERRED: 9 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*