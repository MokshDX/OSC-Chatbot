"""Answer generation: the composition of retrieval and a chat model.

This is the only place that decides *when the assistant should decline to answer*,
which is the system's main defence against confident wrong answers:

* No retrieval hits -> abstain without calling the model at all. Cheap, and
  correct: with nothing to ground an answer in, generating one is guessing.
* An answer with no citations -> treated as ungrounded. Whether that becomes an
  abstention is controlled by `generation.require_citations`.

Streaming contract: text deltas are provisional and `AnswerComplete` is
authoritative. When `AnswerComplete.answer.abstained` is true, the client must
replace what it rendered. This keeps the abstention policy identical in both
modes; a policy that only worked when not streaming would be worse than none.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass

from ..logging import get_logger
from ..protocols import ChatModel
from ..retrieval import RetrievalPipeline, RetrievalResult
from ..settings import GenerationSettings
from ..types import (
    Answer,
    ChatRequest,
    Citation,
    CitationDelta,
    Message,
    Role,
    StreamEnd,
    TextDelta,
    Usage,
)
from .prompts import ANSWER_SYSTEM_PROMPT

log = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class RetrievalReady:
    """Emitted before generation so the client can render sources immediately."""

    result: RetrievalResult


@dataclass(frozen=True, slots=True)
class AnswerComplete:
    """The authoritative final answer."""

    answer: Answer


type AnswerEvent = RetrievalReady | TextDelta | CitationDelta | AnswerComplete


class Answerer:
    """Answers a question against the indexed corpus."""

    def __init__(
        self,
        retrieval: RetrievalPipeline,
        model: ChatModel,
        settings: GenerationSettings,
    ) -> None:
        self._retrieval = retrieval
        self._model = model
        self._settings = settings

    async def answer(self, question: str, history: list[Message] | None = None) -> Answer:
        """Answer `question`, returning the complete result."""
        history = history or []
        retrieval = await self._retrieval.retrieve(question, history)

        if not retrieval.chunks:
            return self._abstention(retrieval)

        response = await self._model.complete(
            self._build_request(question, history, retrieval)
        )
        return self._finalise(
            text=response.text,
            citations=response.citations,
            retrieval=retrieval,
            usage=response.usage,
            model=response.model or self._model.model_id,
        )

    async def stream(
        self, question: str, history: list[Message] | None = None
    ) -> AsyncIterator[AnswerEvent]:
        """Answer `question`, emitting events as they become available."""
        history = history or []
        retrieval = await self._retrieval.retrieve(question, history)
        yield RetrievalReady(result=retrieval)

        if not retrieval.chunks:
            yield AnswerComplete(answer=self._abstention(retrieval))
            return

        request = self._build_request(question, history, retrieval)
        parts: list[str] = []
        citations: list[Citation] = []
        usage = Usage()

        async for event in self._model.stream(request):
            match event:
                case TextDelta():
                    parts.append(event.text)
                    yield event
                case CitationDelta():
                    citations.append(event.citation)
                    yield event
                case StreamEnd():
                    usage = event.usage

        yield AnswerComplete(
            answer=self._finalise(
                text="".join(parts),
                citations=citations,
                retrieval=retrieval,
                usage=usage,
                model=self._model.model_id,
            )
        )

    def _build_request(
        self, question: str, history: list[Message], retrieval: RetrievalResult
    ) -> ChatRequest:
        return ChatRequest(
            messages=[*history, Message(role=Role.USER, content=question)],
            system=ANSWER_SYSTEM_PROMPT,
            sources=retrieval.as_sources(),
            max_tokens=self._settings.max_tokens,
            temperature=self._settings.temperature,
        )

    def _abstention(self, retrieval: RetrievalResult) -> Answer:
        log.info("generation.abstained", extra={"reason": "no_sources", "query": retrieval.query})
        return Answer(
            text=self._settings.abstention_message,
            citations=[],
            retrieved=[],
            usage=Usage(),
            model=self._model.model_id,
            abstained=True,
        )

    def _finalise(
        self,
        *,
        text: str,
        citations: list[Citation],
        retrieval: RetrievalResult,
        usage: Usage,
        model: str,
    ) -> Answer:
        """Apply the citation policy and assemble the final answer."""
        ungrounded = self._settings.require_citations and not citations
        if ungrounded:
            log.warning(
                "generation.uncited_answer",
                extra={
                    "query": retrieval.query,
                    "chunk_ids": [hit.chunk.id for hit in retrieval.chunks],
                },
            )

        log.info(
            "generation.complete",
            extra={
                "model": model,
                "query": retrieval.query,
                "citations": len(citations),
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "cached_input_tokens": usage.cached_input_tokens,
            },
        )

        return Answer(
            text=self._settings.abstention_message if ungrounded else text,
            citations=citations,
            retrieved=retrieval.chunks,
            usage=usage,
            model=model,
            abstained=ungrounded,
        )
