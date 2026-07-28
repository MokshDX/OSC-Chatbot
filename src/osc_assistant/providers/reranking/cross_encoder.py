"""Local cross-encoder reranker.

A cross-encoder scores the query and candidate together rather than comparing two
independently-produced vectors, which is why it consistently outperforms the
first-stage ranking. It is also quadratically more expensive, so it only ever runs
on the shortlist retrieval already produced.

Runs in-process with no network call, which keeps the added latency predictable
and keeps corpus text on our own infrastructure.
"""

from __future__ import annotations

import asyncio
from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ...errors import MissingDependencyError
from ...protocols import Reranker
from ...registries import reranker_registry
from ...registry import ComponentConfig
from ...types import MatchSource, ScoredChunk

DEFAULT_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CrossEncoderOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    device: str | None = None
    batch_size: int = Field(default=32, ge=1)
    max_length: int = Field(default=512, ge=64)


class CrossEncoderReranker:
    """Adapter over a `sentence-transformers` CrossEncoder."""

    def __init__(self, model: str, options: CrossEncoderOptions) -> None:
        try:
            from sentence_transformers import CrossEncoder
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise MissingDependencyError(
                "cross_encoder", "sentence-transformers", "local"
            ) from exc

        self._model_id = model or DEFAULT_MODEL
        self._options = options
        self._encoder = CrossEncoder(
            self._model_id, device=options.device, max_length=options.max_length
        )

    @property
    def model_id(self) -> str:
        return self._model_id

    async def rerank(
        self, query: str, candidates: Sequence[ScoredChunk], top_k: int
    ) -> list[ScoredChunk]:
        if not candidates:
            return []

        pairs = [(query, candidate.chunk.text) for candidate in candidates]
        scores = await asyncio.to_thread(self._score, pairs)

        rescored = [
            ScoredChunk(chunk=candidate.chunk, score=float(score), source=MatchSource.RERANK)
            for candidate, score in zip(candidates, scores, strict=True)
        ]
        rescored.sort(key=lambda item: item.score, reverse=True)
        return rescored[:top_k]

    def _score(self, pairs: list[tuple[str, str]]) -> list[float]:
        result: Any = self._encoder.predict(
            pairs, batch_size=self._options.batch_size, show_progress_bar=False
        )
        return [float(value) for value in result]


@reranker_registry.register("cross_encoder")
def _build(config: ComponentConfig) -> Reranker:
    return CrossEncoderReranker(config.model, CrossEncoderOptions.model_validate(config.options))
