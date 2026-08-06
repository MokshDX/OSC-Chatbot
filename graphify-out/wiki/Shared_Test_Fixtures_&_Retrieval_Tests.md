# Shared Test Fixtures & Retrieval Tests

> 29 nodes · cohesion 0.13

## Key Concepts

- **StubEmbeddingModel** (65 connections) — `tests/conftest.py`
- **test_retrieval.py** (28 connections) — `tests/test_retrieval.py`
- **conftest.py** (21 connections) — `tests/conftest.py`
- **_pipeline()** (12 connections) — `tests/test_retrieval.py`
- **test_rewriting_resolves_a_follow_up_question()** (9 connections) — `tests/test_retrieval.py`
- **test_min_score_is_applied_before_reranking()** (6 connections) — `tests/test_retrieval.py`
- **test_reranker_reorders_the_shortlist()** (6 connections) — `tests/test_retrieval.py`
- **test_empty_corpus_returns_no_hits()** (5 connections) — `tests/test_retrieval.py`
- **test_every_strategy_finds_the_right_document()** (5 connections) — `tests/test_retrieval.py`
- **fixture** (4 connections)
- **._encode()** (4 connections) — `tests/conftest.py`
- **test_hybrid_results_are_marked_as_fused()** (4 connections) — `tests/test_retrieval.py`
- **test_min_score_filters_weak_hits()** (4 connections) — `tests/test_retrieval.py`
- **test_top_k_bounds_the_result_set()** (4 connections) — `tests/test_retrieval.py`
- **documents()** (3 connections) — `tests/conftest.py`
- **embeddings()** (3 connections) — `tests/conftest.py`
- **Vector** (3 connections)
- **store()** (3 connections) — `tests/conftest.py`
- **.embed_documents()** (3 connections) — `tests/conftest.py`
- **.embed_query()** (3 connections) — `tests/conftest.py`
- **Shared test fixtures and in-process test doubles. The doubles are deliberately…** (1 connections) — `tests/conftest.py`
- **A deterministic bag-of-words embedder. Hashes each token into a fixed number of…** (1 connections) — `tests/conftest.py`
- **.dimensions()** (1 connections) — `tests/conftest.py`
- **.__init__()** (1 connections) — `tests/conftest.py`
- **.model_id()** (1 connections) — `tests/conftest.py`
- *... and 4 more nodes in this community*

## Relationships

- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (19 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (13 shared connections)
- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (12 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (9 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (7 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (7 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (6 shared connections)
- [Evaluator & Judge Composition](Evaluator_%26_Judge_Composition.md) (4 shared connections)
- [Noop Reranker & Evaluation Corpus](Noop_Reranker_%26_Evaluation_Corpus.md) (3 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (2 shared connections)
- [Observability Installation & Isolation](Observability_Installation_%26_Isolation.md) (2 shared connections)
- [Citations & Native Citation Model](Citations_%26_Native_Citation_Model.md) (2 shared connections)

## Source Files

- `tests/conftest.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 191 (94%)
- INFERRED: 13 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*