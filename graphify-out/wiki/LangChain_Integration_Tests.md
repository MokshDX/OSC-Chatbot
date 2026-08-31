# LangChain Integration Tests

> 32 nodes

## Key Concepts

- **ChatRequest** (57 connections) — `src/osc_assistant/types.py`
- **ProviderError** (33 connections) — `src/osc_assistant/errors.py`
- **llm/gemini.py** (28 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **_ExplodingChatModel** (23 connections) — `tests/test_server_lifecycle.py`
- **.stream()** (13 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **compose_grounded_system()** (10 connections) — `src/osc_assistant/grounding.py`
- **GeminiChatModel** (9 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.complete()** (9 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **._build_config()** (7 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.stream()** (7 connections) — `tests/test_server_lifecycle.py`
- **_build_contents()** (6 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.stream()** (4 connections) — `src/osc_assistant/protocols.py`
- **Any** (4 connections)
- **.complete()** (4 connections) — `tests/test_server_lifecycle.py`
- **_finish_reason()** (3 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **An upstream provider (LLM, embeddings, reranker) failed.** (1 connections) — `src/osc_assistant/errors.py`
- **Fold the system prompt, citation instruction and sources into one string. Used…** (1 connections) — `src/osc_assistant/grounding.py`
- **StreamEvent** (1 connections)
- **Generate a response incrementally.** (1 connections) — `src/osc_assistant/protocols.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.supports_citations()** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **StreamEvent** (1 connections)
- **Google Gemini chat provider (native SDK). Gemini also exposes an OpenAI-…** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **Adapter over `google-genai`'s async models interface.** (1 connections) — `src/osc_assistant/providers/llm/gemini.py`
- *... and 7 more nodes in this community*

## Relationships

- [Recursive Chunker](Recursive_Chunker.md) (25 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (18 shared connections)
- [Logging Tests](Logging_Tests.md) (11 shared connections)
- [Chunker Registration](Chunker_Registration.md) (10 shared connections)
- [Conversation Turn Orchestration](Conversation_Turn_Orchestration.md) (7 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (6 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (6 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (5 shared connections)
- [Evaluation Framework Rationale](Evaluation_Framework_Rationale.md) (5 shared connections)
- [Lifecycle Release Doubles](Lifecycle_Release_Doubles.md) (4 shared connections)
- [Regression Gate Tests](Regression_Gate_Tests.md) (4 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (4 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/grounding.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/llm/gemini.py`
- `src/osc_assistant/types.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 203 (85%)
- INFERRED: 35 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*