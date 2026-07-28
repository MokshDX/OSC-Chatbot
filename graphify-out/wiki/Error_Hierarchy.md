# Error Hierarchy

> 40 nodes · cohesion 0.09

## Key Concepts

- **types.py** (48 connections) — `src/osc_assistant/types.py`
- **protocols.py** (31 connections) — `src/osc_assistant/protocols.py`
- **answerer.py** (25 connections) — `src/osc_assistant/generation/answerer.py`
- **errors.py** (22 connections) — `src/osc_assistant/errors.py`
- **ConfigurationError** (21 connections) — `src/osc_assistant/errors.py`
- **ProviderError** (20 connections) — `src/osc_assistant/errors.py`
- **MissingDependencyError** (18 connections) — `src/osc_assistant/errors.py`
- **embeddings/gemini.py** (15 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **embeddings/openai_compatible.py** (15 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **local.py** (14 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **voyage.py** (14 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **AssistantError** (7 connections) — `src/osc_assistant/errors.py`
- **Role** (7 connections) — `src/osc_assistant/types.py`
- **embeddings/__init__.py** (6 connections) — `src/osc_assistant/providers/embeddings/__init__.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **GeminiEmbeddingOptions** (3 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **LocalEmbeddingOptions** (3 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **OpenAIEmbeddingOptions** (3 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **_make_factory()** (2 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **Exception** (1 connections)
- **Exception hierarchy for the assistant. A single root (`AssistantError`) lets…** (1 connections) — `src/osc_assistant/errors.py`
- **Base class for every error raised by this package.** (1 connections) — `src/osc_assistant/errors.py`
- *... and 15 more nodes in this community*

## Relationships

- [Embedding Model Interface](Embedding_Model_Interface.md) (17 shared connections)
- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (16 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (16 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (13 shared connections)
- [Streaming & Response Types](Streaming_%26_Response_Types.md) (13 shared connections)
- [Dimension Guard & Match Source](Dimension_Guard_%26_Match_Source.md) (8 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (8 shared connections)
- [OpenAI-Compatible Chat Adapter](OpenAI-Compatible_Chat_Adapter.md) (8 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (7 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (7 shared connections)
- [pgvector Setup & Codecs](pgvector_Setup_%26_Codecs.md) (6 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (5 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/generation/answerer.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/embeddings/__init__.py`
- `src/osc_assistant/providers/embeddings/gemini.py`
- `src/osc_assistant/providers/embeddings/local.py`
- `src/osc_assistant/providers/embeddings/openai_compatible.py`
- `src/osc_assistant/providers/embeddings/voyage.py`
- `src/osc_assistant/providers/llm/gemini.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 308 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*