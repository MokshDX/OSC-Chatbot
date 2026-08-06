# Error Hierarchy & Embedding Providers

> 42 nodes · cohesion 0.07

## Key Concepts

- **MissingDependencyError** (29 connections) — `src/osc_assistant/errors.py`
- **ConfigurationError** (26 connections) — `src/osc_assistant/errors.py`
- **_FakeEmbeddings** (23 connections) — `tests/test_langchain_integration.py`
- **embeddings/langchain_bridge.py** (18 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **LangChainEmbeddingModel** (11 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **DimensionMismatchError** (9 connections) — `src/osc_assistant/errors.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **_instantiate()** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **._assert_width()** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **LangChainEmbeddingOptions** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **.__init__()** (5 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **.embed_documents()** (4 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **.embed_query()** (4 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.__init__()** (3 connections) — `src/osc_assistant/errors.py`
- **GeminiEmbeddingOptions** (3 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **OpenAIEmbeddingOptions** (3 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **GeminiOptions** (3 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **OpenAICompatibleOptions** (3 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.__init__()** (2 connections) — `src/osc_assistant/errors.py`
- **.__init__()** (2 connections) — `src/osc_assistant/errors.py`
- **Vector** (2 connections)
- *... and 17 more nodes in this community*

## Relationships

- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (19 shared connections)
- [LangChain Bridges & Splitters](LangChain_Bridges_%26_Splitters.md) (8 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (6 shared connections)
- [OpenAI-Compatible Chat Provider](OpenAI-Compatible_Chat_Provider.md) (5 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (5 shared connections)
- [Grounded Prompt & LangChain Chat](Grounded_Prompt_%26_LangChain_Chat.md) (4 shared connections)
- [Parse Errors & Format Parsers](Parse_Errors_%26_Format_Parsers.md) (4 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (4 shared connections)
- [Anthropic Adapter & Retrieval Pipeline](Anthropic_Adapter_%26_Retrieval_Pipeline.md) (3 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (3 shared connections)
- [Component Registry](Component_Registry.md) (2 shared connections)
- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (2 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/providers/embeddings/gemini.py`
- `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- `src/osc_assistant/providers/embeddings/openai_compatible.py`
- `src/osc_assistant/providers/llm/gemini.py`
- `src/osc_assistant/providers/llm/openai_compatible.py`
- `tests/test_langchain_integration.py`

## Audit Trail

- EXTRACTED: 180 (89%)
- INFERRED: 22 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*