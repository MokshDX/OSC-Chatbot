# Configuration Errors & Gemini Embeddings

> 29 nodes

## Key Concepts

- **MissingDependencyError** (29 connections) — `src/osc_assistant/errors.py`
- **llm/openai_compatible.py** (29 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **ConfigurationError** (26 connections) — `src/osc_assistant/errors.py`
- **_FakeEmbeddings** (23 connections) — `tests/test_langchain_integration.py`
- **_instantiate()** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **.__init__()** (5 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **GeminiEmbeddingOptions** (3 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **LocalEmbeddingOptions** (3 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **OpenAIEmbeddingOptions** (3 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **GeminiOptions** (3 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **_Preset** (3 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **OpenAICompatibleOptions** (3 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **_resolve_key()** (3 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **The system is misconfigured and cannot start or serve a request. Raised for…** (1 connections) — `src/osc_assistant/errors.py`
- **A provider was selected but its optional dependency is not installed.** (1 connections) — `src/osc_assistant/errors.py`
- **BaseModel** (1 connections)
- **Any** (1 connections)
- **BaseModel** (1 connections)
- **BaseModel** (1 connections)
- **BaseModel** (1 connections)
- **BaseModel** (1 connections)
- *... and 4 more nodes in this community*

## Relationships

- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (23 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (9 shared connections)
- [Grounding & OpenAI-Compatible Chat](Grounding_%26_OpenAI-Compatible_Chat.md) (7 shared connections)
- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (7 shared connections)
- [LangChain Embedding Bridge](LangChain_Embedding_Bridge.md) (6 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (5 shared connections)
- [Text Extraction Parsers](Text_Extraction_Parsers.md) (4 shared connections)
- [DimensionMismatchError](DimensionMismatchError.md) (3 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (3 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (3 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (3 shared connections)
- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (2 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/providers/embeddings/gemini.py`
- `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- `src/osc_assistant/providers/embeddings/local.py`
- `src/osc_assistant/providers/embeddings/openai_compatible.py`
- `src/osc_assistant/providers/llm/gemini.py`
- `src/osc_assistant/providers/llm/openai_compatible.py`
- `tests/test_langchain_integration.py`

## Audit Trail

- EXTRACTED: 147 (89%)
- INFERRED: 19 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*