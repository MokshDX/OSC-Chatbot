# ScoredChunk

> God node · 36 connections · `src/osc_assistant/types.py`

**Community:** [Logging System Design](Logging_System_Design.md)

## Connections by Relation

### contains
- types.py `EXTRACTED`

### imports
- protocols.py `EXTRACTED`
- pgvector.py `EXTRACTED`
- memory.py `EXTRACTED`
- retrieval/pipeline.py `EXTRACTED`
- judge.py `EXTRACTED`
- cross_encoder.py `EXTRACTED`
- noop.py `EXTRACTED`
- fusion.py `EXTRACTED`
- langchain.py `EXTRACTED`

### rationale_for
- A chunk with a relevance score. Scores are only comparable within a single… `EXTRACTED`

### references
- reciprocal_rank_fusion() `EXTRACTED`
- _to_scored_chunk() `EXTRACTED`
- _ranking() `EXTRACTED`
- .is_faithful() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- to_langchain_document() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- ._search() `EXTRACTED`
- ._search_store() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- .rerank() `EXTRACTED`
- .rerank() `EXTRACTED`
- .rerank() `EXTRACTED`

### uses
- EmbeddingModel `INFERRED`
- VectorStore `INFERRED`
- ChatModel `INFERRED`
- Chunker `INFERRED`
- Reranker `INFERRED`
- StoreInspector `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*