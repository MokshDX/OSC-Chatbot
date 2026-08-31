# Chat & Session Route Handlers

> 10 nodes

## Key Concepts

- **chat()** (10 connections) — `src/osc_assistant/api/app.py`
- **open_session()** (6 connections) — `src/osc_assistant/api/app.py`
- **SessionBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **_trace_payload()** (4 connections) — `src/osc_assistant/api/app.py`
- **post** (3 connections)
- **StreamingResponse** (1 connections)
- **The trace for `trace_id`, if it is still in the buffer. Returned inline on…** (1 connections) — `src/osc_assistant/api/app.py`
- **Open a conversation. Sessions are ephemeral: memory lives in this process, is…** (1 connections) — `src/osc_assistant/api/app.py`
- **Answer a question, streaming by default. Three shapes, one handler: a one-shot…** (1 connections) — `src/osc_assistant/api/app.py`
- **A session id. The only thing a client needs to keep between turns.** (1 connections) — `src/osc_assistant/api/schemas.py`

## Relationships

- [Persistent Trace Store Tests](Persistent_Trace_Store_Tests.md) (6 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (4 shared connections)
- [Fusion & Provider Packages](Fusion_%26_Provider_Packages.md) (4 shared connections)
- [API Request Schemas](API_Request_Schemas.md) (1 shared connections)

## Source Files

- `src/osc_assistant/api/app.py`
- `src/osc_assistant/api/schemas.py`

## Audit Trail

- EXTRACTED: 33 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*