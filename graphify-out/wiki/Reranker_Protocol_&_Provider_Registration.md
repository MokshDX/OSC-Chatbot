# Reranker Protocol & Provider Registration

> 24 nodes · cohesion 0.10

## Key Concepts

- **Reranker** (23 connections) — `src/osc_assistant/protocols.py`
- **cross_encoder.py** (15 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **noop.py** (15 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **CrossEncoderReranker** (7 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **providers/__init__.py** (6 connections) — `src/osc_assistant/providers/__init__.py`
- **.__init__()** (6 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **reranking/__init__.py** (4 connections) — `src/osc_assistant/providers/reranking/__init__.py`
- **CrossEncoderOptions** (3 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **.rerank()** (2 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **A second-stage relevance model applied to retrieval candidates.** (1 connections) — `src/osc_assistant/protocols.py`
- **.model_id()** (1 connections) — `src/osc_assistant/protocols.py`
- **Provider implementations. Importing this package registers every built-in…** (1 connections) — `src/osc_assistant/providers/__init__.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **._score()** (1 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **BaseModel** (1 connections)
- **register** (1 connections)
- **Local cross-encoder reranker. A cross-encoder scores the query and candidate…** (1 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **Adapter over a `sentence-transformers` CrossEncoder.** (1 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **Reranker providers. Imported for registration side effects.** (1 connections) — `src/osc_assistant/providers/reranking/__init__.py`
- **register** (1 connections)
- **Pass-through reranker: the default. Reranking is a real accuracy gain but costs…** (1 connections) — `src/osc_assistant/providers/reranking/noop.py`

## Relationships

- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (11 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (5 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (5 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (4 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (3 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (3 shared connections)
- [Container Lifecycle & E2E](Container_Lifecycle_%26_E2E.md) (2 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (2 shared connections)
- [Noop Reranker & Evaluation Corpus](Noop_Reranker_%26_Evaluation_Corpus.md) (2 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (1 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (1 shared connections)
- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (1 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/__init__.py`
- `src/osc_assistant/providers/reranking/__init__.py`
- `src/osc_assistant/providers/reranking/cross_encoder.py`
- `src/osc_assistant/providers/reranking/noop.py`
- `src/osc_assistant/retrieval/pipeline.py`

## Audit Trail

- EXTRACTED: 97 (92%)
- INFERRED: 9 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*