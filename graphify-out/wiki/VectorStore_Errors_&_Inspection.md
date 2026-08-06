# VectorStore Errors & Inspection

> 22 nodes · cohesion 0.12

## Key Concepts

- **pgvector.py** (30 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **DocumentSummary** (21 connections) — `src/osc_assistant/types.py`
- **VectorStoreError** (6 connections) — `src/osc_assistant/errors.py`
- **.setup()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **._summarise()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_to_document_summary()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.get_document()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.list_documents()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_register_codecs()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.get_document()** (3 connections) — `src/osc_assistant/protocols.py`
- **.list_documents()** (3 connections) — `src/osc_assistant/protocols.py`
- **.get_document()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.list_documents()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_redact_dsn()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **The vector store could not complete an operation.** (1 connections) — `src/osc_assistant/errors.py`
- **Indexed documents, newest first. `search` matches title or source URI.** (1 connections) — `src/osc_assistant/protocols.py`
- **One document's index record, or None if it is not indexed.** (1 connections) — `src/osc_assistant/protocols.py`
- **PostgreSQL + pgvector store: the production default. One datastore holds chunk…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Open the pool and, unless disabled, apply pending migrations.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Decode JSONB into Python objects instead of raw strings.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Strip the password from a DSN before it reaches a terminal or a log. Connection…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **What the store knows about one indexed document. Distinct from `Document`: it…** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (8 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (7 shared connections)
- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (7 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (4 shared connections)
- [Trace Listing CLI](Trace_Listing_CLI.md) (3 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (3 shared connections)
- [Store Construction & Embedding Calls](Store_Construction_%26_Embedding_Calls.md) (3 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (3 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (2 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (2 shared connections)
- [Whitespace Normalisation & Error Base](Whitespace_Normalisation_%26_Error_Base.md) (1 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/vectorstores/memory.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 100 (93%)
- INFERRED: 8 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*