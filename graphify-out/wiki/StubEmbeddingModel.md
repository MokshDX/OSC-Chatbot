# StubEmbeddingModel

> God node · 69 connections · `tests/conftest.py`

**Community:** [Stub Embedding Model](Stub_Embedding_Model.md)

## Connections by Relation

### calls
- [_stub_environment()](_stub_environment%28%29.md) `EXTRACTED`
- _register_stub_providers() `EXTRACTED`
- [_stub_providers()](_stub_providers%28%29.md) `EXTRACTED`

### contains
- [conftest.py](conftest.py.md) `EXTRACTED`

### imports
- test_evaluation.py `EXTRACTED`
- test_cli.py `EXTRACTED`
- test_api.py `EXTRACTED`
- test_server_lifecycle.py `EXTRACTED`
- test_retrieval.py `EXTRACTED`
- test_answerer.py `EXTRACTED`
- test_pgvector_integration.py `EXTRACTED`
- test_ingestion.py `EXTRACTED`

### method
- ._encode() `EXTRACTED`
- .embed_documents() `EXTRACTED`
- .embed_query() `EXTRACTED`
- .dimensions() `EXTRACTED`
- .__init__() `EXTRACTED`
- .model_id() `EXTRACTED`

### rationale_for
- A deterministic bag-of-words embedder. Hashes each token into a fixed number of… `EXTRACTED`

### references
- _answerer() `EXTRACTED`
- retrieval() `EXTRACTED`
- _pipeline() `EXTRACTED`
- indexed() `EXTRACTED`
- indexed() `EXTRACTED`
- test_rewriting_resolves_a_follow_up_question() `EXTRACTED`
- pipeline() `EXTRACTED`
- populated() `EXTRACTED`
- test_failed_replace_leaves_no_hash_without_chunks() `EXTRACTED`
- test_replace_document_supersedes_the_old_chunks() `EXTRACTED`
- test_native_citation_provider_needs_no_marker_parsing() `EXTRACTED`
- test_no_retrieval_hits_abstains_without_calling_the_model() `EXTRACTED`
- test_streamed_abstention_is_signalled_on_the_final_event() `EXTRACTED`
- test_reindex_forces_work_the_content_hash_says_is_unnecessary() `EXTRACTED`
- test_min_score_is_applied_before_reranking() `EXTRACTED`
- test_reranker_reorders_the_shortlist() `EXTRACTED`
- test_citation_requirement_can_be_relaxed() `EXTRACTED`
- test_cited_answer_is_returned_with_its_sources() `EXTRACTED`
- test_sources_are_passed_to_the_model() `EXTRACTED`
- test_stream_abstains_without_a_model_call_when_nothing_is_retrieved() `EXTRACTED`

### uses
- [MemoryVectorStore](MemoryVectorStore.md) `INFERRED`
- [Document](Document.md) `INFERRED`
- [ChatRequest](ChatRequest.md) `INFERRED`
- Usage `INFERRED`
- ChatResponse `INFERRED`
- TextDelta `INFERRED`
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- _ClosableEmbedding `INFERRED`
- CitationDelta `INFERRED`
- StreamEnd `INFERRED`
- Citation `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*