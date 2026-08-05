# Anthropic Chat Adapter

> 27 nodes

## Key Concepts

- **anthropic_provider.py** (27 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.stream()** (11 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **AnthropicChatModel** (10 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.complete()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_build_messages()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_parse_content()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **llm/__init__.py** (6 connections) — `src/osc_assistant/providers/llm/__init__.py`
- **._build_payload()** (6 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Any** (5 connections)
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **AnthropicOptions** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_last_user_index()** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.aclose()** (2 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Chat model providers. Imported for registration side effects.** (1 connections) — `src/osc_assistant/providers/llm/__init__.py`
- **BaseModel** (1 connections)
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.supports_citations()** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **StreamEvent** (1 connections)
- **register** (1 connections)
- **Anthropic chat provider. This is the only adapter with native citation support:…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Adapter over the Anthropic Messages API. Satisfies `protocols.ChatModel`…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Release the underlying HTTP client. See `Container.shutdown()`.** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Stream the answer, then emit citations once the message is complete. Text is…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- *... and 2 more nodes in this community*

## Relationships

- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (14 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (6 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (6 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (3 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (3 shared connections)
- [Rank Fusion & Source Rendering](Rank_Fusion_%26_Source_Rendering.md) (3 shared connections)
- [ChatModel Protocol](ChatModel_Protocol.md) (2 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (1 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/llm/__init__.py`
- `src/osc_assistant/providers/llm/anthropic_provider.py`

## Audit Trail

- EXTRACTED: 119 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*