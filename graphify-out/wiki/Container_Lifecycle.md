# Container Lifecycle

> 39 nodes

## Key Concepts

- **Container** (60 connections) — `src/osc_assistant/container.py`
- **test_e2e.py** (20 connections) — `tests/test_e2e.py`
- **Path** (7 connections)
- **indexed()** (7 connections) — `tests/test_e2e.py`
- **_build_corpus()** (5 connections) — `tests/test_e2e.py`
- **corpus()** (5 connections) — `tests/test_e2e.py`
- **test_re_running_an_unchanged_corpus_makes_no_embedding_calls()** (5 connections) — `tests/test_e2e.py`
- **.shutdown()** (4 connections) — `src/osc_assistant/container.py`
- **_write_pdf()** (4 connections) — `tests/test_e2e.py`
- **test_reindex_forces_work_the_hash_says_is_unnecessary()** (4 connections) — `tests/test_e2e.py`
- **.chunker()** (3 connections) — `src/osc_assistant/container.py`
- **.__aenter__()** (3 connections) — `src/osc_assistant/container.py`
- **test_a_corpus_of_six_formats_indexes()** (3 connections) — `tests/test_e2e.py`
- **test_hybrid_retrieval_ranks_the_right_document_first()** (3 connections) — `tests/test_e2e.py`
- **test_a_grounded_answer_cites_the_source_it_came_from()** (3 connections) — `tests/test_e2e.py`
- **test_a_question_the_corpus_cannot_answer_is_declined()** (3 connections) — `tests/test_e2e.py`
- **test_a_binary_format_is_answerable()** (3 connections) — `tests/test_e2e.py`
- **test_the_streamed_and_buffered_paths_agree_on_abstention()** (3 connections) — `tests/test_e2e.py`
- **test_the_run_is_fully_traced()** (3 connections) — `tests/test_e2e.py`
- **.embeddings()** (2 connections) — `src/osc_assistant/container.py`
- **.startup()** (2 connections) — `src/osc_assistant/container.py`
- **.__aexit__()** (2 connections) — `src/osc_assistant/container.py`
- **fixture** (2 connections)
- **Self** (1 connections)
- **Builds and owns the application's components.** (1 connections) — `src/osc_assistant/container.py`
- *... and 14 more nodes in this community*

## Relationships

- [Settings Schema](Settings_Schema.md) (9 shared connections)
- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (8 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (7 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (7 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (6 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (3 shared connections)
- [ChatModel Protocol](ChatModel_Protocol.md) (3 shared connections)
- [Filesystem Loader & Corpus Boundary](Filesystem_Loader_%26_Corpus_Boundary.md) (3 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (2 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (2 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `tests/test_e2e.py`

## Audit Trail

- EXTRACTED: 159 (92%)
- INFERRED: 13 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*