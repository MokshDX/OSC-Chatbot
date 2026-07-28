# PgVectorStore

> God node · 31 connections · `src/osc_assistant/providers/vectorstores/pgvector.py`

**Community:** [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md)

## Connections by Relation

### calls
- _build() `EXTRACTED`

### contains
- pgvector.py `EXTRACTED`

### method
- ._acquire() `EXTRACTED`
- ._migrate() `EXTRACTED`
- .replace_document() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_vector() `EXTRACTED`
- ._assert_dimensions_match() `EXTRACTED`
- .setup() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- .__init__() `EXTRACTED`
- .list_document_hashes() `EXTRACTED`
- .delete_document() `EXTRACTED`
- .document_ids() `EXTRACTED`
- .workspace_id() `EXTRACTED`
- .close() `EXTRACTED`
- .dimensions() `EXTRACTED`

### rationale_for
- Adapter over PostgreSQL with the pgvector extension. `EXTRACTED`

### references
- populated() `EXTRACTED`
- test_failed_replace_leaves_no_hash_without_chunks() `EXTRACTED`
- test_replace_document_supersedes_the_old_chunks() `EXTRACTED`
- store() `EXTRACTED`
- test_search_ignores_other_embedding_models() `EXTRACTED`
- test_workspace_isolates_queries() `EXTRACTED`
- test_deleting_a_document_cascades_to_its_chunks() `EXTRACTED`
- test_hybrid_search_fuses_both_rankings() `EXTRACTED`
- test_metadata_round_trips_as_json() `EXTRACTED`
- test_migrations_are_applied_and_idempotent() `EXTRACTED`
- test_vector_search_finds_the_nearest_chunk() `EXTRACTED`
- test_document_hashes_support_incremental_sync() `EXTRACTED`
- test_keyword_search_uses_the_generated_tsvector() `EXTRACTED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*