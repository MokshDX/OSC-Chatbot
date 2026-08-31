# Document

> God node · 54 connections · `src/osc_assistant/types.py`

**Community:** [Conversational Evaluator](Conversational_Evaluator.md)

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
- pgvector.py `EXTRACTED`
- memory.py `EXTRACTED`
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
- ._read() `EXTRACTED`
- .ingest() `EXTRACTED`
- indexed() `EXTRACTED`
- indexed() `EXTRACTED`
- test_a_populated_index_produces_no_note() `EXTRACTED`
- exploding_client() `EXTRACTED`
- test_a_known_provider_failure_keeps_its_actionable_message() `EXTRACTED`
- .split() `EXTRACTED`
- .split() `EXTRACTED`
- .replace_document() `EXTRACTED`
- .replace_document() `EXTRACTED`
- .split() `EXTRACTED`
- ._index() `EXTRACTED`
- ._summarise() `EXTRACTED`
- .split() `EXTRACTED`
- .replace_document() `EXTRACTED`
- .split() `EXTRACTED`
- .load() `EXTRACTED`
- documents() `EXTRACTED`

### uses
- [StubEmbeddingModel](StubEmbeddingModel.md) `INFERRED`
- StubChatModel `INFERRED`
- EmbeddingModel `INFERRED`
- VectorStore `INFERRED`
- ChatModel `INFERRED`
- _FakeEmbeddings `INFERRED`
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- Chunker `INFERRED`
- _ClosableEmbedding `INFERRED`
- Reranker `INFERRED`
- NativeCitationChatModel `INFERRED`
- FailingChatModel `INFERRED`
- StoreInspector `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*