# Observability Composition & Rendering

> 20 nodes

## Key Concepts

- **observability/__init__.py** (21 connections) — `src/osc_assistant/observability/__init__.py`
- **configure_observability()** (14 connections) — `src/osc_assistant/observability/__init__.py`
- **render_waterfall()** (13 connections) — `src/osc_assistant/observability/render.py`
- **traces()** (10 connections) — `src/osc_assistant/cli/diagnose.py`
- **render.py** (10 connections) — `src/osc_assistant/observability/render.py`
- **render_summary()** (7 connections) — `src/osc_assistant/observability/render.py`
- **_details()** (5 connections) — `src/osc_assistant/observability/render.py`
- **set_trace_sink()** (5 connections) — `src/osc_assistant/observability/trace.py`
- **test_the_waterfall_renders_every_span_and_marks_failures()** (4 connections) — `tests/test_observability.py`
- **_label()** (3 connections) — `src/osc_assistant/observability/render.py`
- **_short()** (2 connections) — `src/osc_assistant/observability/render.py`
- **List recent execution traces, most recent first. Read from the persisted trace…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Path** (1 connections)
- **Observability: tracing, persistence, and the rendering of traces. Three modules…** (1 connections) — `src/osc_assistant/observability/__init__.py`
- **Install the whole observability stack. Safe to call more than once. Persistence…** (1 connections) — `src/osc_assistant/observability/__init__.py`
- **Rendering a trace for a human. Separate from `trace` because collection and…** (1 connections) — `src/osc_assistant/observability/render.py`
- **Draw the trace as an indented waterfall. Bars are positioned by `offset_ms` and…** (1 connections) — `src/osc_assistant/observability/render.py`
- **One line: id, name, duration, span count, outcome.** (1 connections) — `src/osc_assistant/observability/render.py`
- **The first few attributes, plus any error. Truncated on purpose: a waterfall is…** (1 connections) — `src/osc_assistant/observability/render.py`
- **Install a destination for completed traces, or `None` to remove one. A callable…** (1 connections) — `src/osc_assistant/observability/trace.py`

## Relationships

- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (11 shared connections)
- [Trace Fetching & Persistence](Trace_Fetching_%26_Persistence.md) (9 shared connections)
- [Tracing & Retrieval Instrumentation](Tracing_%26_Retrieval_Instrumentation.md) (7 shared connections)
- [Trace Store Tests](Trace_Store_Tests.md) (5 shared connections)
- [Execution Tracing Core](Execution_Tracing_Core.md) (5 shared connections)
- [Span Context Management](Span_Context_Management.md) (4 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (3 shared connections)
- [Trace Store](Trace_Store.md) (2 shared connections)
- [conftest.py](conftest.py.md) (2 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/diagnose.py`
- `src/osc_assistant/observability/__init__.py`
- `src/osc_assistant/observability/render.py`
- `src/osc_assistant/observability/trace.py`
- `tests/test_observability.py`

## Audit Trail

- EXTRACTED: 97 (94%)
- INFERRED: 6 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*