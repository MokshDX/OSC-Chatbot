# OpenAI-Compatible Embeddings

> 10 nodes

## Key Concepts

- **OpenAICompatibleEmbeddingModel** (12 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **._embed()** (5 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **.embed_documents()** (3 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **Vector** (3 connections)
- **.embed_query()** (3 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **.aclose()** (2 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **.dimensions()** (1 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **Adapter over the `/v1/embeddings` interface.** (1 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **Release the underlying HTTP client. `Container.shutdown()` probes every…** (1 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (2 shared connections)
- [Lifecycle Release Doubles](Lifecycle_Release_Doubles.md) (2 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (2 shared connections)

## Source Files

- `src/osc_assistant/providers/embeddings/openai_compatible.py`

## Audit Trail

- EXTRACTED: 29 (91%)
- INFERRED: 3 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*