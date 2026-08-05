# Span Context Management

> 13 nodes

## Key Concepts

- **Span** (18 connections) — `src/osc_assistant/observability/trace.py`
- **_reset()** (7 connections) — `src/osc_assistant/observability/trace.py`
- **Any** (6 connections)
- **.set()** (3 connections) — `src/osc_assistant/observability/trace.py`
- **.to_dict()** (2 connections) — `src/osc_assistant/observability/trace.py`
- **.root()** (2 connections) — `src/osc_assistant/observability/trace.py`
- **ContextVar** (1 connections)
- **T** (1 connections)
- **Token** (1 connections)
- **One stage of processing, timed. `offset_ms` is measured from the start of the…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Attach structured facts about what this stage did. Values should be small and…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Time one stage inside the active trace. Outside a trace this yields a detached…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Restore `variable`, tolerating a close in a foreign context. The streaming…** (1 connections) — `src/osc_assistant/observability/trace.py`

## Relationships

- [Trace Fetching & Persistence](Trace_Fetching_%26_Persistence.md) (7 shared connections)
- [Observability Composition & Rendering](Observability_Composition_%26_Rendering.md) (4 shared connections)
- [Execution Tracing Core](Execution_Tracing_Core.md) (4 shared connections)
- [Trace Store](Trace_Store.md) (1 shared connections)
- [Tracing & Retrieval Instrumentation](Tracing_%26_Retrieval_Instrumentation.md) (1 shared connections)

## Source Files

- `src/osc_assistant/observability/trace.py`

## Audit Trail

- EXTRACTED: 44 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*