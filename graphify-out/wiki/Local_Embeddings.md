# Local Embeddings

> 8 nodes

## Key Concepts

- **LocalEmbeddingModel** (9 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **Vector** (3 connections)
- **.embed_documents()** (2 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **.embed_query()** (2 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **._encode()** (2 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **.dimensions()** (1 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **Adapter over a `sentence-transformers` model loaded in-process.** (1 connections) — `src/osc_assistant/providers/embeddings/local.py`

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (2 shared connections)
- [ADR 0001 Protocol Seams](ADR_0001_Protocol_Seams.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/embeddings/local.py`

## Audit Trail

- EXTRACTED: 21 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*