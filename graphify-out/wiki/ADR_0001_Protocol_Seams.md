# ADR 0001 Protocol Seams

> 22 nodes

## Key Concepts

- **EmbeddingModel** (30 connections) — `src/osc_assistant/protocols.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **.__init__()** (4 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **Vector** (4 connections)
- **.search_hybrid()** (4 connections) — `src/osc_assistant/protocols.py`
- **.embed_documents()** (3 connections) — `src/osc_assistant/protocols.py`
- **.embed_query()** (3 connections) — `src/osc_assistant/protocols.py`
- **.search_vector()** (3 connections) — `src/osc_assistant/protocols.py`
- **.dimensions()** (2 connections) — `src/osc_assistant/protocols.py`
- **.model_id()** (1 connections) — `src/osc_assistant/protocols.py`
- **A text embedding model. Document and query embedding are separate methods…** (1 connections) — `src/osc_assistant/protocols.py`
- **Vector width. Must match the vector store's configured dimension.** (1 connections) — `src/osc_assistant/protocols.py`
- **Embed corpus text. Returns one vector per input, in order.** (1 connections) — `src/osc_assistant/protocols.py`
- **Embed a search query.** (1 connections) — `src/osc_assistant/protocols.py`
- **Combined lexical and vector search, fused into a single ranking.** (1 connections) — `src/osc_assistant/protocols.py`
- **register** (1 connections)
- **register** (1 connections)
- **register** (1 connections)
- **register** (1 connections)

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (11 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (7 shared connections)
- [Memory Vector Store](Memory_Vector_Store.md) (4 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (3 shared connections)
- [Logging System Design](Logging_System_Design.md) (3 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (2 shared connections)
- [PgVector Store](PgVector_Store.md) (1 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (1 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (1 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (1 shared connections)
- [LangChain Embedding Bridge](LangChain_Embedding_Bridge.md) (1 shared connections)
- [Gemini Embeddings](Gemini_Embeddings.md) (1 shared connections)

## Source Files

- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/embeddings/gemini.py`
- `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- `src/osc_assistant/providers/embeddings/local.py`
- `src/osc_assistant/providers/embeddings/voyage.py`

## Audit Trail

- EXTRACTED: 74 (89%)
- INFERRED: 9 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*