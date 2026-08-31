# Session Memory Architecture

> 23 nodes

## Key Concepts

- **RetrievalSettings** (28 connections) — `src/osc_assistant/settings.py`
- **RetrievalPipeline** (20 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **QueryRewriter** (13 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **retrieval/__init__.py** (9 connections) — `src/osc_assistant/retrieval/__init__.py`
- **test_rewriting_resolves_a_follow_up_question()** (9 connections) — `tests/test_retrieval.py`
- **OSCRetriever()** (6 connections) — `src/osc_assistant/integrations/langchain.py`
- **.__init__()** (6 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **test_min_score_is_applied_before_reranking()** (6 connections) — `tests/test_retrieval.py`
- **test_the_langchain_retriever_refuses_the_synchronous_path()** (5 connections) — `tests/test_langchain_integration.py`
- **._search()** (4 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **._search_store()** (4 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **.__init__()** (2 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **.model_id()** (2 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **Any** (1 connections)
- **Build a LangChain `BaseRetriever` over an OSC retrieval pipeline. A factory…** (1 connections) — `src/osc_assistant/integrations/langchain.py`
- **Retrieval: query rewriting, search and reranking.** (1 connections) — `src/osc_assistant/retrieval/__init__.py`
- **Composes rewriting, search and reranking into one call.** (1 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **Dispatch to the store, timing it and recording the shape of the result. The…** (1 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **Turns a conversational turn into a standalone retrieval query.** (1 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **The model doing the rewriting, for traces and logs.** (1 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **Silently spinning a second event loop would be worse than refusing.** (1 connections) — `tests/test_langchain_integration.py`
- **Regression: the threshold must not be measured against reranker output. A…** (1 connections) — `tests/test_retrieval.py`
- **Tuning for the retrieval stage. Every value here is an experiment knob.** (1 connections) — `src/osc_assistant/settings.py`

## Relationships

- [Evaluation Framework ADR](Evaluation_Framework_ADR.md) (10 shared connections)
- [Evaluation Runner Tests](Evaluation_Runner_Tests.md) (7 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (6 shared connections)
- [Quality Report Renderer](Quality_Report_Renderer.md) (6 shared connections)
- [Document Loaders](Document_Loaders.md) (5 shared connections)
- [Logging System Design](Logging_System_Design.md) (4 shared connections)
- [PgVector Store](PgVector_Store.md) (3 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (3 shared connections)
- [Generation & Abstention Metrics](Generation_%26_Abstention_Metrics.md) (3 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (2 shared connections)
- [Settings Precedence Tests](Settings_Precedence_Tests.md) (2 shared connections)
- [Lifecycle Release Doubles](Lifecycle_Release_Doubles.md) (2 shared connections)

## Source Files

- `src/osc_assistant/integrations/langchain.py`
- `src/osc_assistant/retrieval/__init__.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/retrieval/rewrite.py`
- `src/osc_assistant/settings.py`
- `tests/test_langchain_integration.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 109 (88%)
- INFERRED: 15 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*