# Settings Schema

> 30 nodes

## Key Concepts

- **Settings** (38 connections) — `src/osc_assistant/settings.py`
- **settings.py** (31 connections) — `src/osc_assistant/settings.py`
- **_SyncClosableReranker** (23 connections) — `tests/test_server_lifecycle.py`
- **RetrievalSettings** (22 connections) — `src/osc_assistant/settings.py`
- **_ClosableEmbedding** (21 connections) — `tests/test_server_lifecycle.py`
- **GenerationSettings** (12 connections) — `src/osc_assistant/settings.py`
- **_settings()** (10 connections) — `tests/test_e2e.py`
- **ChunkingSettings** (9 connections) — `src/osc_assistant/settings.py`
- **_settings()** (8 connections) — `tests/test_api.py`
- **osc_assistant/__init__.py** (6 connections) — `src/osc_assistant/__init__.py`
- **BaseModel** (6 connections)
- **ObservabilitySettings** (5 connections) — `src/osc_assistant/settings.py`
- **DatabaseSettings** (4 connections) — `src/osc_assistant/settings.py`
- **ServerSettings** (3 connections) — `src/osc_assistant/settings.py`
- **.__init__()** (2 connections) — `src/osc_assistant/container.py`
- **.traces_are_exposed()** (2 connections) — `src/osc_assistant/settings.py`
- **.__init__()** (2 connections) — `tests/test_server_lifecycle.py`
- **.__init__()** (2 connections) — `tests/test_server_lifecycle.py`
- **OSC internal knowledge assistant. A provider-agnostic retrieval-augmented…** (1 connections) — `src/osc_assistant/__init__.py`
- **Configuration. Layered, highest precedence first: process environment, then…** (1 connections) — `src/osc_assistant/settings.py`
- **Tuning for the retrieval stage. Every value here is an experiment knob.** (1 connections) — `src/osc_assistant/settings.py`
- **How much the system records about its own execution. Defaults are chosen for a…** (1 connections) — `src/osc_assistant/settings.py`
- **Root configuration object. Nested values are addressable from the environment…** (1 connections) — `src/osc_assistant/settings.py`
- **Whether the HTTP trace endpoints should be registered. Two conditions, not one.…** (1 connections) — `src/osc_assistant/settings.py`
- **.aclose()** (1 connections) — `tests/test_server_lifecycle.py`
- *... and 5 more nodes in this community*

## Relationships

- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (14 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (13 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (9 shared connections)
- [Settings Loading & YAML Profiles](Settings_Loading_%26_YAML_Profiles.md) (9 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (8 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (6 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (6 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (6 shared connections)
- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (6 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (5 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (4 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (4 shared connections)

## Source Files

- `src/osc_assistant/__init__.py`
- `src/osc_assistant/container.py`
- `src/osc_assistant/settings.py`
- `tests/test_api.py`
- `tests/test_e2e.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 165 (76%)
- INFERRED: 53 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*