# Anthropic Chat Adapter

> 23 nodes · cohesion 0.14

## Key Concepts

- **anthropic_provider.py** (27 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.stream()** (11 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **AnthropicChatModel** (9 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.complete()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_build_messages()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_parse_content()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **._build_payload()** (6 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Any** (5 connections)
- **.__init__()** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **AnthropicOptions** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_last_user_index()** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.supports_citations()** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **BaseModel** (1 connections)
- **register** (1 connections)
- **StreamEvent** (1 connections)
- **Anthropic chat provider. This is the only adapter with native citation support:…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Stream the answer, then emit citations once the message is complete. Text is…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Attach sources as citable documents on the final user turn. Sources belong to…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Flatten response blocks into text, appending a marker after each cited span.…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Adapter over the Anthropic Messages API. Satisfies `protocols.ChatModel`…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`

## Relationships

- [Streaming & Response Types](Streaming_%26_Response_Types.md) (12 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (8 shared connections)
- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (4 shared connections)
- [Rank Fusion & Citation Grounding](Rank_Fusion_%26_Citation_Grounding.md) (3 shared connections)
- [Chat Model Interface](Chat_Model_Interface.md) (2 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (2 shared connections)
- [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md) (2 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (2 shared connections)
- [OpenAI-Compatible Chat Adapter](OpenAI-Compatible_Chat_Adapter.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/llm/anthropic_provider.py`

## Audit Trail

- EXTRACTED: 108 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*