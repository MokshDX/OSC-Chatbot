# Span Tree & Trace Core

> 22 nodes · cohesion 0.13

## Key Concepts

- **Trace** (30 connections) — `src/osc_assistant/observability/trace.py`
- **Span** (19 connections) — `src/osc_assistant/observability/trace.py`
- **_reset()** (7 connections) — `src/osc_assistant/observability/trace.py`
- **Any** (6 connections)
- **_log_trace()** (5 connections) — `src/osc_assistant/observability/trace.py`
- **.slowest()** (4 connections) — `src/osc_assistant/observability/trace.py`
- **.set()** (3 connections) — `src/osc_assistant/observability/trace.py`
- **.to_dict()** (3 connections) — `src/osc_assistant/observability/trace.py`
- **.to_dict()** (2 connections) — `src/osc_assistant/observability/trace.py`
- **.root()** (2 connections) — `src/osc_assistant/observability/trace.py`
- **ContextVar** (1 connections)
- **T** (1 connections)
- **One stage of processing, timed. `offset_ms` is measured from the start of the…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Attach structured facts about what this stage did. Values should be small and…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Everything one operation did, as a flat list of spans in start order. Flat…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **The leaf span that consumed the most wall time. Leaves only: a parent's…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Begin a root trace for one operation (a request, a CLI command, a sync).…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Time one stage inside the active trace. Outside a trace this yields a detached…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Restore `variable`, tolerating a close in a foreign context. The streaming…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Emit the whole trace as one structured record. One line per operation rather…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **.failed()** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Token** (1 connections)

## Relationships

- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (8 shared connections)
- [Observability Entry & Trace Rendering](Observability_Entry_%26_Trace_Rendering.md) (8 shared connections)
- [Persistent Trace Store](Persistent_Trace_Store.md) (6 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (3 shared connections)
- [Trace Sink & JSONL Parsing](Trace_Sink_%26_JSONL_Parsing.md) (3 shared connections)
- [Trace Listing CLI](Trace_Listing_CLI.md) (2 shared connections)
- [Trace Ring Buffer](Trace_Ring_Buffer.md) (2 shared connections)
- [Observability Installation & Isolation](Observability_Installation_%26_Isolation.md) (1 shared connections)
- [Trace Configuration & CLI Trace](Trace_Configuration_%26_CLI_Trace.md) (1 shared connections)
- [Trace Store Tests](Trace_Store_Tests.md) (1 shared connections)

## Source Files

- `src/osc_assistant/observability/trace.py`

## Audit Trail

- EXTRACTED: 89 (96%)
- INFERRED: 4 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*