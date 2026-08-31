# Chunker Registration

> 23 nodes

## Key Concepts

- **llm/openai_compatible.py** (29 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.stream()** (14 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **OpenAICompatibleChatModel** (9 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.complete()** (9 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **llm/__init__.py** (6 connections) — `src/osc_assistant/providers/llm/__init__.py`
- **._build_payload()** (6 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **_Preset** (3 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **OpenAICompatibleOptions** (3 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **Any** (3 connections)
- **_resolve_key()** (3 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.aclose()** (2 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **_make_factory()** (2 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **Chat model providers. Imported for registration side effects.** (1 connections) — `src/osc_assistant/providers/llm/__init__.py`
- **BaseModel** (1 connections)
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.supports_citations()** (1 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **StreamEvent** (1 connections)
- **Chat provider for any OpenAI-compatible endpoint. One adapter covers OpenAI,…** (1 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **Defaults for one OpenAI-compatible service.** (1 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **Adapter over the `/v1/chat/completions` interface.** (1 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **Release the underlying HTTP client. `Container.shutdown()` probes every…** (1 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **Stream text, resolving citations from the accumulated answer at the end.…** (1 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (11 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (11 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (10 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (7 shared connections)
- [Regression Gate Tests](Regression_Gate_Tests.md) (3 shared connections)
- [Conversation Turn Orchestration](Conversation_Turn_Orchestration.md) (1 shared connections)
- [Logging Tests](Logging_Tests.md) (1 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (1 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/llm/__init__.py`
- `src/osc_assistant/providers/llm/openai_compatible.py`

## Audit Trail

- EXTRACTED: 104 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*