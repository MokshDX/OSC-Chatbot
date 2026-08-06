# Search Strategies & Reranking

> 21 nodes · cohesion 0.15

## Key Concepts

- **ScoredChunk** (40 connections) — `src/osc_assistant/types.py`
- **_to_scored_chunk()** (8 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_encode_vector()** (7 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_hybrid()** (6 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.search_hybrid()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_vector()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_keyword()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.search_vector()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.search_keyword()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **._search()** (4 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **._search_store()** (4 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **.rerank()** (3 connections) — `src/osc_assistant/protocols.py`
- **_cosine_similarity()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Vector** (3 connections)
- **Vector** (3 connections)
- **_tokenize()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Return the `top_k` most relevant candidates, most relevant first.** (1 connections) — `src/osc_assistant/protocols.py`
- **Term-overlap scoring. Deliberately not BM25: this exists to make hybrid…** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Render a vector in pgvector's literal form for the `::vector` cast.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Dispatch to the store, timing it and recording the shape of the result. The…** (1 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **A chunk with a relevance score. Scores are only comparable within a single…** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [Reranker Protocol & Provider Registration](Reranker_Protocol_%26_Provider_Registration.md) (5 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (5 shared connections)
- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (5 shared connections)
- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (4 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (4 shared connections)
- [Store Construction & Embedding Calls](Store_Construction_%26_Embedding_Calls.md) (4 shared connections)
- [RRF Fusion & Source Rendering](RRF_Fusion_%26_Source_Rendering.md) (3 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (3 shared connections)
- [VectorStore Errors & Inspection](VectorStore_Errors_%26_Inspection.md) (3 shared connections)
- [Evaluator & Judge Composition](Evaluator_%26_Judge_Composition.md) (2 shared connections)
- [API Request & Response Schemas](API_Request_%26_Response_Schemas.md) (2 shared connections)
- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (2 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/vectorstores/memory.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 108 (95%)
- INFERRED: 6 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*