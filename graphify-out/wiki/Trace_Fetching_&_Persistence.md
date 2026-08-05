# Trace Fetching & Persistence

> 25 nodes

## Key Concepts

- **Trace** (30 connections) — `src/osc_assistant/observability/trace.py`
- **trace_from_dict()** (12 connections) — `src/osc_assistant/observability/store.py`
- **store.py** (11 connections) — `src/osc_assistant/observability/store.py`
- **_traces_from()** (7 connections) — `src/osc_assistant/cli/diagnose.py`
- **fail()** (6 connections) — `src/osc_assistant/cli/_shared.py`
- **._read_backwards()** (6 connections) — `src/osc_assistant/observability/store.py`
- **_fetch_traces()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **.get()** (5 connections) — `src/osc_assistant/observability/store.py`
- **_parse_line()** (5 connections) — `src/osc_assistant/observability/store.py`
- **_log_trace()** (5 connections) — `src/osc_assistant/observability/trace.py`
- **.slowest()** (4 connections) — `src/osc_assistant/observability/trace.py`
- **.to_dict()** (3 connections) — `src/osc_assistant/observability/trace.py`
- **test_an_empty_trace_renders_without_raising()** (3 connections) — `tests/test_observability.py`
- **Report an operator-facing error and exit non-zero.** (1 connections) — `src/osc_assistant/cli/_shared.py`
- **Any** (1 connections)
- **Traces that outlive the process that produced them. The in-memory recorder in…** (1 connections) — `src/osc_assistant/observability/store.py`
- **Rebuild a `Trace` from its serialised form. The inverse of `Trace.to_dict`, and…** (1 connections) — `src/osc_assistant/observability/store.py`
- **Look up by full id, or by a unique prefix — ids get pasted by hand.** (1 connections) — `src/osc_assistant/observability/store.py`
- **Yield traces newest first, current file before rotated. Reads whole files…** (1 connections) — `src/osc_assistant/observability/store.py`
- **Parse one record, skipping anything malformed. A truncated final line is…** (1 connections) — `src/osc_assistant/observability/store.py`
- **.failed()** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Everything one operation did, as a flat list of spans in start order. Flat…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **The leaf span that consumed the most wall time. Leaves only: a parent's…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Begin a root trace for one operation (a request, a CLI command, a sync).…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Emit the whole trace as one structured record. One line per operation rather…** (1 connections) — `src/osc_assistant/observability/trace.py`

## Relationships

- [Observability Composition & Rendering](Observability_Composition_%26_Rendering.md) (9 shared connections)
- [Trace Store](Trace_Store.md) (7 shared connections)
- [Span Context Management](Span_Context_Management.md) (7 shared connections)
- [Execution Tracing Core](Execution_Tracing_Core.md) (6 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (4 shared connections)
- [Trace Store Tests](Trace_Store_Tests.md) (4 shared connections)
- [Tracing & Retrieval Instrumentation](Tracing_%26_Retrieval_Instrumentation.md) (3 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (1 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/_shared.py`
- `src/osc_assistant/cli/diagnose.py`
- `src/osc_assistant/observability/store.py`
- `src/osc_assistant/observability/trace.py`
- `tests/test_observability.py`

## Audit Trail

- EXTRACTED: 109 (96%)
- INFERRED: 5 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*