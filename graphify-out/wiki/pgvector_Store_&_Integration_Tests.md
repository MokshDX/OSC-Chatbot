# pgvector Store & Integration Tests

> 48 nodes · cohesion 0.07

## Key Concepts

- **PgVectorStore** (43 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_pgvector_integration.py** (26 connections) — `tests/test_pgvector_integration.py`
- **EmbeddedChunk** (20 connections) — `src/osc_assistant/types.py`
- **PgVectorOptions** (7 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **populated()** (7 connections) — `tests/test_pgvector_integration.py`
- **test_failed_replace_leaves_no_hash_without_chunks()** (7 connections) — `tests/test_pgvector_integration.py`
- **test_replace_document_supersedes_the_old_chunks()** (7 connections) — `tests/test_pgvector_integration.py`
- **.replace_document()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **store()** (5 connections) — `tests/test_pgvector_integration.py`
- **test_search_ignores_other_embedding_models()** (5 connections) — `tests/test_pgvector_integration.py`
- **test_workspace_isolates_queries()** (5 connections) — `tests/test_pgvector_integration.py`
- **embeddings()** (4 connections) — `tests/test_pgvector_integration.py`
- **test_a_document_with_no_chunks_is_still_listed()** (4 connections) — `tests/test_pgvector_integration.py`
- **test_statistics_are_scoped_to_the_workspace()** (4 connections) — `tests/test_pgvector_integration.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.list_document_hashes()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **fixture** (3 connections)
- **test_deleting_a_document_cascades_to_its_chunks()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_hybrid_search_fuses_both_rankings()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_metadata_round_trips_as_json()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_migrations_are_applied_and_idempotent()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_vector_search_finds_the_nearest_chunk()** (3 connections) — `tests/test_pgvector_integration.py`
- **.document_ids()** (2 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.workspace_id()** (2 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_a_chunk_round_trips_with_its_metadata()** (2 connections) — `tests/test_pgvector_integration.py`
- *... and 23 more nodes in this community*

## Relationships

- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (12 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (12 shared connections)
- [VectorStore Errors & Inspection](VectorStore_Errors_%26_Inspection.md) (7 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (6 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (4 shared connections)
- [Store Construction & Embedding Calls](Store_Construction_%26_Embedding_Calls.md) (3 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (2 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (2 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (2 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (1 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (1 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `src/osc_assistant/types.py`
- `tests/test_pgvector_integration.py`

## Audit Trail

- EXTRACTED: 203 (97%)
- INFERRED: 6 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*