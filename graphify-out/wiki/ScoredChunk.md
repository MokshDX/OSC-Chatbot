# ScoredChunk

> God node · 32 connections · `src/osc_assistant/types.py`

**Community:** [Hybrid Search Scoring](Hybrid_Search_Scoring.md)

## Connections by Relation

### contains
- types.py `EXTRACTED`

### imports
- protocols.py `EXTRACTED`
- pgvector.py `EXTRACTED`
- memory.py `EXTRACTED`
- schemas.py `EXTRACTED`
- retrieval/pipeline.py `EXTRACTED`
- cross_encoder.py `EXTRACTED`
- noop.py `EXTRACTED`
- fusion.py `EXTRACTED`

### rationale_for
- A chunk with a relevance score. Scores are only comparable within a single… `EXTRACTED`

### references
- reciprocal_rank_fusion() `EXTRACTED`
- _to_scored_chunk() `EXTRACTED`
- _ranking() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- .from_domain() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- .rerank() `EXTRACTED`
- ._search() `EXTRACTED`
- .rerank() `EXTRACTED`
- .rerank() `EXTRACTED`

### uses
- [VectorStore](VectorStore.md) `INFERRED`
- [EmbeddingModel](EmbeddingModel.md) `INFERRED`
- ChatModel `INFERRED`
- Reranker `INFERRED`
- Chunker `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*