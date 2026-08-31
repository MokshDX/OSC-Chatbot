# Gemini Embeddings

> 8 nodes

## Key Concepts

- **GeminiEmbeddingModel** (9 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **._embed()** (5 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **.embed_documents()** (3 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **Vector** (3 connections)
- **.embed_query()** (3 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **.dimensions()** (1 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **Adapter over `google-genai`'s embedding interface.** (1 connections) — `src/osc_assistant/providers/embeddings/gemini.py`

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (2 shared connections)
- [ADR 0001 Protocol Seams](ADR_0001_Protocol_Seams.md) (1 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/embeddings/gemini.py`

## Audit Trail

- EXTRACTED: 26 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*