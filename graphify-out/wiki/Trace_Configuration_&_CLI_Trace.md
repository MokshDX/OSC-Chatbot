# Trace Configuration & CLI Trace

> 29 nodes · cohesion 0.11

## Key Concepts

- **trace()** (33 connections) — `src/osc_assistant/cli/diagnose.py`
- **test_observability.py** (18 connections) — `tests/test_observability.py`
- **configure_tracing()** (11 connections) — `src/osc_assistant/observability/trace.py`
- **test_capture_text_off_records_the_length_only()** (4 connections) — `tests/test_observability.py`
- **test_span_count_is_capped_and_the_overflow_is_reported()** (4 connections) — `tests/test_observability.py`
- **_reset_tracing()** (3 connections) — `tests/test_observability.py`
- **test_a_trace_is_retrievable_by_id_and_by_unique_prefix()** (3 connections) — `tests/test_observability.py`
- **test_a_trace_serialises_to_json_safe_primitives()** (3 connections) — `tests/test_observability.py`
- **test_an_empty_trace_renders_without_raising()** (3 connections) — `tests/test_observability.py`
- **test_attributes_are_attached_to_the_innermost_span()** (3 connections) — `tests/test_observability.py`
- **test_disabled_tracing_records_nothing()** (3 connections) — `tests/test_observability.py`
- **test_nested_spans_record_parent_and_depth()** (3 connections) — `tests/test_observability.py`
- **test_nested_trace_extends_the_outer_one()** (3 connections) — `tests/test_observability.py`
- **test_spans_outside_a_trace_are_inert()** (3 connections) — `tests/test_observability.py`
- **test_the_recorder_is_bounded_and_returns_newest_first()** (3 connections) — `tests/test_observability.py`
- **test_the_slowest_span_ignores_parents()** (3 connections) — `tests/test_observability.py`
- **test_a_trace_records_its_spans_in_start_order()** (2 connections) — `tests/test_observability.py`
- **test_an_exception_is_recorded_and_re_raised()** (2 connections) — `tests/test_observability.py`
- **Expand one execution trace into a stage-by-stage waterfall. With no id this…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Install tracing configuration. Safe to call more than once.** (1 connections) — `src/osc_assistant/observability/trace.py`
- **fixture** (1 connections)
- **Tracing tests. The load-bearing properties are that a trace describes the…** (1 connections) — `tests/test_observability.py`
- **A corpus-wide ingestion must not grow one trace without bound.** (1 connections) — `tests/test_observability.py`
- **Trace ids are pasted by hand out of a log line or a support ticket.** (1 connections) — `tests/test_observability.py`
- **A parent's duration contains its children, so ranking all spans says nothing.** (1 connections) — `tests/test_observability.py`
- *... and 4 more nodes in this community*

## Relationships

- [Diagnostic CLI Commands](Diagnostic_CLI_Commands.md) (7 shared connections)
- [Observability Entry & Trace Rendering](Observability_Entry_%26_Trace_Rendering.md) (6 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (6 shared connections)
- [Trace Sink & JSONL Parsing](Trace_Sink_%26_JSONL_Parsing.md) (3 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)
- [Trace Store Tests](Trace_Store_Tests.md) (2 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (2 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (1 shared connections)
- [Trace Listing CLI](Trace_Listing_CLI.md) (1 shared connections)
- [Observability Installation & Isolation](Observability_Installation_%26_Isolation.md) (1 shared connections)
- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/diagnose.py`
- `src/osc_assistant/observability/trace.py`
- `tests/test_observability.py`

## Audit Trail

- EXTRACTED: 68 (58%)
- INFERRED: 50 (42%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*