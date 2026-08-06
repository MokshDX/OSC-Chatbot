# Trace & Status Endpoints

> 10 nodes · cohesion 0.22

## Key Concepts

- **status()** (7 connections) — `src/osc_assistant/api/app.py`
- **IndexStatusBody** (6 connections) — `src/osc_assistant/api/schemas.py`
- **get** (5 connections)
- **list_traces()** (4 connections) — `src/osc_assistant/api/app.py`
- **get_trace()** (3 connections) — `src/osc_assistant/api/app.py`
- **.from_domain()** (3 connections) — `src/osc_assistant/api/schemas.py`
- **What is currently indexed. Separate from `/health` because it queries the…** (1 connections) — `src/osc_assistant/api/app.py`
- **Recent execution traces, most recent first.** (1 connections) — `src/osc_assistant/api/app.py`
- **One execution trace in full, by id or unique prefix.** (1 connections) — `src/osc_assistant/api/app.py`
- **What the store currently holds. The admin view the CLI also renders.** (1 connections) — `src/osc_assistant/api/schemas.py`

## Relationships

- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (5 shared connections)
- [Chat & Health Endpoints](Chat_%26_Health_Endpoints.md) (3 shared connections)
- [API Request & Response Schemas](API_Request_%26_Response_Schemas.md) (3 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (1 shared connections)

## Source Files

- `src/osc_assistant/api/app.py`
- `src/osc_assistant/api/schemas.py`

## Audit Trail

- EXTRACTED: 32 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*