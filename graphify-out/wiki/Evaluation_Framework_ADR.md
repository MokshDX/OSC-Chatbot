# Evaluation Framework ADR

> 19 nodes

## Key Concepts

- **test_retrieval.py** (28 connections) — `tests/test_retrieval.py`
- **_pipeline()** (12 connections) — `tests/test_retrieval.py`
- **NoopReranker** (10 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **test_reranker_reorders_the_shortlist()** (6 connections) — `tests/test_retrieval.py`
- **test_every_strategy_finds_the_right_document()** (5 connections) — `tests/test_retrieval.py`
- **test_empty_corpus_returns_no_hits()** (5 connections) — `tests/test_retrieval.py`
- **test_rewrite_failure_falls_back_to_the_original_question()** (5 connections) — `tests/test_retrieval.py`
- **test_hybrid_results_are_marked_as_fused()** (4 connections) — `tests/test_retrieval.py`
- **test_top_k_bounds_the_result_set()** (4 connections) — `tests/test_retrieval.py`
- **test_min_score_filters_weak_hits()** (4 connections) — `tests/test_retrieval.py`
- **test_first_turn_is_not_rewritten()** (4 connections) — `tests/test_retrieval.py`
- **.rerank()** (2 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **Truncates the candidate list without reordering it.** (1 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **parametrize** (1 connections)
- **Retrieval tests, including the vector store contract. `test_store_contract`…** (1 connections) — `tests/test_retrieval.py`
- **This is what triggers abstention rather than a guessed answer.** (1 connections) — `tests/test_retrieval.py`
- **With no history there is nothing to resolve, so no call should be made.** (1 connections) — `tests/test_retrieval.py`
- **A degraded query beats a failed request.** (1 connections) — `tests/test_retrieval.py`

## Relationships

- [Quality Report Renderer](Quality_Report_Renderer.md) (11 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (10 shared connections)
- [Settings Precedence Tests](Settings_Precedence_Tests.md) (9 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (5 shared connections)
- [PgVector Store](PgVector_Store.md) (2 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (2 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (2 shared connections)
- [Default Local Profile](Default_Local_Profile.md) (1 shared connections)
- [LangChain Embedding Bridge](LangChain_Embedding_Bridge.md) (1 shared connections)
- [Logging System Design](Logging_System_Design.md) (1 shared connections)
- [FastAPI Routes & Session Endpoints](FastAPI_Routes_%26_Session_Endpoints.md) (1 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/reranking/noop.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 93 (97%)
- INFERRED: 3 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*