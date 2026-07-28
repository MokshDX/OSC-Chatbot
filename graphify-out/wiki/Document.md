# Document

> God node · 46 connections · `src/osc_assistant/types.py`

**Community:** [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md)

## Connections by Relation

### calls
- _document() `EXTRACTED`
- populated() `EXTRACTED`
- test_failed_replace_leaves_no_hash_without_chunks() `EXTRACTED`
- test_replace_document_supersedes_the_old_chunks() `EXTRACTED`
- test_store_rejects_wrong_width_vectors() `EXTRACTED`

### contains
- types.py `EXTRACTED`

### imports
- protocols.py `EXTRACTED`
- pgvector.py `EXTRACTED`
- memory.py `EXTRACTED`
- recursive.py `EXTRACTED`
- ingestion/pipeline.py `EXTRACTED`
- loaders.py `EXTRACTED`

### method
- .hash() `EXTRACTED`

### rationale_for
- A source document as fetched by a connector, before chunking. `EXTRACTED`

### references
- indexed() `EXTRACTED`
- indexed() `EXTRACTED`
- ._read() `EXTRACTED`
- test_one_bad_document_does_not_abort_the_sync() `EXTRACTED`
- .split() `EXTRACTED`
- _to_chunks() `EXTRACTED`
- .ingest() `EXTRACTED`
- .replace_document() `EXTRACTED`
- .replace_document() `EXTRACTED`
- client() `EXTRACTED`
- test_prune_disabled_leaves_other_documents_alone() `EXTRACTED`
- .split() `EXTRACTED`
- test_documents_are_indexed() `EXTRACTED`
- test_edited_document_is_reindexed() `EXTRACTED`
- test_reingesting_unchanged_documents_does_no_work() `EXTRACTED`
- test_removed_documents_are_pruned() `EXTRACTED`
- ._index() `EXTRACTED`
- .replace_document() `EXTRACTED`
- .split() `EXTRACTED`
- .load() `EXTRACTED`

### uses
- [StubEmbeddingModel](StubEmbeddingModel.md) `INFERRED`
- [StubChatModel](StubChatModel.md) `INFERRED`
- [VectorStore](VectorStore.md) `INFERRED`
- [EmbeddingModel](EmbeddingModel.md) `INFERRED`
- ChatModel `INFERRED`
- Reranker `INFERRED`
- Chunker `INFERRED`
- NativeCitationChatModel `INFERRED`
- FailingChatModel `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*