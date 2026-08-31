# Trace HTTP Endpoints

> 7 nodes

## Key Concepts

- **get** (5 connections)
- **TraceListBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **list_traces()** (4 connections) — `src/osc_assistant/api/app.py`
- **get_trace()** (3 connections) — `src/osc_assistant/api/app.py`
- **Recent execution traces, most recent first.** (1 connections) — `src/osc_assistant/api/app.py`
- **One execution trace in full, by id or unique prefix.** (1 connections) — `src/osc_assistant/api/app.py`
- **Recent execution traces. Development-only; see `Settings.traces_are_exposed`.** (1 connections) — `src/osc_assistant/api/schemas.py`

## Relationships

- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (4 shared connections)
- [Fusion & Provider Packages](Fusion_%26_Provider_Packages.md) (2 shared connections)
- [Persistent Trace Store Tests](Persistent_Trace_Store_Tests.md) (2 shared connections)

## Source Files

- `src/osc_assistant/api/app.py`
- `src/osc_assistant/api/schemas.py`

## Audit Trail

- EXTRACTED: 20 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*