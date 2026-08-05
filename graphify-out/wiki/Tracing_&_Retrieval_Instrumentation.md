# Tracing & Retrieval Instrumentation

> 32 nodes

## Key Concepts

- **trace()** (33 connections) — `src/osc_assistant/cli/diagnose.py`
- **test_observability.py** (18 connections) — `tests/test_observability.py`
- **annotate()** (17 connections) — `src/osc_assistant/observability/trace.py`
- **configure_tracing()** (11 connections) — `src/osc_assistant/observability/trace.py`
- **.retrieve()** (10 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **test_a_trace_survives_serialisation_intact()** (6 connections) — `tests/test_trace_store.py`
- **test_capture_text_off_records_the_length_only()** (4 connections) — `tests/test_observability.py`
- **test_span_count_is_capped_and_the_overflow_is_reported()** (4 connections) — `tests/test_observability.py`
- **_reset_tracing()** (3 connections) — `tests/test_observability.py`
- **test_nested_spans_record_parent_and_depth()** (3 connections) — `tests/test_observability.py`
- **test_nested_trace_extends_the_outer_one()** (3 connections) — `tests/test_observability.py`
- **test_attributes_are_attached_to_the_innermost_span()** (3 connections) — `tests/test_observability.py`
- **test_disabled_tracing_records_nothing()** (3 connections) — `tests/test_observability.py`
- **test_the_recorder_is_bounded_and_returns_newest_first()** (3 connections) — `tests/test_observability.py`
- **test_a_trace_is_retrievable_by_id_and_by_unique_prefix()** (3 connections) — `tests/test_observability.py`
- **test_the_slowest_span_ignores_parents()** (3 connections) — `tests/test_observability.py`
- **test_a_trace_serialises_to_json_safe_primitives()** (3 connections) — `tests/test_observability.py`
- **test_a_trace_records_its_spans_in_start_order()** (2 connections) — `tests/test_observability.py`
- **test_an_exception_is_recorded_and_re_raised()** (2 connections) — `tests/test_observability.py`
- **Expand one execution trace into a stage-by-stage waterfall. With no id this…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Install tracing configuration. Safe to call more than once.** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Attach attributes to the innermost active span, if there is one. The…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Retrieve the chunks most relevant to `question`.** (1 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **fixture** (1 connections)
- **Tracing tests. The load-bearing properties are that a trace describes the…** (1 connections) — `tests/test_observability.py`
- *... and 7 more nodes in this community*

## Relationships

- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (8 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (8 shared connections)
- [Observability Composition & Rendering](Observability_Composition_%26_Rendering.md) (7 shared connections)
- [Execution Tracing Core](Execution_Tracing_Core.md) (7 shared connections)
- [Trace Store Tests](Trace_Store_Tests.md) (6 shared connections)
- [Trace Fetching & Persistence](Trace_Fetching_%26_Persistence.md) (3 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (3 shared connections)
- [Retrieval Pipeline](Retrieval_Pipeline.md) (2 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (2 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (1 shared connections)
- [Span Context Management](Span_Context_Management.md) (1 shared connections)
- [Outbound LangChain Retriever](Outbound_LangChain_Retriever.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/diagnose.py`
- `src/osc_assistant/observability/trace.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `tests/test_observability.py`
- `tests/test_trace_store.py`

## Audit Trail

- EXTRACTED: 94 (64%)
- INFERRED: 53 (36%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*