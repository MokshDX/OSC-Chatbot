# Stub Embedding Model

> 24 nodes

## Key Concepts

- **StubEmbeddingModel** (69 connections) — `tests/conftest.py`
- **test_retrieval.py** (28 connections) — `tests/test_retrieval.py`
- **_pipeline()** (12 connections) — `tests/test_retrieval.py`
- **test_min_score_is_applied_before_reranking()** (6 connections) — `tests/test_retrieval.py`
- **test_reranker_reorders_the_shortlist()** (6 connections) — `tests/test_retrieval.py`
- **test_every_strategy_finds_the_right_document()** (5 connections) — `tests/test_retrieval.py`
- **test_empty_corpus_returns_no_hits()** (5 connections) — `tests/test_retrieval.py`
- **._encode()** (4 connections) — `tests/conftest.py`
- **test_hybrid_results_are_marked_as_fused()** (4 connections) — `tests/test_retrieval.py`
- **test_top_k_bounds_the_result_set()** (4 connections) — `tests/test_retrieval.py`
- **test_min_score_filters_weak_hits()** (4 connections) — `tests/test_retrieval.py`
- **.embed_documents()** (3 connections) — `tests/conftest.py`
- **Vector** (3 connections)
- **.embed_query()** (3 connections) — `tests/conftest.py`
- **test_deleting_a_document_removes_its_chunks()** (2 connections) — `tests/test_retrieval.py`
- **test_hashes_are_recorded_for_incremental_sync()** (2 connections) — `tests/test_retrieval.py`
- **.__init__()** (1 connections) — `tests/conftest.py`
- **.model_id()** (1 connections) — `tests/conftest.py`
- **.dimensions()** (1 connections) — `tests/conftest.py`
- **A deterministic bag-of-words embedder. Hashes each token into a fixed number of…** (1 connections) — `tests/conftest.py`
- **parametrize** (1 connections)
- **Retrieval tests, including the vector store contract. `test_store_contract`…** (1 connections) — `tests/test_retrieval.py`
- **Regression: the threshold must not be measured against reranker output. A…** (1 connections) — `tests/test_retrieval.py`
- **This is what triggers abstention rather than a guessed answer.** (1 connections) — `tests/test_retrieval.py`

## Relationships

- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (14 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (11 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (9 shared connections)
- [pgvector Store Interface](pgvector_Store_Interface.md) (8 shared connections)
- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (7 shared connections)
- [Settings Schema](Settings_Schema.md) (6 shared connections)
- [conftest.py](conftest.py.md) (3 shared connections)
- [EmbeddedChunk](EmbeddedChunk.md) (3 shared connections)
- [NoopReranker](NoopReranker.md) (3 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (3 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (2 shared connections)
- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (2 shared connections)

## Source Files

- `tests/conftest.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 156 (93%)
- INFERRED: 12 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*