# ChatModel Protocol

> 12 nodes

## Key Concepts

- **ChatModel** (33 connections) — `src/osc_assistant/protocols.py`
- **.stream()** (4 connections) — `src/osc_assistant/protocols.py`
- **.fast_llm()** (3 connections) — `src/osc_assistant/container.py`
- **.llm()** (2 connections) — `src/osc_assistant/container.py`
- **.model_id()** (2 connections) — `src/osc_assistant/protocols.py`
- **.supports_citations()** (2 connections) — `src/osc_assistant/protocols.py`
- **A cheaper model for auxiliary steps such as query rewriting.** (1 connections) — `src/osc_assistant/container.py`
- **StreamEvent** (1 connections)
- **A text-generating model.** (1 connections) — `src/osc_assistant/protocols.py`
- **The provider's identifier for the underlying model, for logs and traces.** (1 connections) — `src/osc_assistant/protocols.py`
- **True if the provider resolves citations itself from structured sources. When…** (1 connections) — `src/osc_assistant/protocols.py`
- **Generate a response incrementally.** (1 connections) — `src/osc_assistant/protocols.py`

## Relationships

- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (4 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (3 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (3 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (2 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (2 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (2 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (2 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (2 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (2 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (1 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (1 shared connections)
- [Store Inspector](Store_Inspector.md) (1 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/protocols.py`

## Audit Trail

- EXTRACTED: 43 (83%)
- INFERRED: 9 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*