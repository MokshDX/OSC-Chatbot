# EmbeddedChunk

> 10 nodes

## Key Concepts

- **EmbeddedChunk** (20 connections) — `src/osc_assistant/types.py`
- **populated()** (7 connections) — `tests/test_pgvector_integration.py`
- **test_failed_replace_leaves_no_hash_without_chunks()** (7 connections) — `tests/test_pgvector_integration.py`
- **.replace_document()** (4 connections) — `src/osc_assistant/protocols.py`
- **embeddings()** (4 connections) — `tests/test_pgvector_integration.py`
- **fixture** (3 connections)
- **Atomically replace a document and all of its chunks. Must be all-or-nothing.…** (1 connections) — `src/osc_assistant/protocols.py`
- **A chunk paired with the vector produced for it, tagged with its model. The…** (1 connections) — `src/osc_assistant/types.py`
- **Overrides the shared fixture so vectors match the target table's width.** (1 connections) — `tests/test_pgvector_integration.py`
- **The skip check reads a recorded hash as "chunks are present". A partial write…** (1 connections) — `tests/test_pgvector_integration.py`

## Relationships

- [pgvector Store Interface](pgvector_Store_Interface.md) (7 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (4 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (4 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (3 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (3 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (2 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (1 shared connections)
- [ChatModel Protocol](ChatModel_Protocol.md) (1 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (1 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (1 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (1 shared connections)
- [Vector Store Registration](Vector_Store_Registration.md) (1 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`
- `src/osc_assistant/types.py`
- `tests/test_pgvector_integration.py`

## Audit Trail

- EXTRACTED: 43 (88%)
- INFERRED: 6 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*