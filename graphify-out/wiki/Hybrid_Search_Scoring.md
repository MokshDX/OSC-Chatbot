# Hybrid Search Scoring

> 13 nodes · cohesion 0.22

## Key Concepts

- **ScoredChunk** (32 connections) — `src/osc_assistant/types.py`
- **.search_hybrid()** (6 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.search_keyword()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.search_vector()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Vector** (4 connections)
- **.search_hybrid()** (4 connections) — `src/osc_assistant/protocols.py`
- **.search_vector()** (3 connections) — `src/osc_assistant/protocols.py`
- **_cosine_similarity()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Vector** (3 connections)
- **_tokenize()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Combined lexical and vector search, fused into a single ranking.** (1 connections) — `src/osc_assistant/protocols.py`
- **Term-overlap scoring. Deliberately not BM25: this exists to make hybrid…** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **A chunk with a relevance score. Scores are only comparable within a single…** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [Vector Store Interface](Vector_Store_Interface.md) (4 shared connections)
- [Rank Fusion & Citation Grounding](Rank_Fusion_%26_Citation_Grounding.md) (4 shared connections)
- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (4 shared connections)
- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (4 shared connections)
- [Embedding Model Interface](Embedding_Model_Interface.md) (3 shared connections)
- [Dimension Guard & Match Source](Dimension_Guard_%26_Match_Source.md) (3 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (3 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (2 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (2 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (2 shared connections)
- [Chat Model Interface](Chat_Model_Interface.md) (1 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/vectorstores/memory.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 65 (93%)
- INFERRED: 5 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*