"""Conversational query rewriting.

"What about the second one?" is not a searchable query. Rewriting resolves
pronouns and ellipsis against the conversation so retrieval sees a standalone
question, which is the difference between working and useless follow-up turns.

Runs on the configured *fast* model, since it sits on the critical path before
retrieval. It is also strictly best-effort: any failure falls back to the original
question, because a slightly worse query beats a failed request.
"""

from __future__ import annotations

from collections.abc import Sequence

from ..logging import get_logger
from ..observability import annotate
from ..protocols import ChatModel
from ..types import ChatRequest, Message, Role

log = get_logger(__name__)

MAX_HISTORY_TURNS = 6

_SYSTEM_PROMPT = """\
You rewrite the final user message into a standalone search query.

Rules:
- Resolve pronouns and references using the conversation.
- Keep the user's own terminology, product names, acronyms and error codes verbatim.
- Output only the rewritten query. No preamble, no quotes, no explanation.
- If the message is already standalone, output it unchanged."""


class QueryRewriter:
    """Turns a conversational turn into a standalone retrieval query."""

    def __init__(self, model: ChatModel, max_tokens: int = 256) -> None:
        self._model = model
        self._max_tokens = max_tokens

    @property
    def model_id(self) -> str:
        """The model doing the rewriting, for traces and logs."""
        return self._model.model_id

    async def rewrite(self, question: str, history: Sequence[Message]) -> str:
        """Return a standalone form of `question`.

        With no prior turns there is nothing to resolve, so the question is
        returned untouched and no request is made.
        """
        if not history:
            annotate(skipped="no_history")
            return question

        transcript = _format_history(history[-MAX_HISTORY_TURNS:])
        prompt = f"Conversation so far:\n{transcript}\n\nFinal user message:\n{question}"

        try:
            response = await self._model.complete(
                ChatRequest(
                    messages=[Message(role=Role.USER, content=prompt)],
                    system=_SYSTEM_PROMPT,
                    max_tokens=self._max_tokens,
                )
            )
        # Broad by intent: rewriting is an optimisation. Any failure degrades to
        # the original question rather than failing the user's request.
        except Exception as exc:
            # Visible in the trace as an attribute rather than an error: the stage
            # succeeded at its contract (it produced a usable query), it just did
            # so by falling back. A trace that showed this as a failure would send
            # someone debugging the wrong thing.
            annotate(fallback="provider_error", error=str(exc))
            log.warning("rewrite.failed", extra={"error": str(exc)})
            return question

        rewritten = response.text.strip()
        if not rewritten:
            annotate(fallback="empty_response")
            return question

        log.info(
            "rewrite.complete",
            extra={"original": question, "rewritten": rewritten},
        )
        return rewritten


def _format_history(history: Sequence[Message]) -> str:
    return "\n".join(f"{message.role.value}: {message.content}" for message in history)
