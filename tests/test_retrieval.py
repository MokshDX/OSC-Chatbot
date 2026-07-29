"""Retrieval tests, including the vector store contract.

`test_store_contract` runs against the in-memory store. Any new store
implementation should be added to its parametrisation so every backend is held to
the same behaviour.
"""

from __future__ import annotations

from collections.abc import Sequence

import pytest

from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
from osc_assistant.errors import DimensionMismatchError
from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader
from osc_assistant.providers.reranking.noop import NoopReranker
from osc_assistant.providers.vectorstores.memory import MemoryVectorStore
from osc_assistant.retrieval import QueryRewriter, RetrievalPipeline
from osc_assistant.settings import RetrievalSettings
from osc_assistant.types import (
    Chunk,
    Document,
    EmbeddedChunk,
    MatchSource,
    Message,
    Role,
    ScoredChunk,
)

from .conftest import EMBEDDING_DIMENSIONS, FailingChatModel, StubChatModel, StubEmbeddingModel


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


def _pipeline(
    store: MemoryVectorStore,
    embeddings: StubEmbeddingModel,
    **overrides: object,
) -> RetrievalPipeline:
    settings = RetrievalSettings(rewrite_queries=False, **overrides)  # type: ignore[arg-type]
    return RetrievalPipeline(
        store=store,
        embeddings=embeddings,
        reranker=NoopReranker(),
        settings=settings,
    )


# --------------------------------------------------------------- store contract


async def test_store_rejects_wrong_width_vectors(store: MemoryVectorStore) -> None:
    """Mixing vector widths silently produces nonsense scores; it must raise."""
    document = Document(id="d1", source_uri="file:///d.md", title="T", text="t")
    chunk = Chunk(
        id="c1", document_id="d1", ordinal=0, text="t", title="T", source_uri="file:///d.md"
    )

    with pytest.raises(DimensionMismatchError):
        await store.replace_document(
            document, [EmbeddedChunk(chunk=chunk, vector=[0.1, 0.2], embedding_model="stub")]
        )

    assert await store.document_ids() == set(), "a rejected write must not be partially applied"


async def test_deleting_a_document_removes_its_chunks(indexed: MemoryVectorStore) -> None:
    await indexed.delete_document("doc-vacation")

    hits = await indexed.search_keyword("vacation days accrue", limit=10)
    assert all(hit.chunk.document_id != "doc-vacation" for hit in hits)
    assert "doc-vacation" not in await indexed.document_ids()


async def test_hashes_are_recorded_for_incremental_sync(indexed: MemoryVectorStore) -> None:
    hashes = await indexed.list_document_hashes()

    assert set(hashes) == {"doc-vacation", "doc-expenses", "doc-onboarding"}
    assert all(len(value) == 64 for value in hashes.values())


# ------------------------------------------------------------------- strategies


@pytest.mark.parametrize("strategy", ["vector", "keyword", "hybrid"])
async def test_every_strategy_finds_the_right_document(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel, strategy: str
) -> None:
    pipeline = _pipeline(indexed, embeddings, strategy=strategy)

    result = await pipeline.retrieve("How many vacation days do employees accrue?")

    assert result.chunks
    assert result.chunks[0].chunk.document_id == "doc-vacation"


async def test_hybrid_results_are_marked_as_fused(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    pipeline = _pipeline(indexed, embeddings, strategy="hybrid")

    result = await pipeline.retrieve("expense receipts")

    assert all(hit.source is MatchSource.HYBRID for hit in result.chunks)


async def test_top_k_bounds_the_result_set(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    pipeline = _pipeline(indexed, embeddings, top_k=2)

    result = await pipeline.retrieve("policy")

    assert len(result.chunks) <= 2


async def test_min_score_filters_weak_hits(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    permissive = await _pipeline(indexed, embeddings, strategy="vector").retrieve("laptop")
    strict = await _pipeline(
        indexed, embeddings, strategy="vector", min_score=0.99
    ).retrieve("laptop")

    assert len(strict.chunks) < len(permissive.chunks)


async def test_min_score_is_applied_before_reranking(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    """Regression: the threshold must not be measured against reranker output.

    A cross-encoder returns an unbounded logit that is routinely negative for a
    genuinely relevant passage. When the threshold was applied after reranking,
    the default `min_score: 0.0` silently discarded every result the moment a
    reranker was enabled — and the symptom looked like a bad reranker rather than
    a misapplied threshold.
    """

    class NegativeScoringReranker:
        """Stands in for a cross-encoder: relevance-ordered, negative scores."""

        model_id = "negative-stub"

        async def rerank(
            self, query: str, candidates: Sequence[ScoredChunk], top_k: int
        ) -> list[ScoredChunk]:
            return [
                ScoredChunk(chunk=hit.chunk, score=-1.5 - index, source=MatchSource.RERANK)
                for index, hit in enumerate(candidates[:top_k])
            ]

    pipeline = RetrievalPipeline(
        store=indexed,
        embeddings=embeddings,
        reranker=NegativeScoringReranker(),
        settings=RetrievalSettings(rewrite_queries=False, strategy="vector", min_score=0.0),
    )

    result = await pipeline.retrieve("How many vacation days do employees accrue?")

    assert result.chunks, "negative reranker scores must not be filtered out"
    assert all(hit.score < 0 for hit in result.chunks)


async def test_empty_corpus_returns_no_hits(embeddings: StubEmbeddingModel) -> None:
    """This is what triggers abstention rather than a guessed answer."""
    empty = MemoryVectorStore(dimensions=EMBEDDING_DIMENSIONS)

    result = await _pipeline(empty, embeddings).retrieve("anything at all")

    assert result.chunks == []


async def test_reranker_reorders_the_shortlist(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    class ReverseReranker:
        @property
        def model_id(self) -> str:
            return "reverse"

        async def rerank(self, query: str, candidates: list, top_k: int) -> list:  # type: ignore[type-arg]
            return list(reversed(candidates))[:top_k]

    baseline = await _pipeline(indexed, embeddings, top_k=3).retrieve("policy")
    reranked = await RetrievalPipeline(
        store=indexed,
        embeddings=embeddings,
        reranker=ReverseReranker(),
        settings=RetrievalSettings(rewrite_queries=False, top_k=3),
    ).retrieve("policy")

    assert [hit.chunk.id for hit in reranked.chunks] != [hit.chunk.id for hit in baseline.chunks]


# --------------------------------------------------------------- query rewriting


async def test_rewriting_resolves_a_follow_up_question(
    indexed: MemoryVectorStore, embeddings: StubEmbeddingModel
) -> None:
    rewriter = QueryRewriter(StubChatModel(reply="When do unused vacation days expire?"))
    pipeline = RetrievalPipeline(
        store=indexed,
        embeddings=embeddings,
        reranker=NoopReranker(),
        settings=RetrievalSettings(rewrite_queries=True),
        rewriter=rewriter,
    )

    result = await pipeline.retrieve(
        "When do they expire?",
        [Message(role=Role.USER, content="Tell me about the vacation policy.")],
    )

    assert result.original_query == "When do they expire?"
    assert result.query == "When do unused vacation days expire?"
    assert result.chunks[0].chunk.document_id == "doc-vacation"


async def test_first_turn_is_not_rewritten() -> None:
    """With no history there is nothing to resolve, so no call should be made."""
    model = StubChatModel()
    rewriter = QueryRewriter(model)

    assert await rewriter.rewrite("What is the expense limit?", []) == "What is the expense limit?"
    assert model.requests == []


async def test_rewrite_failure_falls_back_to_the_original_question() -> None:
    """A degraded query beats a failed request."""
    rewriter = QueryRewriter(FailingChatModel())

    result = await rewriter.rewrite(
        "And that one?", [Message(role=Role.USER, content="Earlier question")]
    )

    assert result == "And that one?"
