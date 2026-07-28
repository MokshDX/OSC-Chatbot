# Gemini Chat Adapter

> 28 nodes · cohesion 0.13

## Key Concepts

- **ChatRequest** (39 connections) — `src/osc_assistant/types.py`
- **llm/gemini.py** (28 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **grounding.py** (12 connections) — `src/osc_assistant/grounding.py`
- **.stream()** (12 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **GeminiChatModel** (9 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.complete()** (9 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **compose_grounded_system()** (8 connections) — `src/osc_assistant/grounding.py`
- **._build_config()** (7 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.complete()** (7 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **_build_contents()** (6 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **._build_payload()** (6 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **Any** (4 connections)
- **_finish_reason()** (3 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **GeminiOptions** (3 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **Grounding and citation handling for providers without native citation support.…** (1 connections) — `src/osc_assistant/grounding.py`
- **Fold the system prompt, citation instruction and sources into one string. Used…** (1 connections) — `src/osc_assistant/grounding.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.supports_citations()** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **BaseModel** (1 connections)
- **register** (1 connections)
- **StreamEvent** (1 connections)
- **Google Gemini chat provider (native SDK). Gemini also exposes an OpenAI-…** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **Build the generation config as a plain mapping. `google-genai` accepts a dict…** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- *... and 3 more nodes in this community*

## Relationships

- [Streaming & Response Types](Streaming_%26_Response_Types.md) (23 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (16 shared connections)
- [Rank Fusion & Citation Grounding](Rank_Fusion_%26_Citation_Grounding.md) (10 shared connections)
- [OpenAI-Compatible Chat Adapter](OpenAI-Compatible_Chat_Adapter.md) (8 shared connections)
- [Chat Model Interface](Chat_Model_Interface.md) (5 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (4 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (3 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (3 shared connections)
- [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md) (2 shared connections)
- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (2 shared connections)
- [Embedding Model Interface](Embedding_Model_Interface.md) (1 shared connections)
- [Vector Store Interface](Vector_Store_Interface.md) (1 shared connections)

## Source Files

- `src/osc_assistant/grounding.py`
- `src/osc_assistant/providers/llm/gemini.py`
- `src/osc_assistant/providers/llm/openai_compatible.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 166 (95%)
- INFERRED: 9 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*