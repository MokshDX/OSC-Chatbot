# pgvector Store Interface

> 38 nodes

## Key Concepts

- **PgVectorStore** (43 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_pgvector_integration.py** (26 connections) — `tests/test_pgvector_integration.py`
- **PgVectorOptions** (7 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_replace_document_supersedes_the_old_chunks()** (7 connections) — `tests/test_pgvector_integration.py`
- **store()** (5 connections) — `tests/test_pgvector_integration.py`
- **test_workspace_isolates_queries()** (5 connections) — `tests/test_pgvector_integration.py`
- **test_search_ignores_other_embedding_models()** (5 connections) — `tests/test_pgvector_integration.py`
- **test_statistics_are_scoped_to_the_workspace()** (4 connections) — `tests/test_pgvector_integration.py`
- **test_a_document_with_no_chunks_is_still_listed()** (4 connections) — `tests/test_pgvector_integration.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.list_document_hashes()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_migrations_are_applied_and_idempotent()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_vector_search_finds_the_nearest_chunk()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_hybrid_search_fuses_both_rankings()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_metadata_round_trips_as_json()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_deleting_a_document_cascades_to_its_chunks()** (3 connections) — `tests/test_pgvector_integration.py`
- **.workspace_id()** (2 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.document_ids()** (2 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_keyword_search_uses_the_generated_tsvector()** (2 connections) — `tests/test_pgvector_integration.py`
- **test_document_hashes_support_incremental_sync()** (2 connections) — `tests/test_pgvector_integration.py`
- **test_statistics_are_computed_in_sql()** (2 connections) — `tests/test_pgvector_integration.py`
- **test_documents_are_listed_with_their_chunk_counts()** (2 connections) — `tests/test_pgvector_integration.py`
- **test_document_search_matches_title_or_uri()** (2 connections) — `tests/test_pgvector_integration.py`
- **test_a_chunk_round_trips_with_its_metadata()** (2 connections) — `tests/test_pgvector_integration.py`
- **test_missing_records_return_none()** (2 connections) — `tests/test_pgvector_integration.py`
- *... and 13 more nodes in this community*

## Relationships

- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (11 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (8 shared connections)
- [EmbeddedChunk](EmbeddedChunk.md) (7 shared connections)
- [Vector Store Registration](Vector_Store_Registration.md) (5 shared connections)
- [Store Inspector](Store_Inspector.md) (2 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)
- [IndexStatistics](IndexStatistics.md) (1 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (1 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (1 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `tests/test_pgvector_integration.py`

## Audit Trail

- EXTRACTED: 158 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*