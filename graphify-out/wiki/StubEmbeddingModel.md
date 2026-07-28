# StubEmbeddingModel

> God node · 57 connections · `tests/conftest.py`

**Community:** [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md)

## Connections by Relation

### calls
- _register_stub_providers() `EXTRACTED`

### contains
- conftest.py `EXTRACTED`

### imports
- test_retrieval.py `EXTRACTED`
- test_answerer.py `EXTRACTED`
- test_api.py `EXTRACTED`
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
- [Document](Document.md) `INFERRED`
- [ChatRequest](ChatRequest.md) `INFERRED`
- Usage `INFERRED`
- ChatResponse `INFERRED`
- TextDelta `INFERRED`
- CitationDelta `INFERRED`
- Citation `INFERRED`
- StreamEnd `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*