# Grounding & OpenAI-Compatible Chat

> 32 nodes

## Key Concepts

- **grounding.py** (18 connections) — `src/osc_assistant/grounding.py`
- **strip_reasoning()** (14 connections) — `src/osc_assistant/grounding.py`
- **.stream()** (14 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **require_answer()** (12 connections) — `src/osc_assistant/grounding.py`
- **test_reasoning_models.py** (12 connections) — `tests/test_reasoning_models.py`
- **OpenAICompatibleChatModel** (9 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.complete()** (9 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **._build_payload()** (6 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **Any** (3 connections)
- **test_unclosed_think_block_collapses_to_empty()** (3 connections) — `tests/test_reasoning_models.py`
- **test_think_tag_later_in_the_answer_is_preserved()** (3 connections) — `tests/test_reasoning_models.py`
- **.aclose()** (2 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **_make_factory()** (2 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **test_leading_think_block_is_removed()** (2 connections) — `tests/test_reasoning_models.py`
- **test_think_block_with_surrounding_whitespace_is_removed()** (2 connections) — `tests/test_reasoning_models.py`
- **test_answer_without_reasoning_is_untouched()** (2 connections) — `tests/test_reasoning_models.py`
- **test_exhausted_budget_raises_an_actionable_error()** (2 connections) — `tests/test_reasoning_models.py`
- **test_empty_completion_for_another_reason_still_raises()** (2 connections) — `tests/test_reasoning_models.py`
- **test_non_empty_answer_passes_through()** (2 connections) — `tests/test_reasoning_models.py`
- **Grounding and citation handling for providers without native citation support.…** (1 connections) — `src/osc_assistant/grounding.py`
- **Remove a leading `<think>` block from a reasoning model's answer. Ollama…** (1 connections) — `src/osc_assistant/grounding.py`
- **Fail loudly when the model produced no answer text. An empty completion…** (1 connections) — `src/osc_assistant/grounding.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.supports_citations()** (1 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- *... and 7 more nodes in this community*

## Relationships

- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (10 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (9 shared connections)
- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (9 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (7 shared connections)
- [Rank Fusion & Source Rendering](Rank_Fusion_%26_Source_Rendering.md) (6 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (2 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (1 shared connections)

## Source Files

- `src/osc_assistant/grounding.py`
- `src/osc_assistant/providers/llm/openai_compatible.py`
- `tests/test_reasoning_models.py`

## Audit Trail

- EXTRACTED: 136 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*