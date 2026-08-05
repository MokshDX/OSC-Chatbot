# Store Inspector

> 12 nodes

## Key Concepts

- **DocumentSummary** (21 connections) — `src/osc_assistant/types.py`
- **._summarise()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_to_document_summary()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.list_documents()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.get_document()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.list_documents()** (3 connections) — `src/osc_assistant/protocols.py`
- **.get_document()** (3 connections) — `src/osc_assistant/protocols.py`
- **.list_documents()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.get_document()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Indexed documents, newest first. `search` matches title or source URI.** (1 connections) — `src/osc_assistant/protocols.py`
- **One document's index record, or None if it is not indexed.** (1 connections) — `src/osc_assistant/protocols.py`
- **What the store knows about one indexed document. Distinct from `Document`: it…** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (3 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (3 shared connections)
- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (3 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (3 shared connections)
- [pgvector Store Interface](pgvector_Store_Interface.md) (2 shared connections)
- [Vector Store Registration](Vector_Store_Registration.md) (2 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (2 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (1 shared connections)
- [ChatModel Protocol](ChatModel_Protocol.md) (1 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (1 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (1 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (1 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/vectorstores/memory.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 48 (89%)
- INFERRED: 6 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*