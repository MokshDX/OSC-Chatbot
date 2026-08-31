# Quality Report Renderer

> 27 nodes

## Key Concepts

- **StubEmbeddingModel** (59 connections) — `tests/conftest.py`
- **StubChatModel** (35 connections) — `tests/conftest.py`
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
- **.dimensions()** (1 connections) — `tests/conftest.py`
- **.__init__()** (1 connections) — `tests/conftest.py`
- **.model_id()** (1 connections) — `tests/conftest.py`
- **.supports_citations()** (1 connections) — `tests/conftest.py`
- **A deterministic bag-of-words embedder. Hashes each token into a fixed number of…** (1 connections) — `tests/conftest.py`
- **A chat model that returns a scripted reply. `supports_citations` is False, so…** (1 connections) — `tests/conftest.py`
- **Answer generation tests. The abstention policy is the system's main defence…** (1 connections) — `tests/test_answerer.py`
- **Generating from nothing is guessing, so the model is never invoked.** (1 connections) — `tests/test_answerer.py`
- *... and 2 more nodes in this community*

## Relationships

- [Recursive Chunker](Recursive_Chunker.md) (16 shared connections)
- [Settings Precedence Tests](Settings_Precedence_Tests.md) (14 shared connections)
- [Protocol Seams & Container](Protocol_Seams_%26_Container.md) (11 shared connections)
- [Evaluation Framework ADR](Evaluation_Framework_ADR.md) (11 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (6 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (4 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (4 shared connections)
- [Evaluation Framework Rationale](Evaluation_Framework_Rationale.md) (4 shared connections)
- [Lifecycle Release Doubles](Lifecycle_Release_Doubles.md) (4 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (3 shared connections)
- [Stub Embedding Encoding](Stub_Embedding_Encoding.md) (3 shared connections)
- [PgVector Store](PgVector_Store.md) (3 shared connections)

## Source Files

- `tests/conftest.py`
- `tests/test_answerer.py`

## Audit Trail

- EXTRACTED: 183 (88%)
- INFERRED: 26 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*