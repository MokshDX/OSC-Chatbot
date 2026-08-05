# pgvector Search & Migrations

> 19 nodes

## Key Concepts

- **._acquire()** (16 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_to_scored_chunk()** (8 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_encode_vector()** (7 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.replace_document()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_vector()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_hybrid()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **._migrate()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_to_chunk()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Any** (5 connections)
- **._assert_dimensions_match()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_keyword()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.document_chunks()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.get_chunk()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Vector** (3 connections)
- **.delete_document()** (2 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Replace a document and its chunks in a single transaction. Delete-then-insert…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Apply unapplied migration files in filename order. A hand-rolled runner rather…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Fail loudly if the stored vector width disagrees with the active model.…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Render a vector in pgvector's literal form for the `::vector` cast.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`

## Relationships

- [pgvector Store Interface](pgvector_Store_Interface.md) (11 shared connections)
- [Vector Store Registration](Vector_Store_Registration.md) (7 shared connections)
- [Outbound LangChain Retriever](Outbound_LangChain_Retriever.md) (4 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (3 shared connections)
- [Store Inspector](Store_Inspector.md) (3 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (2 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (1 shared connections)
- [EmbeddedChunk](EmbeddedChunk.md) (1 shared connections)
- [IndexStatistics](IndexStatistics.md) (1 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/pgvector.py`

## Audit Trail

- EXTRACTED: 92 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*