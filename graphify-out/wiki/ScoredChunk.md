# ScoredChunk

> God node · 40 connections · `src/osc_assistant/types.py`

**Community:** [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md)

## Connections by Relation

### contains
- types.py `EXTRACTED`

### imports
- protocols.py `EXTRACTED`
- runner.py `EXTRACTED`
- memory.py `EXTRACTED`
- pgvector.py `EXTRACTED`
- retrieval/pipeline.py `EXTRACTED`
- schemas.py `EXTRACTED`
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
- ._score_retrieval() `EXTRACTED`
- .is_faithful() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- .from_domain() `EXTRACTED`
- to_langchain_document() `EXTRACTED`
- .search_hybrid() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- ._search() `EXTRACTED`
- ._search_store() `EXTRACTED`
- .search_vector() `EXTRACTED`
- .search_keyword() `EXTRACTED`
- .rerank() `EXTRACTED`
- .rerank() `EXTRACTED`

### uses
- ChatModel `INFERRED`
- EmbeddingModel `INFERRED`
- VectorStore `INFERRED`
- Chunker `INFERRED`
- Reranker `INFERRED`
- StoreInspector `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*