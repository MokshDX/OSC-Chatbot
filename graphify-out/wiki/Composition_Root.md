# Composition Root

> 14 nodes · cohesion 0.16

## Key Concepts

- **Container** (27 connections) — `src/osc_assistant/container.py`
- **.vector_store()** (4 connections) — `src/osc_assistant/container.py`
- **.__aenter__()** (3 connections) — `src/osc_assistant/container.py`
- **.fast_llm()** (3 connections) — `src/osc_assistant/container.py`
- **.__aexit__()** (2 connections) — `src/osc_assistant/container.py`
- **.answerer()** (2 connections) — `src/osc_assistant/container.py`
- **.ingestion()** (2 connections) — `src/osc_assistant/container.py`
- **.llm()** (2 connections) — `src/osc_assistant/container.py`
- **.shutdown()** (2 connections) — `src/osc_assistant/container.py`
- **.startup()** (2 connections) — `src/osc_assistant/container.py`
- **Self** (1 connections)
- **A cheaper model for auxiliary steps such as query rewriting.** (1 connections) — `src/osc_assistant/container.py`
- **Builds and owns the application's components.** (1 connections) — `src/osc_assistant/container.py`
- **Build the store, injecting values it cannot know on its own. Vector width, the…** (1 connections) — `src/osc_assistant/container.py`

## Relationships

- [Settings Loading & YAML Profiles](Settings_Loading_%26_YAML_Profiles.md) (3 shared connections)
- [Chat Model Interface](Chat_Model_Interface.md) (3 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Chunker Registration](Chunker_Registration.md) (2 shared connections)
- [Embedding Model Interface](Embedding_Model_Interface.md) (2 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (2 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (2 shared connections)
- [Vector Store Interface](Vector_Store_Interface.md) (2 shared connections)
- [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md) (2 shared connections)
- [Command Line Interface](Command_Line_Interface.md) (1 shared connections)
- [Structured Logging](Structured_Logging.md) (1 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (1 shared connections)

## Source Files

- `src/osc_assistant/container.py`

## Audit Trail

- EXTRACTED: 46 (87%)
- INFERRED: 7 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*