# Logging Tests

> 29 nodes

## Key Concepts

- **llm/langchain_bridge.py** (34 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.stream()** (17 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.complete()** (13 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **LangChainChatModel** (12 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **Any** (7 connections)
- **_to_langchain_messages()** (7 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **._bind()** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_instantiate()** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_text_of()** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.text()** (5 connections) — `src/osc_assistant/ingestion/parsers.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_stop_reason()** (5 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_reported_model()** (3 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **.supports_citations()** (2 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **The collected text, with each block element on its own line.** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **StreamEvent** (1 connections)
- **register** (1 connections)
- **Chat provider backed by any LangChain `BaseChatModel`. **Why this exists.** OSC…** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **Adapter presenting a LangChain chat model as an OSC `ChatModel`. Translation…** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **False: LangChain normalises provider responses to a common message shape.…** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **Stream text, resolving citations once the full answer is known. Markers can…** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **Apply the per-request generation parameters. `bind` rather than constructor…** (1 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- *... and 4 more nodes in this community*

## Relationships

- [LangChain Integration Tests](LangChain_Integration_Tests.md) (11 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (11 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (9 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (7 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (6 shared connections)
- [Regression Gate Tests](Regression_Gate_Tests.md) (3 shared connections)
- [FastAPI Routes & Session Endpoints](FastAPI_Routes_%26_Session_Endpoints.md) (2 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (2 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (2 shared connections)
- [Chunker Registration](Chunker_Registration.md) (1 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (1 shared connections)

## Source Files

- `src/osc_assistant/ingestion/parsers.py`
- `src/osc_assistant/providers/llm/langchain_bridge.py`

## Audit Trail

- EXTRACTED: 146 (98%)
- INFERRED: 3 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*