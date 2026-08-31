# StubEmbeddingModel

> God node · 59 connections · `tests/conftest.py`

**Community:** [Quality Report Renderer](Quality_Report_Renderer.md)

## Connections by Relation

### calls
- _stub_providers() `EXTRACTED`

### contains
- conftest.py `EXTRACTED`

### imports
- test_server_lifecycle.py `EXTRACTED`
- test_retrieval.py `EXTRACTED`
- test_answerer.py `EXTRACTED`
- test_pgvector_integration.py `EXTRACTED`

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
- _pipeline() `EXTRACTED`
- indexed() `EXTRACTED`
- indexed() `EXTRACTED`
- test_rewriting_resolves_a_follow_up_question() `EXTRACTED`
- populated() `EXTRACTED`
- test_failed_replace_leaves_no_hash_without_chunks() `EXTRACTED`
- test_replace_document_supersedes_the_old_chunks() `EXTRACTED`
- test_native_citation_provider_needs_no_marker_parsing() `EXTRACTED`
- test_no_retrieval_hits_abstains_without_calling_the_model() `EXTRACTED`
- test_streamed_abstention_is_signalled_on_the_final_event() `EXTRACTED`
- test_min_score_is_applied_before_reranking() `EXTRACTED`
- test_reranker_reorders_the_shortlist() `EXTRACTED`
- test_citation_requirement_can_be_relaxed() `EXTRACTED`
- test_cited_answer_is_returned_with_its_sources() `EXTRACTED`
- test_sources_are_passed_to_the_model() `EXTRACTED`
- test_stream_abstains_without_a_model_call_when_nothing_is_retrieved() `EXTRACTED`
- test_stream_emits_citations() `EXTRACTED`
- test_stream_emits_sources_before_any_text() `EXTRACTED`
- test_streamed_deltas_reassemble_into_the_final_text() `EXTRACTED`

### uses
- [MemoryVectorStore](MemoryVectorStore.md) `INFERRED`
- [ChatRequest](ChatRequest.md) `INFERRED`
- [Document](Document.md) `INFERRED`
- Usage `INFERRED`
- ChatResponse `INFERRED`
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- TextDelta `INFERRED`
- _ClosableEmbedding `INFERRED`
- CitationDelta `INFERRED`
- StreamEnd `INFERRED`
- Citation `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*