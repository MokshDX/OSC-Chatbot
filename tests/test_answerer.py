"""Answer generation tests.

The abstention policy is the system's main defence against confident wrong
answers, so it is tested explicitly in both the buffered and streaming paths — a
policy that only held when not streaming would be worse than none.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest

from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
from osc_assistant.generation import AnswerComplete, Answerer, RetrievalReady
from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader
from osc_assistant.observability import RECORDER
from osc_assistant.providers.reranking.noop import NoopReranker
from osc_assistant.providers.vectorstores.memory import MemoryVectorStore
from osc_assistant.retrieval import RetrievalPipeline
from osc_assistant.settings import GenerationSettings, RetrievalSettings
from osc_assistant.types import ChatRequest, CitationDelta, Document, StreamEvent, TextDelta

from .conftest import (
    EMBEDDING_DIMENSIONS,
    NativeCitationChatModel,
    StubChatModel,
    StubEmbeddingModel,
)


@pytest.fixture
async def indexed(
    store: MemoryVectorStore, embeddings: StubEmbeddingModel, documents: list[Document]
) -> MemoryVectorStore:
    pipeline = IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
        embeddings=embeddings,
        store=store,
    )
    await pipeline.ingest(InMemoryLoader(documents).load())
    return store


def _answerer(
    store: MemoryVectorStore,
    embeddings: StubEmbeddingModel,
    model: object,
    **generation: object,
) -> Answerer:
    retrieval = RetrievalPipeline(
        store=store,
        embeddings=embeddings,
        reranker=NoopReranker(),
        settings=RetrievalSettings(rewrite_queries=False, top_k=4),
    )
    return Answerer(
        retrieval=retrieval,
        model=model,  # type: ignore[arg-type]
        settings=GenerationSettings(**generation),  # type: ignore[arg-type]
    )


async def test_cited_answer_is_returned_with_its_sources(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    model = StubChatModel(reply="Employees accrue twenty five vacation days. [1]")
    answerer = _answerer(indexed, embeddings, model)

    answer = await answerer.answer("How many vacation days?")

    assert not answer.abstained
    assert len(answer.citations) == 1
    assert answer.citations[0].source_uri.endswith("vacation.md")
    assert answer.retrieved


async def test_sources_are_passed_to_the_model(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    model = StubChatModel()
    answerer = _answerer(indexed, embeddings, model)

    await answerer.answer("How many vacation days?")

    request = model.requests[0]
    assert request.sources, "retrieved chunks must reach the model as grounding"
    assert request.system is not None and "only from the supplied sources" in request.system


async def test_no_retrieval_hits_abstains_without_calling_the_model(
    embeddings: StubEmbeddingModel,
) -> None:
    """Generating from nothing is guessing, so the model is never invoked."""
    model = StubChatModel()
    answerer = _answerer(MemoryVectorStore(dimensions=EMBEDDING_DIMENSIONS), embeddings, model)

    answer = await answerer.answer("What is our policy on submarines?")

    assert answer.abstained
    assert "could not find" in answer.text
    assert model.requests == [], "no tokens should be spent when there is nothing to ground on"


async def test_uncited_answer_is_treated_as_ungrounded(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    model = StubChatModel(reply="I am confident the answer is forty two.")
    answerer = _answerer(indexed, embeddings, model, require_citations=True)

    answer = await answerer.answer("How many vacation days?")

    assert answer.abstained
    assert "forty two" not in answer.text


async def test_citation_requirement_can_be_relaxed(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    model = StubChatModel(reply="An answer with no markers.")
    answerer = _answerer(indexed, embeddings, model, require_citations=False)

    answer = await answerer.answer("How many vacation days?")

    assert not answer.abstained
    assert answer.text == "An answer with no markers."


async def test_native_citation_provider_needs_no_marker_parsing(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    """Both citation paths must produce the same shape for downstream code."""
    answerer = _answerer(indexed, embeddings, NativeCitationChatModel())

    answer = await answerer.answer("How many vacation days?")

    assert not answer.abstained
    assert len(answer.citations) == 1
    assert answer.citations[0].quoted_text, "a native provider supplies the supporting text"


# ---------------------------------------------------------------------- streaming


async def test_stream_emits_sources_before_any_text(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    answerer = _answerer(indexed, embeddings, StubChatModel())

    events = [event async for event in answerer.stream("How many vacation days?")]

    assert isinstance(events[0], RetrievalReady)
    assert events[0].result.chunks
    assert isinstance(events[-1], AnswerComplete)


async def test_streamed_deltas_reassemble_into_the_final_text(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    reply = "Employees accrue twenty five vacation days. [1]"
    answerer = _answerer(indexed, embeddings, StubChatModel(reply=reply))

    events = [event async for event in answerer.stream("How many vacation days?")]

    streamed = "".join(event.text for event in events if isinstance(event, TextDelta))
    complete = next(event for event in events if isinstance(event, AnswerComplete))
    assert streamed.strip() == complete.answer.text.strip()


async def test_stream_emits_citations(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    answerer = _answerer(indexed, embeddings, StubChatModel(reply="Answer. [1]"))

    events = [event async for event in answerer.stream("How many vacation days?")]

    assert any(isinstance(event, CitationDelta) for event in events)


async def test_streamed_abstention_is_signalled_on_the_final_event(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    """The complete event is authoritative: clients discard streamed text when it
    reports an abstention. This keeps the policy identical in both modes."""
    model = StubChatModel(reply="Unsupported claim with no markers.")
    answerer = _answerer(indexed, embeddings, model, require_citations=True)

    events = [event async for event in answerer.stream("How many vacation days?")]

    complete = next(event for event in events if isinstance(event, AnswerComplete))
    assert complete.answer.abstained
    assert "Unsupported claim" not in complete.answer.text


async def test_stream_abstains_without_a_model_call_when_nothing_is_retrieved(
    embeddings: StubEmbeddingModel,
) -> None:
    model = StubChatModel()
    answerer = _answerer(MemoryVectorStore(dimensions=EMBEDDING_DIMENSIONS), embeddings, model)

    events = [event async for event in answerer.stream("Unknown topic")]

    assert model.requests == []
    assert any(isinstance(event, AnswerComplete) and event.answer.abstained for event in events)


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize(
    "reply",
    [
        "[[NO_ANSWER]]",
        ' \n"[[NO_ANSWER]]". \n',
        "```\n[[NO_ANSWER]]\n```",
        "<think>The sources do not answer the question.</think>\n[[NO_ANSWER]]",
        "[[NO_ANSWER]] [1]",
        " \u2018[[NO_ANSWER]]\u2019!? [[1]] ",
    ],
)
async def test_model_sentinel_becomes_authoritative_abstention(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel, reply: str, streaming: bool
) -> None:
    answerer = _answerer(indexed, embeddings, StubChatModel(reply), require_citations=False)
    if streaming:
        events = [event async for event in answerer.stream("What is the missing policy?")]
        complete = events[-1]
        assert isinstance(complete, AnswerComplete)
        answer = complete.answer
        assert "[[NO_ANSWER]]" in "".join(
            event.text for event in events if isinstance(event, TextDelta)
        )
    else:
        answer = await answerer.answer("What is the missing policy?")

    assert answer.abstained
    assert answer.text == GenerationSettings().abstention_message
    assert answer.citations == []
    assert answer.retrieved
    assert answer.usage.input_tokens == 100
    recorded = RECORDER.get(answer.trace_id)
    assert recorded is not None
    assert any(s.attributes.get("abstention_reason") == "model_declined" for s in recorded.spans)


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize(
    "reply",
    [
        "Employees get twenty five days. [1] The carry-over policy is not specified.",
        "Employees get twenty five days. [1] [[NO_ANSWER]]",
        "[[NO_ANSWER]] The documented entitlement is twenty five days. [1]",
        "The literal marker in this example is `[[NO_ANSWER]]`. [1]",
        "Employees get twenty five days. The other part is [[NO_ANSWER]].",
        "The sources do not specify carry-over, but employees get twenty five days. [1]",
        "The sources do not specify carry-over and the entitlement is twenty five days. [1]",
        "The sources do not specify carry-over. Employees get twenty five days. [1]",
        "Discounts are not expanded in Liquid; expansion happens on save. [1]",
        "The module does not expose HTTP routes. [1]",
        'The documented example is "The sources do not specify retries." [1]',
        "The sources do not specify a limit, the documented capacity is twelve. [1]",
        "The sources do not specify a limit because the capacity varies by room. [1]",
        "The capacity is not listed in the sources. The room has a projector. [1]",
        "The sources do not expose the secret value; they expose its identifier. [1]",
    ],
)
async def test_partial_answers_and_literal_sentinel_mentions_are_preserved(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel, reply: str, streaming: bool
) -> None:
    answerer = _answerer(indexed, embeddings, StubChatModel(reply), require_citations=False)
    if streaming:
        events = [event async for event in answerer.stream("Entitlement and carry-over?")]
        complete = events[-1]
        assert isinstance(complete, AnswerComplete)
        answer = complete.answer
    else:
        answer = await answerer.answer("Entitlement and carry-over?")
    assert not answer.abstained
    assert answer.text.strip() == reply


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("reply", [
    "The sources do not specify the number of retries [[1]].",
    "The number of retries is not specified in the provided sources [[1]][[2]].",
    "<think>Look for the detail.</think>The sources do not provide a retention period. [1]",
    "The documentation does not specify the room capacity. [1]",
    "The requested detail is not explicitly provided in the sources. [1]",
    "The measurement for the 2.75 sample is not listed in the supplied sources. [1]",
    "There is no information about a second edition in the sources. [1]",
    "The sources contain no information about the room capacity. [1]",
    "The documentation does not expose the requested detail. [1]",
    "The sources do not state the capacity. The limit is not addressed in the sources. [1]",
])
async def test_whole_response_prose_refusal_is_recognised(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel, reply: str, streaming: bool
) -> None:
    answerer = _answerer(indexed, embeddings, StubChatModel(reply), require_citations=False)
    if streaming:
        events = [event async for event in answerer.stream("Missing policy?")]
        complete = events[-1]
        assert isinstance(complete, AnswerComplete)
        answer = complete.answer
    else:
        answer = await answerer.answer("Missing policy?")
    assert answer.abstained
    assert answer.text == GenerationSettings().abstention_message
    assert answer.citations == []


async def test_native_citation_on_a_sentinel_is_discarded(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    answer = await _answerer(
        indexed, embeddings, NativeCitationChatModel("[[NO_ANSWER]]")
    ).answer("An unknown detail?")
    assert answer.abstained
    assert answer.citations == []


async def test_a_sentinel_split_across_stream_deltas_is_recognised(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    class CharacterStream(StubChatModel):
        async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
            for character in self.reply:
                yield TextDelta(text=character)

    events = [
        event
        async for event in _answerer(
            indexed, embeddings, CharacterStream("[[NO_ANSWER]]"), require_citations=False
        ).stream("An unknown detail?")
    ]
    complete = events[-1]
    assert isinstance(complete, AnswerComplete)
    assert complete.answer.abstained


async def test_stream_failure_after_sentinel_does_not_fabricate_completion(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    class BrokenStream(StubChatModel):
        async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
            yield TextDelta(text="[[NO_ANSWER]]")
            raise RuntimeError("provider interrupted")

    events = []
    with pytest.raises(RuntimeError, match="provider interrupted"):
        async for event in _answerer(indexed, embeddings, BrokenStream()).stream("Unknown?"):
            events.append(event)
    assert not any(isinstance(event, AnswerComplete) for event in events)
