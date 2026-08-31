# VectorStore Protocol

> 20 nodes

## Key Concepts

- **grounding.py** (18 connections) — `src/osc_assistant/grounding.py`
- **strip_reasoning()** (14 connections) — `src/osc_assistant/grounding.py`
- **require_answer()** (12 connections) — `src/osc_assistant/grounding.py`
- **test_reasoning_models.py** (12 connections) — `tests/test_reasoning_models.py`
- **_escape()** (3 connections) — `src/osc_assistant/grounding.py`
- **test_unclosed_think_block_collapses_to_empty()** (3 connections) — `tests/test_reasoning_models.py`
- **test_think_tag_later_in_the_answer_is_preserved()** (3 connections) — `tests/test_reasoning_models.py`
- **test_leading_think_block_is_removed()** (2 connections) — `tests/test_reasoning_models.py`
- **test_think_block_with_surrounding_whitespace_is_removed()** (2 connections) — `tests/test_reasoning_models.py`
- **test_answer_without_reasoning_is_untouched()** (2 connections) — `tests/test_reasoning_models.py`
- **test_exhausted_budget_raises_an_actionable_error()** (2 connections) — `tests/test_reasoning_models.py`
- **test_empty_completion_for_another_reason_still_raises()** (2 connections) — `tests/test_reasoning_models.py`
- **test_non_empty_answer_passes_through()** (2 connections) — `tests/test_reasoning_models.py`
- **Grounding and citation handling for providers without native citation support.…** (1 connections) — `src/osc_assistant/grounding.py`
- **Remove a leading `<think>` block from a reasoning model's answer. Ollama…** (1 connections) — `src/osc_assistant/grounding.py`
- **Fail loudly when the model produced no answer text. An empty completion…** (1 connections) — `src/osc_assistant/grounding.py`
- **Escape the characters that would otherwise break out of an XML-ish attribute.** (1 connections) — `src/osc_assistant/grounding.py`
- **Reasoning-model output handling in the OpenAI-compatible adapter. Hybrid…** (1 connections) — `tests/test_reasoning_models.py`
- **A block that never closes means the budget ran out mid-thought.** (1 connections) — `tests/test_reasoning_models.py`
- **The pattern is anchored to the start deliberately: a source document about…** (1 connections) — `tests/test_reasoning_models.py`

## Relationships

- [Regression Gate Tests](Regression_Gate_Tests.md) (7 shared connections)
- [Logging Tests](Logging_Tests.md) (7 shared connections)
- [Chunker Registration](Chunker_Registration.md) (7 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (5 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (3 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (1 shared connections)

## Source Files

- `src/osc_assistant/grounding.py`
- `tests/test_reasoning_models.py`

## Audit Trail

- EXTRACTED: 84 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*