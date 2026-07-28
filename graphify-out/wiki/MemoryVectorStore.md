# MemoryVectorStore

> God node · 50 connections · `src/osc_assistant/providers/vectorstores/memory.py`

**Community:** [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md)

## Connections by Relation

### calls
- test_no_retrieval_hits_abstains_without_calling_the_model() `EXTRACTED`
- _build() `EXTRACTED`
- test_stream_abstains_without_a_model_call_when_nothing_is_retrieved() `EXTRACTED`
- test_empty_corpus_returns_no_hits() `EXTRACTED`

### contains
- memory.py `EXTRACTED`

### method
- .replace_document() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .delete_document() `EXTRACTED`
- .close() `EXTRACTED`
- .dimensions() `EXTRACTED`
- .document_ids() `EXTRACTED`
- .__init__() `EXTRACTED`
- .list_document_hashes() `EXTRACTED`
- .setup() `EXTRACTED`

### rationale_for
- A dictionary-backed `VectorStore`. `EXTRACTED`

### references
- _answerer() `EXTRACTED`
- _pipeline() `EXTRACTED`
- indexed() `EXTRACTED`
- indexed() `EXTRACTED`
- test_rewriting_resolves_a_follow_up_question() `EXTRACTED`
- pipeline() `EXTRACTED`
- test_one_bad_document_does_not_abort_the_sync() `EXTRACTED`
- test_native_citation_provider_needs_no_marker_parsing() `EXTRACTED`
- test_streamed_abstention_is_signalled_on_the_final_event() `EXTRACTED`
- test_prune_disabled_leaves_other_documents_alone() `EXTRACTED`
- test_reranker_reorders_the_shortlist() `EXTRACTED`
- test_store_rejects_wrong_width_vectors() `EXTRACTED`
- test_citation_requirement_can_be_relaxed() `EXTRACTED`
- test_cited_answer_is_returned_with_its_sources() `EXTRACTED`
- test_sources_are_passed_to_the_model() `EXTRACTED`
- test_stream_emits_citations() `EXTRACTED`
- test_stream_emits_sources_before_any_text() `EXTRACTED`
- test_streamed_deltas_reassemble_into_the_final_text() `EXTRACTED`
- test_uncited_answer_is_treated_as_ungrounded() `EXTRACTED`
- test_documents_are_indexed() `EXTRACTED`

### uses
- [StubEmbeddingModel](StubEmbeddingModel.md) `INFERRED`
- [StubChatModel](StubChatModel.md) `INFERRED`
- NativeCitationChatModel `INFERRED`
- FailingChatModel `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*