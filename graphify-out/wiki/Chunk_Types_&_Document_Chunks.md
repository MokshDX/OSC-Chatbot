# Chunk Types & Document Chunks

> 20 nodes · cohesion 0.13

## Key Concepts

- **Chunk** (34 connections) — `src/osc_assistant/types.py`
- **._acquire()** (16 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **._migrate()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_to_chunk()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_store_rejects_wrong_width_vectors()** (6 connections) — `tests/test_retrieval.py`
- **._assert_dimensions_match()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Any** (5 connections)
- **.split()** (4 connections) — `src/osc_assistant/protocols.py`
- **.document_chunks()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.get_chunk()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.document_chunks()** (3 connections) — `src/osc_assistant/protocols.py`
- **.get_chunk()** (3 connections) — `src/osc_assistant/protocols.py`
- **.delete_document()** (2 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Every chunk of a document, in ordinal order.** (1 connections) — `src/osc_assistant/protocols.py`
- **One chunk with its full text — what the model was actually shown.** (1 connections) — `src/osc_assistant/protocols.py`
- **Split `document`. Chunk ids must be stable across runs for the same input.** (1 connections) — `src/osc_assistant/protocols.py`
- **Apply unapplied migration files in filename order. A hand-rolled runner rather…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Fail loudly if the stored vector width disagrees with the active model.…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **A retrievable span of a document. `title` and `source_uri` are denormalised…** (1 connections) — `src/osc_assistant/types.py`
- **Mixing vector widths silently produces nonsense scores; it must raise.** (1 connections) — `tests/test_retrieval.py`

## Relationships

- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (12 shared connections)
- [VectorStore Errors & Inspection](VectorStore_Errors_%26_Inspection.md) (8 shared connections)
- [Recursive & Markdown Splitting](Recursive_%26_Markdown_Splitting.md) (6 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (5 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (3 shared connections)
- [Trace Listing CLI](Trace_Listing_CLI.md) (3 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (3 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (2 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (2 shared connections)
- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (2 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (2 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `src/osc_assistant/types.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 99 (94%)
- INFERRED: 6 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*