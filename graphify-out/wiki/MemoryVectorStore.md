# MemoryVectorStore

> God node · 72 connections · `src/osc_assistant/providers/vectorstores/memory.py`

**Community:** [In-Memory Vector Store](In-Memory_Vector_Store.md)

## Connections by Relation

### calls
- retrieval() `EXTRACTED`
- test_no_retrieval_hits_abstains_without_calling_the_model() `EXTRACTED`
- _build() `EXTRACTED`
- test_stream_abstains_without_a_model_call_when_nothing_is_retrieved() `EXTRACTED`
- test_empty_corpus_returns_no_hits() `EXTRACTED`
- test_both_built_in_stores_offer_inspection() `EXTRACTED`
- test_statistics_on_an_empty_store_do_not_divide_by_zero() `EXTRACTED`

### contains
- memory.py `EXTRACTED`

### method
- .replace_document() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- .search_vector() `EXTRACTED`
- ._summarise() `EXTRACTED`
- .get_document() `EXTRACTED`
- .list_documents() `EXTRACTED`
- .statistics() `EXTRACTED`
- .delete_document() `EXTRACTED`
- .document_chunks() `EXTRACTED`
- .get_chunk() `EXTRACTED`
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
- test_a_document_that_produced_no_chunks_is_still_visible() `EXTRACTED`
- pipeline() `EXTRACTED`
- test_genuinely_removed_documents_are_still_pruned_alongside_failures() `EXTRACTED`
- test_one_bad_document_does_not_abort_the_sync() `EXTRACTED`
- test_unreadable_documents_are_not_pruned() `EXTRACTED`
- indexed() `EXTRACTED`
- test_native_citation_provider_needs_no_marker_parsing() `EXTRACTED`
- test_streamed_abstention_is_signalled_on_the_final_event() `EXTRACTED`
- test_prune_disabled_leaves_other_documents_alone() `EXTRACTED`
- test_min_score_is_applied_before_reranking() `EXTRACTED`
- test_reranker_reorders_the_shortlist() `EXTRACTED`
- test_store_rejects_wrong_width_vectors() `EXTRACTED`
- test_citation_requirement_can_be_relaxed() `EXTRACTED`
- test_cited_answer_is_returned_with_its_sources() `EXTRACTED`
- test_sources_are_passed_to_the_model() `EXTRACTED`

### uses
- [StubEmbeddingModel](StubEmbeddingModel.md) `INFERRED`
- [StubChatModel](StubChatModel.md) `INFERRED`
- FailingChatModel `INFERRED`
- NativeCitationChatModel `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*