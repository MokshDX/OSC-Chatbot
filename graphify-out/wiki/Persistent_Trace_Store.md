# Persistent Trace Store

> 16 nodes · cohesion 0.17

## Key Concepts

- **TraceStore** (18 connections) — `src/osc_assistant/observability/store.py`
- **._read_backwards()** (6 connections) — `src/osc_assistant/observability/store.py`
- **.append()** (5 connections) — `src/osc_assistant/observability/store.py`
- **.get()** (5 connections) — `src/osc_assistant/observability/store.py`
- **.recent()** (5 connections) — `src/osc_assistant/observability/store.py`
- **Path** (3 connections)
- **.__init__()** (2 connections) — `src/osc_assistant/observability/store.py`
- **.path()** (2 connections) — `src/osc_assistant/observability/store.py`
- **._rotate_if_needed()** (2 connections) — `src/osc_assistant/observability/store.py`
- **.rotated_path()** (2 connections) — `src/osc_assistant/observability/store.py`
- **Record one completed trace. Never raises. A read-only filesystem, a full disk…** (1 connections) — `src/osc_assistant/observability/store.py`
- **Completed traces, most recent first.** (1 connections) — `src/osc_assistant/observability/store.py`
- **Look up by full id, or by a unique prefix — ids get pasted by hand.** (1 connections) — `src/osc_assistant/observability/store.py`
- **Yield traces newest first, current file before rotated. Reads whole files…** (1 connections) — `src/osc_assistant/observability/store.py`
- **A size-bounded, append-only log of completed traces. Two files: the one being…** (1 connections) — `src/osc_assistant/observability/store.py`
- **.clear()** (1 connections) — `src/osc_assistant/observability/store.py`

## Relationships

- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (6 shared connections)
- [Trace Sink & JSONL Parsing](Trace_Sink_%26_JSONL_Parsing.md) (3 shared connections)
- [Trace Store Tests](Trace_Store_Tests.md) (2 shared connections)
- [Observability Entry & Trace Rendering](Observability_Entry_%26_Trace_Rendering.md) (1 shared connections)
- [Observability Installation & Isolation](Observability_Installation_%26_Isolation.md) (1 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (1 shared connections)

## Source Files

- `src/osc_assistant/observability/store.py`

## Audit Trail

- EXTRACTED: 54 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*