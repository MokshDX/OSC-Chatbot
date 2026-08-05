# Stub Chat Model & Answerer Tests

> 22 nodes

## Key Concepts

- **StubChatModel** (44 connections) — `tests/conftest.py`
- **test_answerer.py** (26 connections) — `tests/test_answerer.py`
- **_answerer()** (19 connections) — `tests/test_answerer.py`
- **test_no_retrieval_hits_abstains_without_calling_the_model()** (6 connections) — `tests/test_answerer.py`
- **test_native_citation_provider_needs_no_marker_parsing()** (6 connections) — `tests/test_answerer.py`
- **test_streamed_abstention_is_signalled_on_the_final_event()** (6 connections) — `tests/test_answerer.py`
- **test_cited_answer_is_returned_with_its_sources()** (5 connections) — `tests/test_answerer.py`
- **test_sources_are_passed_to_the_model()** (5 connections) — `tests/test_answerer.py`
- **test_uncited_answer_is_treated_as_ungrounded()** (5 connections) — `tests/test_answerer.py`
- **test_citation_requirement_can_be_relaxed()** (5 connections) — `tests/test_answerer.py`
- **test_stream_emits_sources_before_any_text()** (5 connections) — `tests/test_answerer.py`
- **test_streamed_deltas_reassemble_into_the_final_text()** (5 connections) — `tests/test_answerer.py`
- **test_stream_emits_citations()** (5 connections) — `tests/test_answerer.py`
- **test_stream_abstains_without_a_model_call_when_nothing_is_retrieved()** (5 connections) — `tests/test_answerer.py`
- **.__init__()** (1 connections) — `tests/conftest.py`
- **.model_id()** (1 connections) — `tests/conftest.py`
- **.supports_citations()** (1 connections) — `tests/conftest.py`
- **A chat model that returns a scripted reply. `supports_citations` is False, so…** (1 connections) — `tests/conftest.py`
- **Answer generation tests. The abstention policy is the system's main defence…** (1 connections) — `tests/test_answerer.py`
- **Generating from nothing is guessing, so the model is never invoked.** (1 connections) — `tests/test_answerer.py`
- **Both citation paths must produce the same shape for downstream code.** (1 connections) — `tests/test_answerer.py`
- **The complete event is authoritative: clients discard streamed text when it…** (1 connections) — `tests/test_answerer.py`

## Relationships

- [Stub Embedding Model](Stub_Embedding_Model.md) (14 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (13 shared connections)
- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (9 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (6 shared connections)
- [Settings Schema](Settings_Schema.md) (5 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (2 shared connections)
- [conftest.py](conftest.py.md) (2 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (2 shared connections)
- [NoopReranker](NoopReranker.md) (2 shared connections)
- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (2 shared connections)
- [CLI Tests](CLI_Tests.md) (1 shared connections)

## Source Files

- `tests/conftest.py`
- `tests/test_answerer.py`

## Audit Trail

- EXTRACTED: 141 (91%)
- INFERRED: 14 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*