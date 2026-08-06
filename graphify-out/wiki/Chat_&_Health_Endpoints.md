# Chat & Health Endpoints

> 15 nodes · cohesion 0.18

## Key Concepts

- **chat()** (10 connections) — `src/osc_assistant/api/app.py`
- **search()** (9 connections) — `src/osc_assistant/api/app.py`
- **health()** (7 connections) — `src/osc_assistant/api/app.py`
- **_container()** (6 connections) — `src/osc_assistant/api/app.py`
- **Request** (5 connections)
- **HealthBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **_trace_payload()** (4 connections) — `src/osc_assistant/api/app.py`
- **ComponentBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **post** (2 connections)
- **Liveness plus the active component set. Returning the resolved configuration…** (1 connections) — `src/osc_assistant/api/app.py`
- **Run retrieval only. Exposed as its own endpoint because retrieval quality is…** (1 connections) — `src/osc_assistant/api/app.py`
- **The trace for `trace_id`, if it is still in the buffer. Returned inline on…** (1 connections) — `src/osc_assistant/api/app.py`
- **Answer a question, streaming by default.** (1 connections) — `src/osc_assistant/api/app.py`
- **Health plus the active component set, so a deployment is self-describing.** (1 connections) — `src/osc_assistant/api/schemas.py`
- **StreamingResponse** (1 connections)

## Relationships

- [API Request & Response Schemas](API_Request_%26_Response_Schemas.md) (10 shared connections)
- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (7 shared connections)
- [Trace & Status Endpoints](Trace_%26_Status_Endpoints.md) (3 shared connections)

## Source Files

- `src/osc_assistant/api/app.py`
- `src/osc_assistant/api/schemas.py`

## Audit Trail

- EXTRACTED: 58 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*