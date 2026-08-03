"""Reasoning-model output handling in the OpenAI-compatible adapter.

Hybrid reasoning models (Qwen3, and anything served by vLLM or llama.cpp with a
thinking template) spend completion tokens before producing an answer, and some
servers return that reasoning inline in `content` rather than in a separate field.
Two consequences have to be handled at the adapter, because everything above it
treats the response as the answer:

1. A `[n]` marker written while thinking aloud is not a citation.
2. A budget consumed entirely by reasoning yields empty text, which the answerer
   would otherwise finalise as an uncited answer — telling the user the corpus
   lacks the information when the real cause is the token budget.
"""

from __future__ import annotations

import pytest

from osc_assistant.errors import ProviderError
from osc_assistant.grounding import require_answer, strip_reasoning


def test_leading_think_block_is_removed() -> None:
    raw = (
        "<think>The user asks about leave. Source [2] mentions it.</think>"
        "Employees get 26 days [1]."
    )

    assert strip_reasoning(raw) == "Employees get 26 days [1]."


def test_think_block_with_surrounding_whitespace_is_removed() -> None:
    assert strip_reasoning("\n  <think>\nhmm\n</think>\n\nAnswer text.") == "Answer text."


def test_unclosed_think_block_collapses_to_empty() -> None:
    """A block that never closes means the budget ran out mid-thought."""
    assert strip_reasoning("<think>I should check the leave policy and then") == ""


def test_answer_without_reasoning_is_untouched() -> None:
    answer = "Employees accrue 26 days of annual leave [1]."

    assert strip_reasoning(answer) == answer


def test_think_tag_later_in_the_answer_is_preserved() -> None:
    """The pattern is anchored to the start deliberately: a source document about
    reasoning models can legitimately quote the tag, and silently deleting the
    rest of the answer would corrupt content the model is citing."""
    answer = "The template uses <think> to open a reasoning block [1]."

    assert strip_reasoning(answer) == answer


def test_exhausted_budget_raises_an_actionable_error() -> None:
    with pytest.raises(ProviderError, match="completion budget was exhausted"):
        require_answer("", "length", "ollama")


def test_empty_completion_for_another_reason_still_raises() -> None:
    with pytest.raises(ProviderError, match="empty completion"):
        require_answer("", "stop", "ollama")


def test_non_empty_answer_passes_through() -> None:
    assert require_answer("An answer [1].", "stop", "ollama") == "An answer [1]."


def test_reasoning_markers_never_become_citations() -> None:
    """The end-to-end property: markers are parsed from the stripped answer only."""
    from osc_assistant.grounding import parse_marker_citations
    from osc_assistant.types import SourceDocument

    sources = [
        SourceDocument(
            chunk_id=f"c{n}", document_id=f"d{n}", title=f"T{n}", source_uri="file:///x", text="t"
        )
        for n in (1, 2, 3)
    ]
    raw = "<think>Maybe [2] or [3] is relevant.</think>The limit is 180 EUR [1]."

    citations = parse_marker_citations(strip_reasoning(raw), sources)

    assert [citation.index for citation in citations] == [1]
