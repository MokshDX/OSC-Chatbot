# Observability Installation & Isolation

> 9 nodes · cohesion 0.22

## Key Concepts

- **configure_observability()** (12 connections) — `src/osc_assistant/observability/__init__.py`
- **_isolate_observability()** (7 connections) — `tests/conftest.py`
- **set_trace_sink()** (5 connections) — `src/osc_assistant/observability/trace.py`
- **Path** (1 connections)
- **Install the whole observability stack. Safe to call more than once. Persistence…** (1 connections) — `src/osc_assistant/observability/__init__.py`
- **Install a destination for completed traces, or `None` to remove one. A callable…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **MonkeyPatch** (1 connections)
- **Path** (1 connections)
- **Keep persisted traces and logs out of the working directory, and apart. Both…** (1 connections) — `tests/conftest.py`

## Relationships

- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (2 shared connections)
- [Observability Entry & Trace Rendering](Observability_Entry_%26_Trace_Rendering.md) (2 shared connections)
- [Trace Store Tests](Trace_Store_Tests.md) (2 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (2 shared connections)
- [Persistent Trace Store](Persistent_Trace_Store.md) (1 shared connections)
- [Trace Configuration & CLI Trace](Trace_Configuration_%26_CLI_Trace.md) (1 shared connections)
- [Trace Sink & JSONL Parsing](Trace_Sink_%26_JSONL_Parsing.md) (1 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (1 shared connections)
- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (1 shared connections)
- [Logging Subsystem Core](Logging_Subsystem_Core.md) (1 shared connections)

## Source Files

- `src/osc_assistant/observability/__init__.py`
- `src/osc_assistant/observability/trace.py`
- `tests/conftest.py`

## Audit Trail

- EXTRACTED: 30 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*