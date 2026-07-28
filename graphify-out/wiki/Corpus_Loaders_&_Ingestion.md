# Corpus Loaders & Ingestion

> 57 nodes · cohesion 0.07

## Key Concepts

- **Document** (46 connections) — `src/osc_assistant/types.py`
- **IngestionPipeline** (18 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **test_ingestion.py** (17 connections) — `tests/test_ingestion.py`
- **InMemoryLoader** (13 connections) — `src/osc_assistant/ingestion/loaders.py`
- **ingestion/pipeline.py** (13 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **ingestion/__init__.py** (12 connections) — `src/osc_assistant/ingestion/__init__.py`
- **loaders.py** (11 connections) — `src/osc_assistant/ingestion/loaders.py`
- **FilesystemLoader** (10 connections) — `src/osc_assistant/ingestion/loaders.py`
- **indexed()** (9 connections) — `tests/test_answerer.py`
- **indexed()** (9 connections) — `tests/test_retrieval.py`
- **._read()** (7 connections) — `src/osc_assistant/ingestion/loaders.py`
- **pipeline()** (7 connections) — `tests/test_ingestion.py`
- **test_one_bad_document_does_not_abort_the_sync()** (7 connections) — `tests/test_ingestion.py`
- **.ingest()** (6 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **test_prune_disabled_leaves_other_documents_alone()** (6 connections) — `tests/test_ingestion.py`
- **normalize_whitespace()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **IngestionReport** (5 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **test_documents_are_indexed()** (5 connections) — `tests/test_ingestion.py`
- **test_edited_document_is_reindexed()** (5 connections) — `tests/test_ingestion.py`
- **test_reingesting_unchanged_documents_does_no_work()** (5 connections) — `tests/test_ingestion.py`
- **test_removed_documents_are_pruned()** (5 connections) — `tests/test_ingestion.py`
- **_derive_title()** (4 connections) — `src/osc_assistant/ingestion/loaders.py`
- **stable_document_id()** (4 connections) — `src/osc_assistant/ingestion/loaders.py`
- **._index()** (4 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **.split()** (4 connections) — `src/osc_assistant/protocols.py`
- *... and 32 more nodes in this community*

## Relationships

- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (22 shared connections)
- [Chunking Strategies](Chunking_Strategies.md) (14 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (7 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (6 shared connections)
- [Chunker Registration](Chunker_Registration.md) (5 shared connections)
- [Structured Logging](Structured_Logging.md) (5 shared connections)
- [Embedding Model Interface](Embedding_Model_Interface.md) (3 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (2 shared connections)
- [Vector Store Interface](Vector_Store_Interface.md) (2 shared connections)
- [Dimension Guard & Match Source](Dimension_Guard_%26_Match_Source.md) (2 shared connections)
- [Streaming & Response Types](Streaming_%26_Response_Types.md) (2 shared connections)
- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (2 shared connections)

## Source Files

- `src/osc_assistant/chunking/recursive.py`
- `src/osc_assistant/ingestion/__init__.py`
- `src/osc_assistant/ingestion/loaders.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/types.py`
- `tests/test_answerer.py`
- `tests/test_ingestion.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 245 (85%)
- INFERRED: 43 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*