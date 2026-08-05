# HTTP API Layer

> 70 nodes

## Key Concepts

- **app.py** (51 connections) — `src/osc_assistant/api/app.py`
- **schemas.py** (22 connections) — `src/osc_assistant/api/schemas.py`
- **create_app()** (21 connections) — `src/osc_assistant/api/app.py`
- **logging.py** (17 connections) — `src/osc_assistant/logging.py`
- **ingestion/pipeline.py** (16 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **get_logger()** (14 connections) — `src/osc_assistant/logging.py`
- **BaseModel** (13 connections)
- **chat()** (10 connections) — `src/osc_assistant/api/app.py`
- **search()** (9 connections) — `src/osc_assistant/api/app.py`
- **health()** (7 connections) — `src/osc_assistant/api/app.py`
- **status()** (7 connections) — `src/osc_assistant/api/app.py`
- **.from_domain()** (7 connections) — `src/osc_assistant/api/schemas.py`
- **configure_logging()** (7 connections) — `src/osc_assistant/logging.py`
- **_container()** (6 connections) — `src/osc_assistant/api/app.py`
- **AnswerBody** (6 connections) — `src/osc_assistant/api/schemas.py`
- **IndexStatusBody** (6 connections) — `src/osc_assistant/api/schemas.py`
- **_register_ui()** (5 connections) — `src/osc_assistant/api/app.py`
- **Request** (5 connections)
- **get** (5 connections)
- **ChatRequestBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **SearchResponseBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **HealthBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **TraceListBody** (5 connections) — `src/osc_assistant/api/schemas.py`
- **FastAPI** (4 connections)
- **list_traces()** (4 connections) — `src/osc_assistant/api/app.py`
- *... and 45 more nodes in this community*

## Relationships

- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (15 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (8 shared connections)
- [AssistantError Base & Loaders](AssistantError_Base_%26_Loaders.md) (6 shared connections)
- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (5 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (5 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (4 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (4 shared connections)
- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (4 shared connections)
- [Settings Schema](Settings_Schema.md) (3 shared connections)
- [IndexStatistics](IndexStatistics.md) (3 shared connections)
- [Execution Tracing Core](Execution_Tracing_Core.md) (3 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (2 shared connections)

## Source Files

- `src/osc_assistant/api/app.py`
- `src/osc_assistant/api/banner.py`
- `src/osc_assistant/api/schemas.py`
- `src/osc_assistant/api/sse.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/logging.py`

## Audit Trail

- EXTRACTED: 347 (99%)
- INFERRED: 5 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*