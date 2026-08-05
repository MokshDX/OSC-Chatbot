# LangChain Embedding Bridge

> 19 nodes

## Key Concepts

- **LangChainEmbeddingModel** (11 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **_embedding_bridge()** (7 connections) — `tests/test_langchain_integration.py`
- **LangChainEmbeddingOptions** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **._assert_width()** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **.embed_documents()** (4 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **.embed_query()** (4 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **.embed_documents()** (4 connections) — `tests/test_langchain_integration.py`
- **.embed_query()** (4 connections) — `tests/test_langchain_integration.py`
- **test_embedding_bridge_satisfies_the_protocol()** (4 connections) — `tests/test_langchain_integration.py`
- **test_embedding_bridge_rejects_a_misdeclared_width()** (4 connections) — `tests/test_langchain_integration.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **test_embedding_bridge_short_circuits_an_empty_batch()** (3 connections) — `tests/test_langchain_integration.py`
- **Vector** (2 connections)
- **BaseModel** (1 connections)
- **.model_id()** (1 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **.dimensions()** (1 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **Adapter presenting a LangChain embeddings object as an OSC `EmbeddingModel`.** (1 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **Catch a misconfigured `dimensions` at the first call rather than at query time.…** (1 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **A wrong `dimensions` would embed the corpus at one width and query at another.** (1 connections) — `tests/test_langchain_integration.py`

## Relationships

- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (6 shared connections)
- [Markdown Chunker & LangChain Tests](Markdown_Chunker_%26_LangChain_Tests.md) (4 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (3 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (2 shared connections)
- [DimensionMismatchError](DimensionMismatchError.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- `tests/test_langchain_integration.py`

## Audit Trail

- EXTRACTED: 64 (97%)
- INFERRED: 2 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*