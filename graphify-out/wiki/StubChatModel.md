# StubChatModel

> God node · 44 connections · `tests/conftest.py`

**Community:** [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md)

## Connections by Relation

### calls
- test_a_judge_failure_records_no_verdict_rather_than_a_wrong_one() `EXTRACTED`
- test_rewriting_resolves_a_follow_up_question() `EXTRACTED`
- test_the_judge_sees_the_passages_the_answer_was_built_from() `EXTRACTED`
- [_stub_environment()](_stub_environment%28%29.md) `EXTRACTED`
- test_a_generation_run_scores_citations_against_what_was_retrieved() `EXTRACTED`
- test_a_missing_expected_fact_is_named_not_just_counted() `EXTRACTED`
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
- [test_first_turn_is_not_rewritten()](test_first_turn_is_not_rewritten%28%29.md) `EXTRACTED`
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
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- _ClosableEmbedding `INFERRED`
- CitationDelta `INFERRED`
- StreamEnd `INFERRED`
- Citation `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*