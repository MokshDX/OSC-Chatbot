# Conversation Turn Orchestration

> 25 nodes

## Key Concepts

- **anthropic_provider.py** (27 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.stream()** (11 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **AnthropicChatModel** (10 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.complete()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_build_messages()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_parse_content()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **._build_payload()** (6 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Any** (5 connections)
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **AnthropicOptions** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_last_user_index()** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.aclose()** (2 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **BaseModel** (1 connections)
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.supports_citations()** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **StreamEvent** (1 connections)
- **register** (1 connections)
- **Anthropic chat provider. This is the only adapter with native citation support:…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Adapter over the Anthropic Messages API. Satisfies `protocols.ChatModel`…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Release the underlying HTTP client. See `Container.shutdown()`.** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Stream the answer, then emit citations once the message is complete. Text is…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Attach sources as citable documents on the final user turn. Sources belong to…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Flatten response blocks into text, appending a marker after each cited span.…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`

## Relationships

- [Recursive Chunker](Recursive_Chunker.md) (12 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (7 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (7 shared connections)
- [Regression Gate Tests](Regression_Gate_Tests.md) (3 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (2 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (2 shared connections)
- [Evaluation Runner Tests](Evaluation_Runner_Tests.md) (2 shared connections)
- [Chunker Registration](Chunker_Registration.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/llm/anthropic_provider.py`

## Audit Trail

- EXTRACTED: 112 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*