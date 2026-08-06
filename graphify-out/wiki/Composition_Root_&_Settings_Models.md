# Composition Root & Settings Models

> 41 nodes · cohesion 0.08

## Key Concepts

- **settings.py** (34 connections) — `src/osc_assistant/settings.py`
- **container.py** (31 connections) — `src/osc_assistant/container.py`
- **_SyncClosableReranker** (23 connections) — `tests/test_server_lifecycle.py`
- **RetrievalSettings** (21 connections) — `src/osc_assistant/settings.py`
- **_ClosableEmbedding** (21 connections) — `tests/test_server_lifecycle.py`
- **test_e2e.py** (20 connections) — `tests/test_e2e.py`
- **GenerationSettings** (11 connections) — `src/osc_assistant/settings.py`
- **_settings()** (10 connections) — `tests/test_e2e.py`
- **ChunkingSettings** (8 connections) — `src/osc_assistant/settings.py`
- **BaseModel** (7 connections)
- **indexed()** (7 connections) — `tests/test_e2e.py`
- **Path** (7 connections)
- **ObservabilitySettings** (5 connections) — `src/osc_assistant/settings.py`
- **_build_corpus()** (5 connections) — `tests/test_e2e.py`
- **corpus()** (5 connections) — `tests/test_e2e.py`
- **test_re_running_an_unchanged_corpus_makes_no_embedding_calls()** (5 connections) — `tests/test_e2e.py`
- **DatabaseSettings** (4 connections) — `src/osc_assistant/settings.py`
- **LoggingSettings** (4 connections) — `src/osc_assistant/settings.py`
- **test_reindex_forces_work_the_hash_says_is_unnecessary()** (4 connections) — `tests/test_e2e.py`
- **_write_pdf()** (4 connections) — `tests/test_e2e.py`
- **ServerSettings** (3 connections) — `src/osc_assistant/settings.py`
- **fixture** (2 connections)
- **.__init__()** (2 connections) — `tests/test_server_lifecycle.py`
- **.__init__()** (2 connections) — `tests/test_server_lifecycle.py`
- **Composition root. The only module that knows both which providers exist and how…** (1 connections) — `src/osc_assistant/container.py`
- *... and 16 more nodes in this community*

## Relationships

- [Container Lifecycle & E2E](Container_Lifecycle_%26_E2E.md) (16 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (13 shared connections)
- [Server Lifecycle Tests](Server_Lifecycle_Tests.md) (9 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (8 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (7 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (7 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (6 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (6 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (6 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (5 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (4 shared connections)
- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (3 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/settings.py`
- `tests/test_e2e.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 210 (80%)
- INFERRED: 52 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*