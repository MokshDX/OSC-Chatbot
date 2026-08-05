# Chat Request & Response Types

> 28 nodes

## Key Concepts

- **ChatRequest** (59 connections) — `src/osc_assistant/types.py`
- **ChatResponse** (28 connections) — `src/osc_assistant/types.py`
- **TextDelta** (23 connections) — `src/osc_assistant/types.py`
- **FailingChatModel** (23 connections) — `tests/conftest.py`
- **CitationDelta** (18 connections) — `src/osc_assistant/types.py`
- **NativeCitationChatModel** (18 connections) — `tests/conftest.py`
- **StreamEnd** (16 connections) — `src/osc_assistant/types.py`
- **Citation** (15 connections) — `src/osc_assistant/types.py`
- **.stream()** (8 connections) — `tests/conftest.py`
- **.stream()** (8 connections) — `tests/conftest.py`
- **.complete()** (4 connections) — `src/osc_assistant/protocols.py`
- **.complete()** (4 connections) — `tests/conftest.py`
- **.complete()** (4 connections) — `tests/conftest.py`
- **.complete()** (4 connections) — `tests/test_server_lifecycle.py`
- **StreamEvent** (3 connections)
- **.stream()** (3 connections) — `tests/conftest.py`
- **Generate a complete response.** (1 connections) — `src/osc_assistant/protocols.py`
- **A reference from the answer back to the material that supports it. `index` is…** (1 connections) — `src/osc_assistant/types.py`
- **A provider-neutral generation request. `sources`, when present, is grounding…** (1 connections) — `src/osc_assistant/types.py`
- **An incremental fragment of the answer.** (1 connections) — `src/osc_assistant/types.py`
- **A citation resolved mid-stream.** (1 connections) — `src/osc_assistant/types.py`
- **.__init__()** (1 connections) — `tests/conftest.py`
- **.model_id()** (1 connections) — `tests/conftest.py`
- **.supports_citations()** (1 connections) — `tests/conftest.py`
- **.model_id()** (1 connections) — `tests/conftest.py`
- *... and 3 more nodes in this community*

## Relationships

- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (22 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (22 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (14 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (14 shared connections)
- [Grounding & OpenAI-Compatible Chat](Grounding_%26_OpenAI-Compatible_Chat.md) (9 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (9 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (7 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (7 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (6 shared connections)
- [Settings Schema](Settings_Schema.md) (6 shared connections)
- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (6 shared connections)
- [ChatModel Protocol](ChatModel_Protocol.md) (4 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`
- `src/osc_assistant/types.py`
- `tests/conftest.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 184 (74%)
- INFERRED: 66 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*