# Document

> God node · 66 connections · `src/osc_assistant/types.py`

**Community:** [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md)

## Connections by Relation

### calls
- _document() `EXTRACTED`
- _document() `EXTRACTED`
- test_a_document_that_produced_no_chunks_is_still_visible() `EXTRACTED`
- populated() `EXTRACTED`
- test_failed_replace_leaves_no_hash_without_chunks() `EXTRACTED`
- test_replace_document_supersedes_the_old_chunks() `EXTRACTED`
- test_store_rejects_wrong_width_vectors() `EXTRACTED`
- test_a_document_with_no_chunks_is_still_listed() `EXTRACTED`

### contains
- types.py `EXTRACTED`

### imports
- protocols.py `EXTRACTED`
- memory.py `EXTRACTED`
- pgvector.py `EXTRACTED`
- langchain_splitters.py `EXTRACTED`
- recursive.py `EXTRACTED`
- loaders.py `EXTRACTED`
- ingestion/pipeline.py `EXTRACTED`

### method
- .hash() `EXTRACTED`

### rationale_for
- A source document as fetched by a connector, before chunking. `EXTRACTED`

### references
- to_chunks() `EXTRACTED`
- retrieval() `EXTRACTED`
- ._read() `EXTRACTED`
- .ingest() `EXTRACTED`
- indexed() `EXTRACTED`
- indexed() `EXTRACTED`
- test_a_populated_index_produces_no_note() `EXTRACTED`
- test_genuinely_removed_documents_are_still_pruned_alongside_failures() `EXTRACTED`
- test_one_bad_document_does_not_abort_the_sync() `EXTRACTED`
- test_unreadable_documents_are_not_pruned() `EXTRACTED`
- exploding_client() `EXTRACTED`
- test_a_known_provider_failure_keeps_its_actionable_message() `EXTRACTED`
- .split() `EXTRACTED`
- .split() `EXTRACTED`
- .replace_document() `EXTRACTED`
- .replace_document() `EXTRACTED`
- test_a_sync_reports_the_trace_that_produced_it() `EXTRACTED`
- test_prune_disabled_leaves_other_documents_alone() `EXTRACTED`
- test_reindex_forces_work_the_content_hash_says_is_unnecessary() `EXTRACTED`
- .split() `EXTRACTED`

### uses
- [StubEmbeddingModel](StubEmbeddingModel.md) `INFERRED`
- [StubChatModel](StubChatModel.md) `INFERRED`
- ChatModel `INFERRED`
- EmbeddingModel `INFERRED`
- VectorStore `INFERRED`
- Chunker `INFERRED`
- Reranker `INFERRED`
- _FakeEmbeddings `INFERRED`
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- StoreInspector `INFERRED`
- _ClosableEmbedding `INFERRED`
- FailingChatModel `INFERRED`
- NativeCitationChatModel `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*