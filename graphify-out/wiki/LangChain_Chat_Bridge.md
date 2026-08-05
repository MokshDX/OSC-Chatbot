# LangChain Chat Bridge

> 33 nodes

## Key Concepts

- **llm/langchain_bridge.py** (34 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.stream()** (17 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.complete()** (13 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **LangChainChatModel** (12 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **compose_grounded_system()** (10 connections) — `src/osc_assistant/grounding.py`
- **Any** (7 connections)
- **_to_langchain_messages()** (7 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **LangChainChatOptions** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **._bind()** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_instantiate()** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_text_of()** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_stop_reason()** (5 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_reported_model()** (3 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **test_bridge_reports_a_missing_integration_package_actionably()** (3 connections) — `tests/test_langchain_integration.py`
- **test_bridge_rejects_a_class_path_without_a_module()** (3 connections) — `tests/test_langchain_integration.py`
- **.supports_citations()** (2 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **Fold the system prompt, citation instruction and sources into one string. Used…** (1 connections) — `src/osc_assistant/grounding.py`
- **BaseModel** (1 connections)
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **StreamEvent** (1 connections)
- **register** (1 connections)
- **Chat provider backed by any LangChain `BaseChatModel`. **Why this exists.** OSC…** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- *... and 8 more nodes in this community*

## Relationships

- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (14 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (12 shared connections)
- [Grounding & OpenAI-Compatible Chat](Grounding_%26_OpenAI-Compatible_Chat.md) (9 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (6 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (5 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (4 shared connections)
- [Markdown Chunker & LangChain Tests](Markdown_Chunker_%26_LangChain_Tests.md) (3 shared connections)
- [ChatModel Protocol](ChatModel_Protocol.md) (2 shared connections)
- [Rank Fusion & Source Rendering](Rank_Fusion_%26_Source_Rendering.md) (1 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (1 shared connections)

## Source Files

- `src/osc_assistant/grounding.py`
- `src/osc_assistant/providers/llm/langchain_bridge.py`
- `tests/test_langchain_integration.py`

## Audit Trail

- EXTRACTED: 166 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*