# pgvector Store & Integration Tests

> 31 nodes · cohesion 0.10

## Key Concepts

- **PgVectorStore** (31 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_pgvector_integration.py** (18 connections) — `tests/test_pgvector_integration.py`
- **test_failed_replace_leaves_no_hash_without_chunks()** (7 connections) — `tests/test_pgvector_integration.py`
- **test_replace_document_supersedes_the_old_chunks()** (7 connections) — `tests/test_pgvector_integration.py`
- **PgVectorOptions** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **store()** (5 connections) — `tests/test_pgvector_integration.py`
- **test_search_ignores_other_embedding_models()** (5 connections) — `tests/test_pgvector_integration.py`
- **test_workspace_isolates_queries()** (5 connections) — `tests/test_pgvector_integration.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.list_document_hashes()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_deleting_a_document_cascades_to_its_chunks()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_hybrid_search_fuses_both_rankings()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_metadata_round_trips_as_json()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_migrations_are_applied_and_idempotent()** (3 connections) — `tests/test_pgvector_integration.py`
- **test_vector_search_finds_the_nearest_chunk()** (3 connections) — `tests/test_pgvector_integration.py`
- **.document_ids()** (2 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.workspace_id()** (2 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_document_hashes_support_incremental_sync()** (2 connections) — `tests/test_pgvector_integration.py`
- **test_keyword_search_uses_the_generated_tsvector()** (2 connections) — `tests/test_pgvector_integration.py`
- **.close()** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.dimensions()** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **BaseModel** (1 connections)
- **Adapter over PostgreSQL with the pgvector extension.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **The partition this store reads and writes. Every query is scoped to it.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Integration tests for the PostgreSQL store. Skipped unless `OSC_TEST_DSN`…** (1 connections) — `tests/test_pgvector_integration.py`
- *... and 6 more nodes in this community*

## Relationships

- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (10 shared connections)
- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (9 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (7 shared connections)
- [pgvector Setup & Codecs](pgvector_Setup_%26_Codecs.md) (5 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (2 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (2 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `tests/test_pgvector_integration.py`

## Audit Trail

- EXTRACTED: 125 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*