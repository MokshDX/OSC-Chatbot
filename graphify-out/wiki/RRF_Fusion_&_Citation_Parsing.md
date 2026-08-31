# RRF Fusion & Citation Parsing

> 38 nodes

## Key Concepts

- **Container** (64 connections) — `src/osc_assistant/container.py`
- **.shutdown()** (4 connections) — `src/osc_assistant/container.py`
- **_inspector()** (3 connections) — `src/osc_assistant/cli/diagnose.py`
- **.vector_store()** (3 connections) — `src/osc_assistant/container.py`
- **.fast_llm()** (3 connections) — `src/osc_assistant/container.py`
- **.__aenter__()** (3 connections) — `src/osc_assistant/container.py`
- **test_a_corpus_of_six_formats_indexes()** (3 connections) — `tests/test_e2e.py`
- **test_a_question_the_corpus_cannot_answer_is_declined()** (3 connections) — `tests/test_e2e.py`
- **test_a_binary_format_is_answerable()** (3 connections) — `tests/test_e2e.py`
- **test_the_run_is_fully_traced()** (3 connections) — `tests/test_e2e.py`
- **.__init__()** (2 connections) — `src/osc_assistant/container.py`
- **.embeddings()** (2 connections) — `src/osc_assistant/container.py`
- **.chunker()** (2 connections) — `src/osc_assistant/container.py`
- **.llm()** (2 connections) — `src/osc_assistant/container.py`
- **ChatModel** (2 connections)
- **.reranker()** (2 connections) — `src/osc_assistant/container.py`
- **.retrieval()** (2 connections) — `src/osc_assistant/container.py`
- **.answerer()** (2 connections) — `src/osc_assistant/container.py`
- **.ingestion()** (2 connections) — `src/osc_assistant/container.py`
- **.startup()** (2 connections) — `src/osc_assistant/container.py`
- **.__aexit__()** (2 connections) — `src/osc_assistant/container.py`
- **Self** (1 connections)
- **StoreInspector** (1 connections)
- **EmbeddingModel** (1 connections)
- **VectorStore** (1 connections)
- *... and 13 more nodes in this community*

## Relationships

- [PgVector SQL & Inspection](PgVector_SQL_%26_Inspection.md) (14 shared connections)
- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (9 shared connections)
- [Evaluation Framework Rationale](Evaluation_Framework_Rationale.md) (6 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (5 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (4 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (3 shared connections)
- [Lifecycle Release Doubles](Lifecycle_Release_Doubles.md) (2 shared connections)
- [StoreInspector Protocol](StoreInspector_Protocol.md) (2 shared connections)
- [SessionStore Seam](SessionStore_Seam.md) (2 shared connections)
- [PgVector Store](PgVector_Store.md) (1 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (1 shared connections)
- [Core CLI Commands](Core_CLI_Commands.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/diagnose.py`
- `src/osc_assistant/container.py`
- `tests/test_e2e.py`

## Audit Trail

- EXTRACTED: 124 (95%)
- INFERRED: 7 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*