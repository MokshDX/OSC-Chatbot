# Persistent Trace Store Tests

> 22 nodes

## Key Concepts

- **schemas.py** (17 connections) — `src/osc_assistant/api/schemas.py`
- **BaseModel** (14 connections)
- **search()** (9 connections) — `src/osc_assistant/api/app.py`
- **.from_domain()** (7 connections) — `src/osc_assistant/api/schemas.py`
- **AnswerBody** (6 connections) — `src/osc_assistant/api/schemas.py`
- **SearchResponseBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **HealthBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **SearchRequestBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **CitationBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **RetrievedChunkBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **.from_domain()** (4 connections) — `src/osc_assistant/api/schemas.py`
- **.from_domain()** (3 connections) — `src/osc_assistant/api/schemas.py`
- **UsageBody** (3 connections) — `src/osc_assistant/api/schemas.py`
- **Any** (1 connections)
- **Run retrieval only. Exposed as its own endpoint because retrieval quality is…** (1 connections) — `src/osc_assistant/api/app.py`
- **Citation** (1 connections)
- **ScoredChunk** (1 connections)
- **Answer** (1 connections)
- **HTTP request and response models. These are separate from the domain types in…** (1 connections) — `src/osc_assistant/api/schemas.py`
- **The final answer. `abstained` is authoritative: when true the assistant…** (1 connections) — `src/osc_assistant/api/schemas.py`
- **Retrieval results without generation. The debugging and evaluation surface.** (1 connections) — `src/osc_assistant/api/schemas.py`
- **Health plus the active component set, so a deployment is self-describing.** (1 connections) — `src/osc_assistant/api/schemas.py`

## Relationships

- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (10 shared connections)
- [Fusion & Provider Packages](Fusion_%26_Provider_Packages.md) (7 shared connections)
- [Chat & Session Route Handlers](Chat_%26_Session_Route_Handlers.md) (6 shared connections)
- [API Request Schemas](API_Request_Schemas.md) (4 shared connections)
- [Trace HTTP Endpoints](Trace_HTTP_Endpoints.md) (2 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (1 shared connections)

## Source Files

- `src/osc_assistant/api/app.py`
- `src/osc_assistant/api/schemas.py`

## Audit Trail

- EXTRACTED: 94 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*