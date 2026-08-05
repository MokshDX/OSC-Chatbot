# Outbound LangChain Retriever

> 22 nodes

## Key Concepts

- **ScoredChunk** (40 connections) — `src/osc_assistant/types.py`
- **langchain.py** (7 connections) — `src/osc_assistant/integrations/langchain.py`
- **to_langchain_document()** (4 connections) — `src/osc_assistant/integrations/langchain.py`
- **Vector** (4 connections)
- **.search_hybrid()** (4 connections) — `src/osc_assistant/protocols.py`
- **._search()** (4 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **._search_store()** (4 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **.embed_documents()** (3 connections) — `src/osc_assistant/protocols.py`
- **.embed_query()** (3 connections) — `src/osc_assistant/protocols.py`
- **.search_vector()** (3 connections) — `src/osc_assistant/protocols.py`
- **.search_keyword()** (3 connections) — `src/osc_assistant/protocols.py`
- **.rerank()** (3 connections) — `src/osc_assistant/protocols.py`
- **LangChainDocument** (1 connections)
- **Exposing OSC to LangChain, rather than the other way round. Every other…** (1 connections) — `src/osc_assistant/integrations/langchain.py`
- **Translate one retrieval hit into a LangChain document. The score and the match…** (1 connections) — `src/osc_assistant/integrations/langchain.py`
- **Embed corpus text. Returns one vector per input, in order.** (1 connections) — `src/osc_assistant/protocols.py`
- **Embed a search query.** (1 connections) — `src/osc_assistant/protocols.py`
- **Lexical search. Return `[]` if the store has no lexical index.** (1 connections) — `src/osc_assistant/protocols.py`
- **Combined lexical and vector search, fused into a single ranking.** (1 connections) — `src/osc_assistant/protocols.py`
- **Return the `top_k` most relevant candidates, most relevant first.** (1 connections) — `src/osc_assistant/protocols.py`
- **Dispatch to the store, timing it and recording the shape of the result. The…** (1 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **A chunk with a relevance score. Scores are only comparable within a single…** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (8 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (4 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (4 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (4 shared connections)
- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (4 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (3 shared connections)
- [Rank Fusion & Source Rendering](Rank_Fusion_%26_Source_Rendering.md) (3 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (2 shared connections)
- [OSCRetriever()](OSCRetriever%28%29.md) (1 shared connections)
- [Markdown Chunker & LangChain Tests](Markdown_Chunker_%26_LangChain_Tests.md) (1 shared connections)
- [Tracing & Retrieval Instrumentation](Tracing_%26_Retrieval_Instrumentation.md) (1 shared connections)

## Source Files

- `src/osc_assistant/integrations/langchain.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 86 (93%)
- INFERRED: 6 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*