# Ingestion Pipeline & Loaders

> 45 nodes

## Key Concepts

- **Document** (70 connections) — `src/osc_assistant/types.py`
- **IngestionPipeline** (27 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **InMemoryLoader** (22 connections) — `src/osc_assistant/ingestion/loaders.py`
- **test_ingestion.py** (22 connections) — `tests/test_ingestion.py`
- **retrieval()** (12 connections) — `tests/test_evaluation.py`
- **.ingest()** (9 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **indexed()** (9 connections) — `tests/test_answerer.py`
- **indexed()** (9 connections) — `tests/test_retrieval.py`
- **test_a_populated_index_produces_no_note()** (9 connections) — `tests/test_server_lifecycle.py`
- **test_a_document_that_produced_no_chunks_is_still_visible()** (8 connections) — `tests/test_inspection.py`
- **pipeline()** (7 connections) — `tests/test_ingestion.py`
- **test_unreadable_documents_are_not_pruned()** (7 connections) — `tests/test_ingestion.py`
- **test_genuinely_removed_documents_are_still_pruned_alongside_failures()** (7 connections) — `tests/test_ingestion.py`
- **test_one_bad_document_does_not_abort_the_sync()** (7 connections) — `tests/test_ingestion.py`
- **test_prune_disabled_leaves_other_documents_alone()** (6 connections) — `tests/test_ingestion.py`
- **test_reindex_forces_work_the_content_hash_says_is_unnecessary()** (6 connections) — `tests/test_ingestion.py`
- **test_a_sync_reports_the_trace_that_produced_it()** (6 connections) — `tests/test_ingestion.py`
- **._index()** (5 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **test_documents_are_indexed()** (5 connections) — `tests/test_ingestion.py`
- **test_reingesting_unchanged_documents_does_no_work()** (5 connections) — `tests/test_ingestion.py`
- **test_edited_document_is_reindexed()** (5 connections) — `tests/test_ingestion.py`
- **test_removed_documents_are_pruned()** (5 connections) — `tests/test_ingestion.py`
- **corpus()** (4 connections) — `tests/test_evaluation.py`
- **._prune()** (3 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **.ingestion()** (2 connections) — `src/osc_assistant/container.py`
- *... and 20 more nodes in this community*

## Relationships

- [Recursive Chunker](Recursive_Chunker.md) (19 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (14 shared connections)
- [AssistantError Base & Loaders](AssistantError_Base_%26_Loaders.md) (11 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (9 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (7 shared connections)
- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (6 shared connections)
- [Chunker Registration](Chunker_Registration.md) (5 shared connections)
- [EmbeddedChunk](EmbeddedChunk.md) (4 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (4 shared connections)
- [Filesystem Loader & Corpus Boundary](Filesystem_Loader_%26_Corpus_Boundary.md) (4 shared connections)
- [Tracing & Retrieval Instrumentation](Tracing_%26_Retrieval_Instrumentation.md) (3 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (3 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/ingestion/loaders.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/types.py`
- `tests/test_answerer.py`
- `tests/test_evaluation.py`
- `tests/test_ingestion.py`
- `tests/test_inspection.py`
- `tests/test_retrieval.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 226 (75%)
- INFERRED: 74 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*