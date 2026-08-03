"""The retrieval pipeline: question in, ranked chunks out.

    rewrite -> search (vector | keyword | hybrid) -> rerank -> threshold -> top_k

Every stage is configuration-driven, and the pipeline holds no provider knowledge:
it is composed from a `VectorStore`, an `EmbeddingModel` and a `Reranker`, so
swapping any of them is a settings change. That is what makes a retrieval sweep
cheap to run.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from ..logging import get_logger
from ..observability import annotate, annotate_text, current_trace_id, span, trace
from ..protocols import EmbeddingModel, Reranker, VectorStore
from ..settings import RetrievalSettings
from ..types import Message, ScoredChunk, SourceDocument
from .rewrite import QueryRewriter

log = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    """Ranked chunks plus everything needed to explain how they were selected.

    `trace_id` is the handle to the full stage-by-stage record in the trace
    recorder: the result says *what* was retrieved, the trace says *how*.
    """

    query: str
    original_query: str
    chunks: list[ScoredChunk] = field(default_factory=list)
    candidates_considered: int = 0
    duration_seconds: float = 0.0
    trace_id: str = ""

    def as_sources(self) -> list[SourceDocument]:
        """Render the results as grounding material for the model."""
        return [
            SourceDocument(
                chunk_id=scored.chunk.id,
                document_id=scored.chunk.document_id,
                title=scored.chunk.title,
                source_uri=scored.chunk.source_uri,
                text=scored.chunk.text,
            )
            for scored in self.chunks
        ]


class RetrievalPipeline:
    """Composes rewriting, search and reranking into one call."""

    def __init__(
        self,
        store: VectorStore,
        embeddings: EmbeddingModel,
        reranker: Reranker,
        settings: RetrievalSettings,
        rewriter: QueryRewriter | None = None,
    ) -> None:
        self._store = store
        self._embeddings = embeddings
        self._reranker = reranker
        self._settings = settings
        self._rewriter = rewriter

    async def retrieve(
        self, question: str, history: list[Message] | None = None
    ) -> RetrievalResult:
        """Retrieve the chunks most relevant to `question`."""
        started = time.perf_counter()

        # `trace` rather than `span`: called on its own — by `osc-assistant search`,
        # by `/api/search`, or by the LangChain retriever — retrieval is the whole
        # operation and needs a trace of its own. Called from the answerer it
        # extends that trace instead of starting a second one.
        with trace(
            "retrieve",
            strategy=self._settings.strategy,
            candidates_requested=self._settings.candidates,
            top_k=self._settings.top_k,
            min_score=self._settings.min_score,
            reranker=self._reranker.model_id,
        ):
            annotate_text("question", question)
            query = await self._resolve_query(question, history or [])

            candidates = await self._search(query)
            # The threshold is applied to first-stage scores, before reranking,
            # because only those are on a known scale (cosine similarity, or an RRF
            # score). A cross-encoder returns an unbounded logit that is routinely
            # negative for a genuinely relevant passage, so thresholding its output
            # at the same configured value would discard the entire result set the
            # moment a reranker was enabled — presenting as "the reranker is bad"
            # rather than as a misapplied threshold.
            with span("threshold", min_score=self._settings.min_score) as filtering:
                kept = [hit for hit in candidates if hit.score >= self._settings.min_score]
                filtering.set(kept=len(kept), discarded=len(candidates) - len(kept))

            with span("rerank", reranker=self._reranker.model_id, input=len(kept)) as ranking:
                selected = await self._reranker.rerank(query, kept, self._settings.top_k)
                ranking.set(
                    selected=len(selected),
                    top_score=round(selected[0].score, 6) if selected else None,
                )

            # Attached to the retrieval span rather than logged separately: this is
            # the answer to "why did the model see these five passages?", and it
            # belongs with the timings that produced them.
            annotate(
                candidates=len(candidates),
                above_threshold=len(kept),
                selected=len(selected),
                chunk_ids=[hit.chunk.id for hit in selected],
                scores=[round(hit.score, 6) for hit in selected],
                documents=sorted({hit.chunk.document_id for hit in selected}),
            )

            result = RetrievalResult(
                query=query,
                original_query=question,
                chunks=selected,
                candidates_considered=len(candidates),
                duration_seconds=time.perf_counter() - started,
                trace_id=current_trace_id(),
            )

        log.info(
            "retrieval.complete",
            extra={
                "query": query,
                "strategy": self._settings.strategy,
                "candidates": len(candidates),
                "above_threshold": len(kept),
                "selected": len(selected),
                "chunk_ids": [hit.chunk.id for hit in selected],
                "duration_seconds": round(result.duration_seconds, 3),
                "trace_id": result.trace_id,
            },
        )
        return result

    async def _resolve_query(self, question: str, history: list[Message]) -> str:
        if not self._settings.rewrite_queries or self._rewriter is None:
            return question
        with span("rewrite", model=self._rewriter.model_id, history=len(history)) as stage:
            rewritten = await self._rewriter.rewrite(question, history)
            stage.set(changed=rewritten != question)
            stage.set_text("rewritten", rewritten)
            return rewritten

    async def _search(self, query: str) -> list[ScoredChunk]:
        limit = self._settings.candidates
        strategy = self._settings.strategy

        if strategy == "keyword":
            return await self._search_store(strategy, limit, query=query)

        with span("embed_query", model=self._embeddings.model_id) as stage:
            vector = await self._embeddings.embed_query(query)
            stage.set(dimensions=len(vector))

        if strategy == "vector":
            return await self._search_store(strategy, limit, vector=vector)
        return await self._search_store(strategy, limit, query=query, vector=vector)

    async def _search_store(
        self,
        strategy: str,
        limit: int,
        *,
        query: str | None = None,
        vector: list[float] | None = None,
    ) -> list[ScoredChunk]:
        """Dispatch to the store, timing it and recording the shape of the result.

        The store call is the single most common source of latency and of
        "retrieval returned nothing" reports, so it gets its own span with the score
        range attached: an empty result and a result of uniformly poor scores are
        different problems with different fixes.
        """
        with span("search", strategy=strategy, limit=limit) as stage:
            if strategy == "keyword":
                assert query is not None
                hits = await self._store.search_keyword(query, limit)
            elif strategy == "vector":
                assert vector is not None
                hits = await self._store.search_vector(vector, limit)
            else:
                assert query is not None and vector is not None
                hits = await self._store.search_hybrid(vector, query, limit)

            stage.set(
                hits=len(hits),
                top_score=round(hits[0].score, 6) if hits else None,
                bottom_score=round(hits[-1].score, 6) if hits else None,
            )
            return hits
