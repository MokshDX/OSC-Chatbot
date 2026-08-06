# API Request & Response Schemas

> 21 nodes · cohesion 0.15

## Key Concepts

- **schemas.py** (22 connections) — `src/osc_assistant/api/schemas.py`
- **BaseModel** (13 connections)
- **.from_domain()** (7 connections) — `src/osc_assistant/api/schemas.py`
- **AnswerBody** (6 connections) — `src/osc_assistant/api/schemas.py`
- **ChatRequestBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **SearchResponseBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **TraceListBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **CitationBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **.to_domain()** (4 connections) — `src/osc_assistant/api/schemas.py`
- **RetrievedChunkBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **.from_domain()** (4 connections) — `src/osc_assistant/api/schemas.py`
- **SearchRequestBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **.domain_history()** (3 connections) — `src/osc_assistant/api/schemas.py`
- **.from_domain()** (3 connections) — `src/osc_assistant/api/schemas.py`
- **MessageBody** (3 connections) — `src/osc_assistant/api/schemas.py`
- **UsageBody** (3 connections) — `src/osc_assistant/api/schemas.py`
- **Any** (1 connections)
- **HTTP request and response models. These are separate from the domain types in…** (1 connections) — `src/osc_assistant/api/schemas.py`
- **The final answer. `abstained` is authoritative: when true the assistant…** (1 connections) — `src/osc_assistant/api/schemas.py`
- **Retrieval results without generation. The debugging and evaluation surface.** (1 connections) — `src/osc_assistant/api/schemas.py`
- **Recent execution traces. Development-only; see `Settings.traces_are_exposed`.** (1 connections) — `src/osc_assistant/api/schemas.py`

## Relationships

- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (10 shared connections)
- [Chat & Health Endpoints](Chat_%26_Health_Endpoints.md) (10 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (8 shared connections)
- [Trace & Status Endpoints](Trace_%26_Status_Endpoints.md) (3 shared connections)
- [Citations & Native Citation Model](Citations_%26_Native_Citation_Model.md) (2 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (2 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (1 shared connections)

## Source Files

- `src/osc_assistant/api/schemas.py`

## Audit Trail

- EXTRACTED: 100 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*