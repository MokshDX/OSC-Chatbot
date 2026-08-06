# Noop Reranker & Evaluation Corpus

> 8 nodes · cohesion 0.25

## Key Concepts

- **retrieval()** (12 connections) — `tests/test_evaluation.py`
- **NoopReranker** (11 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **corpus()** (4 connections) — `tests/test_evaluation.py`
- **.rerank()** (2 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **fixture** (2 connections)
- **.model_id()** (1 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **Truncates the candidate list without reordering it.** (1 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **A three-document corpus with `relative_path` set, as the loader would.** (1 connections) — `tests/test_evaluation.py`

## Relationships

- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (5 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (3 shared connections)
- [Reranker Protocol & Provider Registration](Reranker_Protocol_%26_Provider_Registration.md) (2 shared connections)
- [Golden Set Loading & Evaluation Tests](Golden_Set_Loading_%26_Evaluation_Tests.md) (2 shared connections)
- [Chunker Registration & Options](Chunker_Registration_%26_Options.md) (2 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (1 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (1 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (1 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (1 shared connections)
- [Evaluator & Judge Composition](Evaluator_%26_Judge_Composition.md) (1 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/reranking/noop.py`
- `tests/test_evaluation.py`

## Audit Trail

- EXTRACTED: 29 (85%)
- INFERRED: 5 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*