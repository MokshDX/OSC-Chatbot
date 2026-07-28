"""Answer generation tests.

The abstention policy is the system's main defence against confident wrong
answers, so it is tested explicitly in both the buffered and streaming paths — a
policy that only held when not streaming would be worse than none.
"""

from __future__ import annotations

import pytest

from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
from osc_assistant.generation import AnswerComplete, Answerer, RetrievalReady
from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader
from osc_assistant.providers.reranking.noop import NoopReranker
from osc_assistant.providers.vectorstores.memory import MemoryVectorStore
from osc_assistant.retrieval import RetrievalPipeline
from osc_assistant.settings import GenerationSettings, RetrievalSettings
from osc_assistant.types import CitationDelta, Document, TextDelta

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
