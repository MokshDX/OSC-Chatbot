# VectorStore Protocol

> 16 nodes

## Key Concepts

- **VectorStore** (33 connections) — `src/osc_assistant/protocols.py`
- **.__init__()** (6 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **.vector_store()** (4 connections) — `src/osc_assistant/container.py`
- **.setup()** (2 connections) — `src/osc_assistant/protocols.py`
- **.dimensions()** (2 connections) — `src/osc_assistant/protocols.py`
- **.delete_document()** (2 connections) — `src/osc_assistant/protocols.py`
- **.list_document_hashes()** (2 connections) — `src/osc_assistant/protocols.py`
- **.document_ids()** (2 connections) — `src/osc_assistant/protocols.py`
- **Build the store, injecting values it cannot know on its own. Vector width, the…** (1 connections) — `src/osc_assistant/container.py`
- **.close()** (1 connections) — `src/osc_assistant/protocols.py`
- **Persistence and retrieval of embedded chunks. Implementations that cannot do…** (1 connections) — `src/osc_assistant/protocols.py`
- **Prepare the store (connect, create collections). Idempotent.** (1 connections) — `src/osc_assistant/protocols.py`
- **The vector width this store is configured to hold.** (1 connections) — `src/osc_assistant/protocols.py`
- **Remove a document and every chunk belonging to it.** (1 connections) — `src/osc_assistant/protocols.py`
- **Map document id to stored content hash, for incremental sync.** (1 connections) — `src/osc_assistant/protocols.py`
- **Every document id currently indexed.** (1 connections) — `src/osc_assistant/protocols.py`

## Relationships

- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (5 shared connections)
- [Outbound LangChain Retriever](Outbound_LangChain_Retriever.md) (4 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (2 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (2 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (2 shared connections)
- [EmbeddedChunk](EmbeddedChunk.md) (2 shared connections)
- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (2 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (2 shared connections)
- [Vector Store Registration](Vector_Store_Registration.md) (2 shared connections)
- [Retrieval Pipeline](Retrieval_Pipeline.md) (2 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (1 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (1 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/retrieval/pipeline.py`

## Audit Trail

- EXTRACTED: 52 (85%)
- INFERRED: 9 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*