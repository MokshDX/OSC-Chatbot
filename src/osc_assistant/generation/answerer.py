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

import time
from collections.abc import AsyncIterator
from dataclasses import dataclass

from ..logging import audit, get_logger
from ..observability import annotate, current_trace_id, span, trace
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


def _annotate_generation(usage: Usage, stop_reason: str | None, citations: int) -> None:
    """Record what the model call cost and how it ended.

    `stop_reason` is here because a truncated answer and a complete one are
    indistinguishable from the text alone, and truncation is the most common cause
    of a good retrieval producing a bad answer on a small-context local model.
    """
    annotate(
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        cached_input_tokens=usage.cached_input_tokens,
        stop_reason=stop_reason,
        citations=citations,
    )


def _annotate_abstention(reason: str) -> None:
    annotate(abstained=True, abstention_reason=reason)


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

        with trace("answer", mode="buffered", model=self._model.model_id, turns=len(history)):
            retrieval = await self._retrieval.retrieve(question, history)

            if not retrieval.chunks:
                return self._abstention(retrieval)

            with span("generate", model=self._model.model_id, sources=len(retrieval.chunks)):
                response = await self._model.complete(
                    self._build_request(question, history, retrieval)
                )
                _annotate_generation(response.usage, response.stop_reason, len(response.citations))

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

        with trace("answer", mode="stream", model=self._model.model_id, turns=len(history)):
            retrieval = await self._retrieval.retrieve(question, history)
            yield RetrievalReady(result=retrieval)

            if not retrieval.chunks:
                yield AnswerComplete(answer=self._abstention(retrieval))
                return

            request = self._build_request(question, history, retrieval)
            parts: list[str] = []
            citations: list[Citation] = []
            usage = Usage()

            # The generate span opens before the first delta and closes after the
            # last, so its duration is the whole streamed generation. Time to first
            # token is recorded separately, because for a streaming client that is
            # the number that describes the experience and total duration is not.
            with span(
                "generate", model=self._model.model_id, sources=len(retrieval.chunks)
            ) as stage:
                started = time.perf_counter()
                first_delta_at: float | None = None
                stop_reason: str | None = None

                async for event in self._model.stream(request):
                    match event:
                        case TextDelta():
                            if first_delta_at is None:
                                first_delta_at = time.perf_counter()
                            parts.append(event.text)
                            yield event
                        case CitationDelta():
                            citations.append(event.citation)
                            yield event
                        case StreamEnd():
                            usage = event.usage
                            stop_reason = event.stop_reason

                stage.set(
                    deltas=len(parts),
                    time_to_first_token_ms=(
                        round((first_delta_at - started) * 1000, 2)
                        if first_delta_at is not None
                        else None
                    ),
                )
                _annotate_generation(usage, stop_reason, len(citations))

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
        # No `generate` span is opened, and that absence is the point: a trace with
        # a `retrieve` and no `generate` is the visible signature of an abstention,
        # distinguishable at a glance from a model that answered badly.
        _annotate_abstention("no_sources")
        log.info("generation.abstained", extra={"reason": "no_sources", "query": retrieval.query})
        answer = Answer(
            text=self._settings.abstention_message,
            citations=[],
            retrieved=[],
            usage=Usage(),
            model=self._model.model_id,
            abstained=True,
            trace_id=retrieval.trace_id or current_trace_id(),
        )
        _audit_answer(answer, retrieval)
        return answer

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
            _annotate_abstention("uncited_answer")
            log.warning(
                "generation.uncited_answer",
                extra={
                    "query": retrieval.query,
                    "chunk_ids": [hit.chunk.id for hit in retrieval.chunks],
                },
            )

        with span("finalise", require_citations=self._settings.require_citations) as stage:
            stage.set(
                citations=len(citations),
                cited_chunk_ids=[citation.chunk_id for citation in citations],
                # Which retrieved passages the model actually used. A high
                # retrieval count with one cited source is the signature of an
                # over-wide top_k, and it is invisible without this.
                sources_used=len({citation.chunk_id for citation in citations}),
                sources_offered=len(retrieval.chunks),
                abstained=ungrounded,
                answer_chars=len(text),
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
                "trace_id": retrieval.trace_id,
            },
        )

        answer = Answer(
            text=self._settings.abstention_message if ungrounded else text,
            citations=citations,
            retrieved=retrieval.chunks,
            usage=usage,
            model=model,
            abstained=ungrounded,
            trace_id=retrieval.trace_id or current_trace_id(),
        )
        _audit_answer(answer, retrieval)
        return answer


def _audit_answer(answer: Answer, retrieval: RetrievalResult) -> None:
    """Write one durable record of a question this system answered.

    Separate from `generation.complete`, which is operational and rotates with the
    debug stream. This goes to `audit.log`, whose retention is deliberately longer,
    because "which passages did we show, and what did we say" is the question asked
    months later by someone who is not debugging.

    The record carries the *skeleton* by default — retrieved and cited chunk ids,
    documents, model, tokens, abstention, trace id — and the question and answer
    text only when `logging.capture_payloads` is on. That default is the security
    trade: chunk ids make an answer fully reconstructable via `./osc chunk <id>` by
    someone with access to the index, without putting corpus content in a file that
    tends to get shipped somewhere else.
    """
    audit(
        "answer",
        trace_id=answer.trace_id,
        model=answer.model,
        abstained=answer.abstained,
        question=retrieval.original_query,
        query=retrieval.query,
        answer=answer.text,
        answer_chars=len(answer.text),
        retrieved_chunk_ids=[hit.chunk.id for hit in answer.retrieved],
        retrieved_documents=sorted({hit.chunk.document_id for hit in answer.retrieved}),
        cited_chunk_ids=[citation.chunk_id for citation in answer.citations],
        citations=len(answer.citations),
        input_tokens=answer.usage.input_tokens,
        output_tokens=answer.usage.output_tokens,
        retrieval_ms=round(retrieval.duration_seconds * 1000, 2),
    )
