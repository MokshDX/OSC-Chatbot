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
from ..protocols import EmbeddingModel, Reranker, VectorStore
from ..settings import RetrievalSettings
from ..types import Message, ScoredChunk, SourceDocument
from .rewrite import QueryRewriter

log = get_logger(__name__)


@dataclass(slots=True)
class RetrievalResult:
    """Ranked chunks plus everything needed to explain how they were selected."""

    query: str
    original_query: str
    chunks: list[ScoredChunk] = field(default_factory=list)
    candidates_considered: int = 0
    duration_seconds: float = 0.0

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
        query = await self._resolve_query(question, history or [])

        candidates = await self._search(query)
        # The threshold is applied to first-stage scores, before reranking, because
        # only those are on a known scale (cosine similarity, or an RRF score). A
        # cross-encoder returns an unbounded logit that is routinely negative for a
        # genuinely relevant passage, so thresholding its output at the same
        # configured value would discard the entire result set the moment a
        # reranker was enabled — presenting as "the reranker is bad" rather than as
        # a misapplied threshold.
        kept = [hit for hit in candidates if hit.score >= self._settings.min_score]
        selected = await self._reranker.rerank(query, kept, self._settings.top_k)

        result = RetrievalResult(
            query=query,
            original_query=question,
            chunks=selected,
            candidates_considered=len(candidates),
            duration_seconds=time.perf_counter() - started,
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
            },
        )
        return result

    async def _resolve_query(self, question: str, history: list[Message]) -> str:
        if not self._settings.rewrite_queries or self._rewriter is None:
            return question
        return await self._rewriter.rewrite(question, history)

    async def _search(self, query: str) -> list[ScoredChunk]:
        limit = self._settings.candidates
        strategy = self._settings.strategy

        if strategy == "keyword":
            return await self._store.search_keyword(query, limit)

        vector = await self._embeddings.embed_query(query)
        if strategy == "vector":
            return await self._store.search_vector(vector, limit)
        return await self._store.search_hybrid(vector, query, limit)
