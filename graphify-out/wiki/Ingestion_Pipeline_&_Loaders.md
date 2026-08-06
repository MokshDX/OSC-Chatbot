# Ingestion Pipeline & Loaders

> 42 nodes · cohesion 0.10

## Key Concepts

- **Document** (66 connections) — `src/osc_assistant/types.py`
- **IngestionPipeline** (27 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **InMemoryLoader** (22 connections) — `src/osc_assistant/ingestion/loaders.py`
- **test_ingestion.py** (22 connections) — `tests/test_ingestion.py`
- **test_osc_retrieval_is_usable_as_a_langchain_retriever()** (10 connections) — `tests/test_langchain_integration.py`
- **.ingest()** (9 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **indexed()** (9 connections) — `tests/test_answerer.py`
- **indexed()** (9 connections) — `tests/test_retrieval.py`
- **test_a_populated_index_produces_no_note()** (9 connections) — `tests/test_server_lifecycle.py`
- **LoadFailure** (8 connections) — `src/osc_assistant/types.py`
- **test_a_document_that_produced_no_chunks_is_still_visible()** (8 connections) — `tests/test_inspection.py`
- **test_genuinely_removed_documents_are_still_pruned_alongside_failures()** (7 connections) — `tests/test_ingestion.py`
- **test_one_bad_document_does_not_abort_the_sync()** (7 connections) — `tests/test_ingestion.py`
- **test_unreadable_documents_are_not_pruned()** (7 connections) — `tests/test_ingestion.py`
- **test_a_sync_reports_the_trace_that_produced_it()** (6 connections) — `tests/test_ingestion.py`
- **test_prune_disabled_leaves_other_documents_alone()** (6 connections) — `tests/test_ingestion.py`
- **test_reindex_forces_work_the_content_hash_says_is_unnecessary()** (6 connections) — `tests/test_ingestion.py`
- **._index()** (5 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **test_documents_are_indexed()** (5 connections) — `tests/test_ingestion.py`
- **test_edited_document_is_reindexed()** (5 connections) — `tests/test_ingestion.py`
- **test_reingesting_unchanged_documents_does_no_work()** (5 connections) — `tests/test_ingestion.py`
- **test_removed_documents_are_pruned()** (5 connections) — `tests/test_ingestion.py`
- **._prune()** (3 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **.__init__()** (2 connections) — `src/osc_assistant/ingestion/loaders.py`
- **.load()** (2 connections) — `src/osc_assistant/ingestion/loaders.py`
- *... and 17 more nodes in this community*

## Relationships

- [Chunker Registration & Options](Chunker_Registration_%26_Options.md) (16 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (14 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (9 shared connections)
- [Whitespace Normalisation & Error Base](Whitespace_Normalisation_%26_Error_Base.md) (7 shared connections)
- [Filesystem Loader & Title Derivation](Filesystem_Loader_%26_Title_Derivation.md) (7 shared connections)
- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (6 shared connections)
- [Recursive & Markdown Splitting](Recursive_%26_Markdown_Splitting.md) (6 shared connections)
- [Noop Reranker & Evaluation Corpus](Noop_Reranker_%26_Evaluation_Corpus.md) (5 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (4 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (4 shared connections)
- [Server Lifecycle Tests](Server_Lifecycle_Tests.md) (4 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (3 shared connections)

## Source Files

- `src/osc_assistant/ingestion/loaders.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/types.py`
- `tests/test_answerer.py`
- `tests/test_ingestion.py`
- `tests/test_inspection.py`
- `tests/test_langchain_integration.py`
- `tests/test_retrieval.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 214 (75%)
- INFERRED: 73 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*