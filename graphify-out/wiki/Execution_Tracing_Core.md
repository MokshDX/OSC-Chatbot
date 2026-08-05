# Execution Tracing Core

> 23 nodes

## Key Concepts

- **trace.py** (22 connections) — `src/osc_assistant/observability/trace.py`
- **current_trace_id()** (10 connections) — `src/osc_assistant/observability/trace.py`
- **TraceRecorder** (9 connections) — `src/osc_assistant/observability/trace.py`
- **.get()** (7 connections) — `src/osc_assistant/observability/trace.py`
- **annotate_text()** (7 connections) — `src/osc_assistant/observability/trace.py`
- **.set_text()** (4 connections) — `src/osc_assistant/observability/trace.py`
- **TraceConfig** (3 connections) — `src/osc_assistant/observability/trace.py`
- **test_spans_outside_a_trace_are_inert()** (3 connections) — `tests/test_observability.py`
- **.record()** (2 connections) — `src/osc_assistant/observability/trace.py`
- **.recent()** (2 connections) — `src/osc_assistant/observability/trace.py`
- **_truncate()** (2 connections) — `src/osc_assistant/observability/trace.py`
- **.__init__()** (1 connections) — `src/osc_assistant/observability/trace.py`
- **.resize()** (1 connections) — `src/osc_assistant/observability/trace.py`
- **.clear()** (1 connections) — `src/osc_assistant/observability/trace.py`
- **.__len__()** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Execution tracing: how a request actually spent its time. Structured logs…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Process-wide tracing behaviour, set once from settings at startup. Module-level…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Attach human text (a query, an answer, a chunk excerpt). Kept separate from…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **A bounded ring of recent traces, for `osc-assistant trace` and `/api/traces`.…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Look up by full id, or by a unique prefix — trace ids are pasted by hand.** (1 connections) — `src/osc_assistant/observability/trace.py`
- **The active trace id, or `""` when nothing is tracing. Returned to clients and…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Attach human text to the innermost active span, honouring `capture_text`.** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Instrumented code must be callable from a library context or a test.** (1 connections) — `tests/test_observability.py`

## Relationships

- [Tracing & Retrieval Instrumentation](Tracing_%26_Retrieval_Instrumentation.md) (7 shared connections)
- [Trace Fetching & Persistence](Trace_Fetching_%26_Persistence.md) (6 shared connections)
- [Observability Composition & Rendering](Observability_Composition_%26_Rendering.md) (5 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (4 shared connections)
- [Span Context Management](Span_Context_Management.md) (4 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (3 shared connections)
- [Retrieval Pipeline](Retrieval_Pipeline.md) (3 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (1 shared connections)

## Source Files

- `src/osc_assistant/observability/trace.py`
- `tests/test_observability.py`

## Audit Trail

- EXTRACTED: 81 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*