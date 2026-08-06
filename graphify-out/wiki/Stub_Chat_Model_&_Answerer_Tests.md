# Stub Chat Model & Answerer Tests

> 26 nodes · cohesion 0.14

## Key Concepts

- **StubChatModel** (40 connections) — `tests/conftest.py`
- **test_answerer.py** (26 connections) — `tests/test_answerer.py`
- **_answerer()** (19 connections) — `tests/test_answerer.py`
- **test_native_citation_provider_needs_no_marker_parsing()** (6 connections) — `tests/test_answerer.py`
- **test_no_retrieval_hits_abstains_without_calling_the_model()** (6 connections) — `tests/test_answerer.py`
- **test_streamed_abstention_is_signalled_on_the_final_event()** (6 connections) — `tests/test_answerer.py`
- **test_citation_requirement_can_be_relaxed()** (5 connections) — `tests/test_answerer.py`
- **test_cited_answer_is_returned_with_its_sources()** (5 connections) — `tests/test_answerer.py`
- **test_sources_are_passed_to_the_model()** (5 connections) — `tests/test_answerer.py`
- **test_stream_abstains_without_a_model_call_when_nothing_is_retrieved()** (5 connections) — `tests/test_answerer.py`
- **test_stream_emits_citations()** (5 connections) — `tests/test_answerer.py`
- **test_stream_emits_sources_before_any_text()** (5 connections) — `tests/test_answerer.py`
- **test_streamed_deltas_reassemble_into_the_final_text()** (5 connections) — `tests/test_answerer.py`
- **test_uncited_answer_is_treated_as_ungrounded()** (5 connections) — `tests/test_answerer.py`
- **test_first_turn_is_not_rewritten()** (4 connections) — `tests/test_retrieval.py`
- **_stub_providers()** (4 connections) — `tests/test_server_lifecycle.py`
- **fixture** (2 connections)
- **A chat model that returns a scripted reply. `supports_citations` is False, so…** (1 connections) — `tests/conftest.py`
- **.__init__()** (1 connections) — `tests/conftest.py`
- **.model_id()** (1 connections) — `tests/conftest.py`
- **.supports_citations()** (1 connections) — `tests/conftest.py`
- **Answer generation tests. The abstention policy is the system's main defence…** (1 connections) — `tests/test_answerer.py`
- **Both citation paths must produce the same shape for downstream code.** (1 connections) — `tests/test_answerer.py`
- **The complete event is authoritative: clients discard streamed text when it…** (1 connections) — `tests/test_answerer.py`
- **Generating from nothing is guessing, so the model is never invoked.** (1 connections) — `tests/test_answerer.py`
- *... and 1 more nodes in this community*

## Relationships

- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (19 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (13 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (7 shared connections)
- [Evaluator & Judge Composition](Evaluator_%26_Judge_Composition.md) (6 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (5 shared connections)
- [Citations & Native Citation Model](Citations_%26_Native_Citation_Model.md) (3 shared connections)
- [Server Lifecycle Tests](Server_Lifecycle_Tests.md) (3 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (3 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (2 shared connections)
- [Golden Set Loading & Evaluation Tests](Golden_Set_Loading_%26_Evaluation_Tests.md) (1 shared connections)
- [Chunker Registration & Options](Chunker_Registration_%26_Options.md) (1 shared connections)

## Source Files

- `tests/conftest.py`
- `tests/test_answerer.py`
- `tests/test_retrieval.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 147 (91%)
- INFERRED: 15 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*