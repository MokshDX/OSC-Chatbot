# StubChatModel

> God node · 32 connections · `tests/conftest.py`

**Community:** [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md)

## Connections by Relation

### calls
- test_rewriting_resolves_a_follow_up_question() `EXTRACTED`
- test_no_retrieval_hits_abstains_without_calling_the_model() `EXTRACTED`
- test_streamed_abstention_is_signalled_on_the_final_event() `EXTRACTED`
- test_citation_requirement_can_be_relaxed() `EXTRACTED`
- test_cited_answer_is_returned_with_its_sources() `EXTRACTED`
- test_sources_are_passed_to_the_model() `EXTRACTED`
- test_stream_abstains_without_a_model_call_when_nothing_is_retrieved() `EXTRACTED`
- test_stream_emits_citations() `EXTRACTED`
- test_stream_emits_sources_before_any_text() `EXTRACTED`
- test_streamed_deltas_reassemble_into_the_final_text() `EXTRACTED`
- test_uncited_answer_is_treated_as_ungrounded() `EXTRACTED`
- _register_stub_providers() `EXTRACTED`
- test_first_turn_is_not_rewritten() `EXTRACTED`

### contains
- conftest.py `EXTRACTED`

### imports
- test_retrieval.py `EXTRACTED`
- test_answerer.py `EXTRACTED`
- test_api.py `EXTRACTED`

### method
- .stream() `EXTRACTED`
- .complete() `EXTRACTED`
- .__init__() `EXTRACTED`
- .model_id() `EXTRACTED`
- .supports_citations() `EXTRACTED`

### rationale_for
- A chat model that returns a scripted reply. `supports_citations` is False, so… `EXTRACTED`

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