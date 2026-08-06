# Citation Grounding & Reasoning Models

> 20 nodes · cohesion 0.15

## Key Concepts

- **grounding.py** (18 connections) — `src/osc_assistant/grounding.py`
- **strip_reasoning()** (14 connections) — `src/osc_assistant/grounding.py`
- **require_answer()** (12 connections) — `src/osc_assistant/grounding.py`
- **test_reasoning_models.py** (12 connections) — `tests/test_reasoning_models.py`
- **test_reasoning_markers_never_become_citations()** (5 connections) — `tests/test_reasoning_models.py`
- **test_think_tag_later_in_the_answer_is_preserved()** (3 connections) — `tests/test_reasoning_models.py`
- **test_unclosed_think_block_collapses_to_empty()** (3 connections) — `tests/test_reasoning_models.py`
- **test_answer_without_reasoning_is_untouched()** (2 connections) — `tests/test_reasoning_models.py`
- **test_empty_completion_for_another_reason_still_raises()** (2 connections) — `tests/test_reasoning_models.py`
- **test_exhausted_budget_raises_an_actionable_error()** (2 connections) — `tests/test_reasoning_models.py`
- **test_leading_think_block_is_removed()** (2 connections) — `tests/test_reasoning_models.py`
- **test_non_empty_answer_passes_through()** (2 connections) — `tests/test_reasoning_models.py`
- **test_think_block_with_surrounding_whitespace_is_removed()** (2 connections) — `tests/test_reasoning_models.py`
- **Grounding and citation handling for providers without native citation support.…** (1 connections) — `src/osc_assistant/grounding.py`
- **Remove a leading `<think>` block from a reasoning model's answer. Ollama…** (1 connections) — `src/osc_assistant/grounding.py`
- **Fail loudly when the model produced no answer text. An empty completion…** (1 connections) — `src/osc_assistant/grounding.py`
- **Reasoning-model output handling in the OpenAI-compatible adapter. Hybrid…** (1 connections) — `tests/test_reasoning_models.py`
- **A block that never closes means the budget ran out mid-thought.** (1 connections) — `tests/test_reasoning_models.py`
- **The pattern is anchored to the start deliberately: a source document about…** (1 connections) — `tests/test_reasoning_models.py`
- **The end-to-end property: markers are parsed from the stripped answer only.** (1 connections) — `tests/test_reasoning_models.py`

## Relationships

- [Grounded Prompt & LangChain Chat](Grounded_Prompt_%26_LangChain_Chat.md) (8 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (6 shared connections)
- [OpenAI-Compatible Chat Provider](OpenAI-Compatible_Chat_Provider.md) (5 shared connections)
- [RRF Fusion & Source Rendering](RRF_Fusion_%26_Source_Rendering.md) (3 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (2 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (2 shared connections)
- [Anthropic Adapter & Retrieval Pipeline](Anthropic_Adapter_%26_Retrieval_Pipeline.md) (2 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (1 shared connections)
- [Citations & Native Citation Model](Citations_%26_Native_Citation_Model.md) (1 shared connections)

## Source Files

- `src/osc_assistant/grounding.py`
- `tests/test_reasoning_models.py`

## Audit Trail

- EXTRACTED: 85 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*