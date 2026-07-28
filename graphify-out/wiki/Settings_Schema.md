# Settings Schema

> 10 nodes · cohesion 0.33

## Key Concepts

- **settings.py** (20 connections) — `src/osc_assistant/settings.py`
- **RetrievalSettings** (11 connections) — `src/osc_assistant/settings.py`
- **GenerationSettings** (7 connections) — `src/osc_assistant/settings.py`
- **_settings()** (7 connections) — `tests/test_api.py`
- **BaseModel** (5 connections)
- **ChunkingSettings** (4 connections) — `src/osc_assistant/settings.py`
- **DatabaseSettings** (3 connections) — `src/osc_assistant/settings.py`
- **ServerSettings** (3 connections) — `src/osc_assistant/settings.py`
- **Configuration. Layered, highest precedence first: process environment, then…** (1 connections) — `src/osc_assistant/settings.py`
- **Tuning for the retrieval stage. Every value here is an experiment knob.** (1 connections) — `src/osc_assistant/settings.py`

## Relationships

- [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md) (7 shared connections)
- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (7 shared connections)
- [Settings Loading & YAML Profiles](Settings_Loading_%26_YAML_Profiles.md) (5 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (4 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (3 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (2 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (1 shared connections)
- [Command Line Interface](Command_Line_Interface.md) (1 shared connections)
- [Structured Logging](Structured_Logging.md) (1 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (1 shared connections)

## Source Files

- `src/osc_assistant/settings.py`
- `tests/test_api.py`

## Audit Trail

- EXTRACTED: 57 (92%)
- INFERRED: 5 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*