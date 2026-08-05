# Citation Parsing & Gemini Chat

> 27 nodes

## Key Concepts

- **ProviderError** (33 connections) — `src/osc_assistant/errors.py`
- **Usage** (29 connections) — `src/osc_assistant/types.py`
- **llm/gemini.py** (28 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **parse_marker_citations()** (21 connections) — `src/osc_assistant/grounding.py`
- **.stream()** (13 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **GeminiChatModel** (9 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.complete()** (9 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **._build_config()** (7 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **_build_contents()** (6 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.text()** (5 connections) — `src/osc_assistant/ingestion/parsers.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.complete()** (5 connections) — `tests/conftest.py`
- **Any** (4 connections)
- **_finish_reason()** (3 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **An upstream provider (LLM, embeddings, reranker) failed.** (1 connections) — `src/osc_assistant/errors.py`
- **Extract citations from `[n]` markers in `text`. Markers referring to a source…** (1 connections) — `src/osc_assistant/grounding.py`
- **The collected text, with each block element on its own line.** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.supports_citations()** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **StreamEvent** (1 connections)
- **register** (1 connections)
- **Google Gemini chat provider (native SDK). Gemini also exposes an OpenAI-…** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **Adapter over `google-genai`'s async models interface.** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **Build the generation config as a plain mapping. `google-genai` accepts a dict…** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- *... and 2 more nodes in this community*

## Relationships

- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (22 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (12 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (12 shared connections)
- [Grounding & OpenAI-Compatible Chat](Grounding_%26_OpenAI-Compatible_Chat.md) (10 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (9 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (8 shared connections)
- [Rank Fusion & Source Rendering](Rank_Fusion_%26_Source_Rendering.md) (7 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (6 shared connections)
- [Settings Schema](Settings_Schema.md) (4 shared connections)
- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (3 shared connections)
- [LangChain Embedding Bridge](LangChain_Embedding_Bridge.md) (2 shared connections)
- [ChatModel Protocol](ChatModel_Protocol.md) (2 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/grounding.py`
- `src/osc_assistant/ingestion/parsers.py`
- `src/osc_assistant/providers/llm/gemini.py`
- `src/osc_assistant/types.py`
- `tests/conftest.py`

## Audit Trail

- EXTRACTED: 177 (91%)
- INFERRED: 17 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*