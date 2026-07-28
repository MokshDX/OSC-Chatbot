# VectorStore

> God node · 31 connections · `src/osc_assistant/protocols.py`

**Community:** [Vector Store Interface](Vector_Store_Interface.md)

## Connections by Relation

### contains
- protocols.py `EXTRACTED`

### imports
- container.py `EXTRACTED`
- pgvector.py `EXTRACTED`
- registries.py `EXTRACTED`
- memory.py `EXTRACTED`
- retrieval/pipeline.py `EXTRACTED`
- ingestion/pipeline.py `EXTRACTED`

### inherits
- Protocol `EXTRACTED`

### method
- .replace_document() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .delete_document() `EXTRACTED`
- .dimensions() `EXTRACTED`
- .document_ids() `EXTRACTED`
- .list_document_hashes() `EXTRACTED`
- .setup() `EXTRACTED`
- .close() `EXTRACTED`

### rationale_for
- Persistence and retrieval of embedded chunks. Implementations that cannot do… `EXTRACTED`

### references
- .__init__() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- .vector_store() `EXTRACTED`
- .__init__() `EXTRACTED`

### uses
- [Document](Document.md) `INFERRED`
- [ChatRequest](ChatRequest.md) `INFERRED`
- [ScoredChunk](ScoredChunk.md) `INFERRED`
- Container `INFERRED`
- ChatResponse `INFERRED`
- Chunk `INFERRED`
- EmbeddedChunk `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*