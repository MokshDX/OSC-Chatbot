# HTTP API Layer

> 45 nodes · cohesion 0.09

## Key Concepts

- **app.py** (37 connections) — `src/osc_assistant/api/app.py`
- **schemas.py** (19 connections) — `src/osc_assistant/api/schemas.py`
- **BaseModel** (11 connections)
- **create_app()** (10 connections) — `src/osc_assistant/api/app.py`
- **chat()** (9 connections) — `src/osc_assistant/api/app.py`
- **search()** (8 connections) — `src/osc_assistant/api/app.py`
- **health()** (7 connections) — `src/osc_assistant/api/app.py`
- **AnswerBody** (6 connections) — `src/osc_assistant/api/schemas.py`
- **.from_domain()** (6 connections) — `src/osc_assistant/api/schemas.py`
- **_container()** (5 connections) — `src/osc_assistant/api/app.py`
- **ChatRequestBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **HealthBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **SearchResponseBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **Request** (4 connections)
- **_register_error_handlers()** (4 connections) — `src/osc_assistant/api/app.py`
- **CitationBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **ComponentBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **ErrorBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **.to_domain()** (4 connections) — `src/osc_assistant/api/schemas.py`
- **RetrievedChunkBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **.from_domain()** (4 connections) — `src/osc_assistant/api/schemas.py`
- **SearchRequestBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **encode_event()** (4 connections) — `src/osc_assistant/api/sse.py`
- **FastAPI** (3 connections)
- **api/__init__.py** (3 connections) — `src/osc_assistant/api/__init__.py`
- *... and 20 more nodes in this community*

## Relationships

- [Error Hierarchy](Error_Hierarchy.md) (7 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (7 shared connections)
- [Structured Logging](Structured_Logging.md) (5 shared connections)
- [Settings Loading & YAML Profiles](Settings_Loading_%26_YAML_Profiles.md) (4 shared connections)
- [Streaming & Response Types](Streaming_%26_Response_Types.md) (4 shared connections)
- [Composition Root](Composition_Root.md) (2 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (2 shared connections)
- [Hybrid Search Scoring](Hybrid_Search_Scoring.md) (2 shared connections)
- [Settings Schema](Settings_Schema.md) (1 shared connections)

## Source Files

- `src/osc_assistant/api/__init__.py`
- `src/osc_assistant/api/app.py`
- `src/osc_assistant/api/schemas.py`
- `src/osc_assistant/api/sse.py`

## Audit Trail

- EXTRACTED: 209 (100%)
- INFERRED: 1 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*