# EmbeddingModel

> God node · 28 connections · `src/osc_assistant/protocols.py`

**Community:** [Embedding Model Interface](Embedding_Model_Interface.md)

## Connections by Relation

### contains
- protocols.py `EXTRACTED`

### imports
- container.py `EXTRACTED`
- registries.py `EXTRACTED`
- retrieval/pipeline.py `EXTRACTED`
- embeddings/gemini.py `EXTRACTED`
- embeddings/openai_compatible.py `EXTRACTED`
- local.py `EXTRACTED`
- voyage.py `EXTRACTED`
- ingestion/pipeline.py `EXTRACTED`

### inherits
- Protocol `EXTRACTED`

### method
- .embed_documents() `EXTRACTED`
- .embed_query() `EXTRACTED`
- .dimensions() `EXTRACTED`
- .model_id() `EXTRACTED`

### rationale_for
- A text embedding model. Document and query embedding are separate methods… `EXTRACTED`

### references
- .__init__() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- .__init__() `EXTRACTED`
- .embeddings() `EXTRACTED`

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