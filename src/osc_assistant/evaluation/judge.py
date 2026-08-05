"""LLM-as-judge faithfulness scoring.

Faithfulness asks whether every claim in an answer is supported by the passages the
answer was built from. Unlike recall, MRR or groundedness, it cannot be computed
from ids and set arithmetic — it is a reading-comprehension judgement over natural
language — so it is the one metric in this package that costs a model call.

**Why this is opt-in.** It doubles the number of generations in a run, and it
measures with an instrument made of the same material as the thing being measured.
The deterministic metrics (`groundedness`, `fact_match`, `recall`) are what gate
CI, because a gate that can change its mind between two runs of the same commit is
not a gate. Faithfulness is for depth: it is how the citation-strength gap in
PROJECT_STATUS.md §10 — Anthropic's verified citations versus every other
provider's `[n]` markers — gets a number rather than a caveat.

**Why the judge is a `ChatModel`.** It goes through the same protocol as every
other model in the system, so the judge can be a *different, stronger* provider
than the system under test purely by configuration (`--judge-profile`). Judging an
8B local model's output with the same 8B local model would mostly measure whether
it agrees with itself.

Known limitation, stated rather than hidden: an LLM judge is a biased estimator. It
is used here as a relative measure between two runs of the same golden set with the
same judge, which is a comparison it is good at, and not as an absolute claim that
"94% of answers are faithful". See Zheng et al., *Judging LLM-as-a-Judge*
(NeurIPS 2023): https://arxiv.org/abs/2306.05685
"""

from __future__ import annotations

from collections.abc import Sequence

from ..logging import get_logger
from ..protocols import ChatModel
from ..types import ChatRequest, Message, Role, ScoredChunk

log = get_logger(__name__)

# Frozen, for the same reason `generation/prompts.py` is frozen: a judge whose
# prompt drifts produces scores that cannot be compared across runs, which defeats
# the only purpose the number has.
JUDGE_SYSTEM_PROMPT = """\
You are evaluating whether an answer is faithful to the source passages it was \
given. An answer is faithful when every factual claim it makes is stated in, or \
directly entailed by, the passages. An answer is unfaithful if it adds a fact the \
passages do not contain, changes a number, or contradicts a passage.

Judge only faithfulness to the passages. Do not judge whether the answer is helpful, \
well written, or complete. Do not use knowledge of your own.

Reply with exactly one word: SUPPORTED or UNSUPPORTED."""

JUDGE_TEMPLATE = """\
QUESTION:
{question}

PASSAGES:
{passages}

ANSWER:
{answer}

Is every factual claim in the ANSWER supported by the PASSAGES? \
Reply with exactly one word: SUPPORTED or UNSUPPORTED."""


class FaithfulnessJudge:
    """Scores one answer against the passages it was generated from."""

    def __init__(self, model: ChatModel, *, max_tokens: int = 16) -> None:
        self._model = model
        # A one-word verdict needs almost no budget, and capping it is what stops a
        # reasoning model from spending a thousand tokens per case deliberating.
        self._max_tokens = max_tokens

    async def is_faithful(
        self, question: str, answer: str, sources: Sequence[ScoredChunk]
    ) -> bool | None:
        """Return True, False, or None when the judge could not be reached.

        `None` rather than a default: recording an unreachable judge as "faithful"
        would inflate the metric on exactly the runs where something was wrong, and
        recording it as "unfaithful" would blame the system under test for a
        failure in the instrument. `summarise` excludes `None` from the mean.
        """
        passages = "\n\n".join(
            f"[{index}] {hit.chunk.title}\n{hit.chunk.text}"
            for index, hit in enumerate(sources, start=1)
        )
        if not passages:
            return None

        request = ChatRequest(
            messages=[
                Message(
                    role=Role.USER,
                    content=JUDGE_TEMPLATE.format(
                        question=question, passages=passages, answer=answer
                    ),
                )
            ],
            system=JUDGE_SYSTEM_PROMPT,
            max_tokens=self._max_tokens,
            temperature=0.0,
        )

        try:
            response = await self._model.complete(request)
        # Broad: a judge failure is an instrument failure and must never be able to
        # fail the run it is measuring. The case keeps every deterministic score it
        # already has and simply carries no verdict.
        except Exception as exc:
            log.warning("evaluation.judge_failed", extra={"error": str(exc)})
            return None

        return _parse_verdict(response.text)


def _parse_verdict(text: str) -> bool | None:
    """Read a one-word verdict out of whatever the model actually returned.

    Substring matching rather than equality because models prepend acknowledgements
    and append full stops, and a strict parser would score a correctly-judged run
    as unjudgeable. `UNSUPPORTED` is checked first: it contains `SUPPORTED`.
    """
    upper = text.strip().upper()
    if "UNSUPPORTED" in upper:
        return False
    if "SUPPORTED" in upper:
        return True
    log.warning("evaluation.judge_unparseable", extra={"reply": text[:120]})
    return None
