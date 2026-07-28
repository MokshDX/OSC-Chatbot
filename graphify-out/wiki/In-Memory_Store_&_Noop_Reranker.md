# In-Memory Store & Noop Reranker

> 68 nodes · cohesion 0.07

## Key Concepts

- **StubEmbeddingModel** (57 connections) — `tests/conftest.py`
- **MemoryVectorStore** (50 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **StubChatModel** (32 connections) — `tests/conftest.py`
- **test_retrieval.py** (27 connections) — `tests/test_retrieval.py`
- **test_answerer.py** (26 connections) — `tests/test_answerer.py`
- **_answerer()** (19 connections) — `tests/test_answerer.py`
- **conftest.py** (15 connections) — `tests/conftest.py`
- **_pipeline()** (12 connections) — `tests/test_retrieval.py`
- **test_rewriting_resolves_a_follow_up_question()** (9 connections) — `tests/test_retrieval.py`
- **NoopReranker** (8 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **.replace_document()** (6 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **test_native_citation_provider_needs_no_marker_parsing()** (6 connections) — `tests/test_answerer.py`
- **test_no_retrieval_hits_abstains_without_calling_the_model()** (6 connections) — `tests/test_answerer.py`
- **test_streamed_abstention_is_signalled_on_the_final_event()** (6 connections) — `tests/test_answerer.py`
- **test_reranker_reorders_the_shortlist()** (6 connections) — `tests/test_retrieval.py`
- **test_citation_requirement_can_be_relaxed()** (5 connections) — `tests/test_answerer.py`
- **test_cited_answer_is_returned_with_its_sources()** (5 connections) — `tests/test_answerer.py`
- **test_sources_are_passed_to_the_model()** (5 connections) — `tests/test_answerer.py`
- **test_stream_abstains_without_a_model_call_when_nothing_is_retrieved()** (5 connections) — `tests/test_answerer.py`
- **test_stream_emits_citations()** (5 connections) — `tests/test_answerer.py`
- **test_stream_emits_sources_before_any_text()** (5 connections) — `tests/test_answerer.py`
- **test_streamed_deltas_reassemble_into_the_final_text()** (5 connections) — `tests/test_answerer.py`
- **test_uncited_answer_is_treated_as_ungrounded()** (5 connections) — `tests/test_answerer.py`
- **test_empty_corpus_returns_no_hits()** (5 connections) — `tests/test_retrieval.py`
- **test_every_strategy_finds_the_right_document()** (5 connections) — `tests/test_retrieval.py`
- *... and 43 more nodes in this community*

## Relationships

- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (22 shared connections)
- [Streaming & Response Types](Streaming_%26_Response_Types.md) (21 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (12 shared connections)
- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (10 shared connections)
- [Settings Schema](Settings_Schema.md) (7 shared connections)
- [Dimension Guard & Match Source](Dimension_Guard_%26_Match_Source.md) (6 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (5 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (4 shared connections)
- [Hybrid Search Scoring](Hybrid_Search_Scoring.md) (4 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (4 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (4 shared connections)
- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (2 shared connections)

## Source Files

- `src/osc_assistant/providers/reranking/noop.py`
- `src/osc_assistant/providers/vectorstores/memory.py`
- `tests/conftest.py`
- `tests/test_answerer.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 385 (94%)
- INFERRED: 26 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*