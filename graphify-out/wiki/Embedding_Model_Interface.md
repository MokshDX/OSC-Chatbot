# Embedding Model Interface

> 45 nodes · cohesion 0.05

## Key Concepts

- **EmbeddingModel** (28 connections) — `src/osc_assistant/protocols.py`
- **VoyageEmbeddingModel** (10 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **GeminiEmbeddingModel** (9 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **LocalEmbeddingModel** (9 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **._embed()** (5 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **._embed()** (5 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **.__init__()** (4 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **.embed_documents()** (3 connections) — `src/osc_assistant/protocols.py`
- **.embed_query()** (3 connections) — `src/osc_assistant/protocols.py`
- **.embed_documents()** (3 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **.embed_query()** (3 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **Vector** (3 connections)
- **Vector** (3 connections)
- **Vector** (3 connections)
- **.embed_documents()** (3 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **.embed_query()** (3 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **VoyageOptions** (3 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **.embeddings()** (2 connections) — `src/osc_assistant/container.py`
- **.dimensions()** (2 connections) — `src/osc_assistant/protocols.py`
- **.embed_documents()** (2 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **.embed_query()** (2 connections) — `src/osc_assistant/providers/embeddings/local.py`
- *... and 20 more nodes in this community*

## Relationships

- [Error Hierarchy](Error_Hierarchy.md) (17 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (3 shared connections)
- [Hybrid Search Scoring](Hybrid_Search_Scoring.md) (3 shared connections)
- [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md) (3 shared connections)
- [Composition Root](Composition_Root.md) (2 shared connections)
- [Chunker Registration](Chunker_Registration.md) (2 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (2 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (2 shared connections)
- [Vector Store Interface](Vector_Store_Interface.md) (1 shared connections)
- [Structured Logging](Structured_Logging.md) (1 shared connections)
- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (1 shared connections)
- [Streaming & Response Types](Streaming_%26_Response_Types.md) (1 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/embeddings/gemini.py`
- `src/osc_assistant/providers/embeddings/local.py`
- `src/osc_assistant/providers/embeddings/voyage.py`

## Audit Trail

- EXTRACTED: 140 (95%)
- INFERRED: 7 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*