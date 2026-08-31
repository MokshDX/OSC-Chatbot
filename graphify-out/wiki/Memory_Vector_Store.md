# Memory Vector Store

> 30 nodes

## Key Concepts

- **VectorStore** (30 connections) — `src/osc_assistant/protocols.py`
- **EmbeddedChunk** (20 connections) — `src/osc_assistant/types.py`
- **.replace_document()** (6 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.replace_document()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **._index()** (5 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.replace_document()** (4 connections) — `src/osc_assistant/protocols.py`
- **.search_keyword()** (3 connections) — `src/osc_assistant/protocols.py`
- **.setup()** (2 connections) — `src/osc_assistant/protocols.py`
- **.dimensions()** (2 connections) — `src/osc_assistant/protocols.py`
- **.delete_document()** (2 connections) — `src/osc_assistant/protocols.py`
- **.list_document_hashes()** (2 connections) — `src/osc_assistant/protocols.py`
- **.document_ids()** (2 connections) — `src/osc_assistant/protocols.py`
- **.delete_document()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Chunk, embed and store one document. Each of the three stages gets its own…** (1 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **.close()** (1 connections) — `src/osc_assistant/protocols.py`
- **Persistence and retrieval of embedded chunks. Implementations that cannot do…** (1 connections) — `src/osc_assistant/protocols.py`
- **Prepare the store (connect, create collections). Idempotent.** (1 connections) — `src/osc_assistant/protocols.py`
- **The vector width this store is configured to hold.** (1 connections) — `src/osc_assistant/protocols.py`
- **Atomically replace a document and all of its chunks. Must be all-or-nothing.…** (1 connections) — `src/osc_assistant/protocols.py`
- **Remove a document and every chunk belonging to it.** (1 connections) — `src/osc_assistant/protocols.py`
- **Map document id to stored content hash, for incremental sync.** (1 connections) — `src/osc_assistant/protocols.py`
- **Every document id currently indexed.** (1 connections) — `src/osc_assistant/protocols.py`
- **Lexical search. Return `[]` if the store has no lexical index.** (1 connections) — `src/osc_assistant/protocols.py`
- *... and 5 more nodes in this community*

## Relationships

- [Conversational Evaluator](Conversational_Evaluator.md) (10 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (8 shared connections)
- [Logging System Design](Logging_System_Design.md) (6 shared connections)
- [Protocol Seams & Container](Protocol_Seams_%26_Container.md) (6 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (5 shared connections)
- [ADR 0001 Protocol Seams](ADR_0001_Protocol_Seams.md) (4 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (3 shared connections)
- [Settings Precedence Tests](Settings_Precedence_Tests.md) (3 shared connections)
- [PgVector Store](PgVector_Store.md) (1 shared connections)
- [AccessLock & BulkImportExport Schemas](AccessLock_%26_BulkImportExport_Schemas.md) (1 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (1 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (1 shared connections)

## Source Files

- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/vectorstores/memory.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 97 (87%)
- INFERRED: 14 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*