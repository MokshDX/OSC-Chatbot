# Grounded Prompt & LangChain Chat

> 29 nodes · cohesion 0.12

## Key Concepts

- **llm/langchain_bridge.py** (34 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.stream()** (17 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.complete()** (13 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **LangChainChatModel** (12 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **compose_grounded_system()** (10 connections) — `src/osc_assistant/grounding.py`
- **Any** (7 connections)
- **_to_langchain_messages()** (7 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_instantiate()** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **._bind()** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_text_of()** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_stop_reason()** (5 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_reported_model()** (3 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.supports_citations()** (2 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **Fold the system prompt, citation instruction and sources into one string. Used…** (1 connections) — `src/osc_assistant/grounding.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **register** (1 connections)
- **StreamEvent** (1 connections)
- **Chat provider backed by any LangChain `BaseChatModel`. **Why this exists.** OSC…** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **False: LangChain normalises provider responses to a common message shape.…** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **Stream text, resolving citations once the full answer is known. Markers can…** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **Apply the per-request generation parameters. `bind` rather than constructor…** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **Import and construct the LangChain chat model named by `class_path`.** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- *... and 4 more nodes in this community*

## Relationships

- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (20 shared connections)
- [Citation Grounding & Reasoning Models](Citation_Grounding_%26_Reasoning_Models.md) (8 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (7 shared connections)
- [LangChain Bridges & Splitters](LangChain_Bridges_%26_Splitters.md) (6 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (4 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (4 shared connections)
- [OpenAI-Compatible Chat Provider](OpenAI-Compatible_Chat_Provider.md) (3 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (2 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (2 shared connections)
- [RRF Fusion & Source Rendering](RRF_Fusion_%26_Source_Rendering.md) (1 shared connections)
- [HTML Parser](HTML_Parser.md) (1 shared connections)

## Source Files

- `src/osc_assistant/grounding.py`
- `src/osc_assistant/providers/llm/langchain_bridge.py`

## Audit Trail

- EXTRACTED: 153 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*