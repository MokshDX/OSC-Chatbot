# Fusion & Provider Packages

> 14 nodes

## Key Concepts

- **_container()** (8 connections) — `src/osc_assistant/api/app.py`
- **Request** (7 connections)
- **health()** (7 connections) — `src/osc_assistant/api/app.py`
- **status()** (7 connections) — `src/osc_assistant/api/app.py`
- **IndexStatusBody** (6 connections) — `src/osc_assistant/api/schemas.py`
- **close_session()** (5 connections) — `src/osc_assistant/api/app.py`
- **ComponentBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **.from_domain()** (3 connections) — `src/osc_assistant/api/schemas.py`
- **delete** (1 connections)
- **Liveness plus the active component set. Returning the resolved configuration…** (1 connections) — `src/osc_assistant/api/app.py`
- **What is currently indexed. Separate from `/health` because it queries the…** (1 connections) — `src/osc_assistant/api/app.py`
- **Destroy a session and everything remembered in it. Idempotent: closing an…** (1 connections) — `src/osc_assistant/api/app.py`
- **IndexStatistics** (1 connections)
- **What the store currently holds. The admin view the CLI also renders.** (1 connections) — `src/osc_assistant/api/schemas.py`

## Relationships

- [Persistent Trace Store Tests](Persistent_Trace_Store_Tests.md) (7 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (6 shared connections)
- [Chat & Session Route Handlers](Chat_%26_Session_Route_Handlers.md) (4 shared connections)
- [Trace HTTP Endpoints](Trace_HTTP_Endpoints.md) (2 shared connections)

## Source Files

- `src/osc_assistant/api/app.py`
- `src/osc_assistant/api/schemas.py`

## Audit Trail

- EXTRACTED: 53 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*