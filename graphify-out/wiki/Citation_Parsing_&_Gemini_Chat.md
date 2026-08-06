# Citation Parsing & Gemini Chat

> 42 nodes · cohesion 0.10

## Key Concepts

- **ChatRequest** (59 connections) — `src/osc_assistant/types.py`
- **Usage** (29 connections) — `src/osc_assistant/types.py`
- **llm/gemini.py** (28 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **TextDelta** (23 connections) — `src/osc_assistant/types.py`
- **parse_marker_citations()** (21 connections) — `src/osc_assistant/grounding.py`
- **FailingChatModel** (20 connections) — `tests/conftest.py`
- **CitationDelta** (18 connections) — `src/osc_assistant/types.py`
- **StreamEnd** (16 connections) — `src/osc_assistant/types.py`
- **.stream()** (14 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.stream()** (13 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **GeminiChatModel** (9 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.complete()** (9 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.stream()** (8 connections) — `tests/conftest.py`
- **.stream()** (8 connections) — `tests/conftest.py`
- **._build_config()** (7 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.stream()** (7 connections) — `tests/test_server_lifecycle.py`
- **_build_contents()** (6 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.complete()** (5 connections) — `tests/conftest.py`
- **Any** (4 connections)
- **.complete()** (4 connections) — `tests/conftest.py`
- **_finish_reason()** (3 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.stream()** (3 connections) — `tests/conftest.py`
- **StreamEvent** (3 connections)
- **Extract citations from `[n]` markers in `text`. Markers referring to a source…** (1 connections) — `src/osc_assistant/grounding.py`
- *... and 17 more nodes in this community*

## Relationships

- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (21 shared connections)
- [Grounded Prompt & LangChain Chat](Grounded_Prompt_%26_LangChain_Chat.md) (20 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (20 shared connections)
- [OpenAI-Compatible Chat Provider](OpenAI-Compatible_Chat_Provider.md) (14 shared connections)
- [Anthropic Adapter & Retrieval Pipeline](Anthropic_Adapter_%26_Retrieval_Pipeline.md) (13 shared connections)
- [Citations & Native Citation Model](Citations_%26_Native_Citation_Model.md) (9 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (7 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (7 shared connections)
- [Citation Grounding & Reasoning Models](Citation_Grounding_%26_Reasoning_Models.md) (6 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (6 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (6 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (6 shared connections)

## Source Files

- `src/osc_assistant/grounding.py`
- `src/osc_assistant/providers/llm/gemini.py`
- `src/osc_assistant/providers/llm/openai_compatible.py`
- `src/osc_assistant/types.py`
- `tests/conftest.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 289 (85%)
- INFERRED: 51 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*