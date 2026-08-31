# AccessLock & BulkImportExport Schemas

> 37 nodes

## Key Concepts

- **trace()** (33 connections) — `src/osc_assistant/cli/diagnose.py`
- **test_observability.py** (18 connections) — `tests/test_observability.py`
- **annotate()** (17 connections) — `src/osc_assistant/observability/trace.py`
- **configure_tracing()** (10 connections) — `src/osc_assistant/observability/trace.py`
- **.ingest()** (9 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **.rewrite()** (6 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **test_capture_text_off_records_the_length_only()** (4 connections) — `tests/test_observability.py`
- **test_span_count_is_capped_and_the_overflow_is_reported()** (4 connections) — `tests/test_observability.py`
- **TraceConfig** (3 connections) — `src/osc_assistant/observability/trace.py`
- **_format_history()** (3 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **_reset_tracing()** (3 connections) — `tests/test_observability.py`
- **test_nested_spans_record_parent_and_depth()** (3 connections) — `tests/test_observability.py`
- **test_nested_trace_extends_the_outer_one()** (3 connections) — `tests/test_observability.py`
- **test_attributes_are_attached_to_the_innermost_span()** (3 connections) — `tests/test_observability.py`
- **test_spans_outside_a_trace_are_inert()** (3 connections) — `tests/test_observability.py`
- **test_disabled_tracing_records_nothing()** (3 connections) — `tests/test_observability.py`
- **test_the_recorder_is_bounded_and_returns_newest_first()** (3 connections) — `tests/test_observability.py`
- **test_a_trace_is_retrievable_by_id_and_by_unique_prefix()** (3 connections) — `tests/test_observability.py`
- **test_the_slowest_span_ignores_parents()** (3 connections) — `tests/test_observability.py`
- **test_a_trace_serialises_to_json_safe_primitives()** (3 connections) — `tests/test_observability.py`
- **test_a_trace_records_its_spans_in_start_order()** (2 connections) — `tests/test_observability.py`
- **test_an_exception_is_recorded_and_re_raised()** (2 connections) — `tests/test_observability.py`
- **Sync `documents` into the store. Args: documents: The full current contents of…** (1 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **Process-wide tracing behaviour, set once from settings at startup. Module-level…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Install tracing configuration. Safe to call more than once.** (1 connections) — `src/osc_assistant/observability/trace.py`
- *... and 12 more nodes in this community*

## Relationships

- [Doctor Health Checks](Doctor_Health_Checks.md) (12 shared connections)
- [Evaluation Runner Tests](Evaluation_Runner_Tests.md) (9 shared connections)
- [Answerer & Abstention Policy](Answerer_%26_Abstention_Policy.md) (7 shared connections)
- [Logging Filters & Audit Stream](Logging_Filters_%26_Audit_Stream.md) (6 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (5 shared connections)
- [PgVector Store](PgVector_Store.md) (2 shared connections)
- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (2 shared connections)
- [StoreInspector Protocol](StoreInspector_Protocol.md) (2 shared connections)
- [FastAPI Routes & Session Endpoints](FastAPI_Routes_%26_Session_Endpoints.md) (1 shared connections)
- [Memory Vector Store](Memory_Vector_Store.md) (1 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (1 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/diagnose.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/observability/trace.py`
- `src/osc_assistant/retrieval/rewrite.py`
- `tests/test_observability.py`

## Audit Trail

- EXTRACTED: 103 (66%)
- INFERRED: 53 (34%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*