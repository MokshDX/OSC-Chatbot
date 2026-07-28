"""In-process vector store.

Not a toy: this is what makes the test suite run without a database and what makes
a chunking or embedding sweep over a few thousand chunks a single process with no
infrastructure. It is the reference implementation of the `VectorStore` protocol —
if a change to the protocol is awkward to implement here, the protocol is wrong.

Not for production: everything lives in memory, search is a linear scan, and
nothing survives a restart.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from collections.abc import Sequence

from ...errors import DimensionMismatchError
from ...fusion import reciprocal_rank_fusion
from ...protocols import VectorStore
from ...registries import vector_store_registry
from ...registry import ComponentConfig
from ...types import (
    Document,
    EmbeddedChunk,
    MatchSource,
    ScoredChunk,
    Vector,
)

_TOKEN_PATTERN = re.compile(r"\w+")


class MemoryVectorStore:
    """A dictionary-backed `VectorStore`."""

    def __init__(self, dimensions: int, rrf_k: int = 60) -> None:
        self._dimensions = dimensions
        self._rrf_k = rrf_k
        self._chunks: dict[str, EmbeddedChunk] = {}
        self._hashes: dict[str, str] = {}

    async def setup(self) -> None:
        return None

    async def close(self) -> None:
        return None

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def replace_document(
        self, document: Document, chunks: Sequence[EmbeddedChunk]
    ) -> None:
        """Replace a document and its chunks.

        Atomic by construction: the vectors are validated before anything mutates,
        so a bad batch leaves the previous state untouched.
        """
        for embedded in chunks:
            if len(embedded.vector) != self._dimensions:
                raise DimensionMismatchError(
                    self._dimensions, len(embedded.vector), embedded.embedding_model
                )

        await self.delete_document(document.id)
        for embedded in chunks:
            self._chunks[embedded.chunk.id] = embedded
        self._hashes[document.id] = document.hash

    async def delete_document(self, document_id: str) -> None:
        stale = [
            chunk_id
            for chunk_id, embedded in self._chunks.items()
            if embedded.chunk.document_id == document_id
        ]
        for chunk_id in stale:
            del self._chunks[chunk_id]
        self._hashes.pop(document_id, None)

    async def list_document_hashes(self) -> dict[str, str]:
        return dict(self._hashes)

    async def document_ids(self) -> set[str]:
        return set(self._hashes)

    async def search_vector(self, vector: Vector, limit: int) -> list[ScoredChunk]:
        scored = [
            ScoredChunk(
                chunk=embedded.chunk,
                score=_cosine_similarity(vector, embedded.vector),
                source=MatchSource.VECTOR,
            )
            for embedded in self._chunks.values()
        ]
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:limit]

    async def search_keyword(self, query: str, limit: int) -> list[ScoredChunk]:
        """Term-overlap scoring.

        Deliberately not BM25: this exists to make hybrid retrieval exercisable
        without Postgres, not to be a search engine. Ranking quality here should
        never be used to judge the retrieval strategy — measure that against the
        pgvector store.
        """
        terms = Counter(_tokenize(query))
        if not terms:
            return []

        scored: list[ScoredChunk] = []
        for embedded in self._chunks.values():
            tokens = Counter(_tokenize(embedded.chunk.text))
            overlap = sum(min(count, tokens[term]) for term, count in terms.items())
            if overlap:
                scored.append(
                    ScoredChunk(
                        chunk=embedded.chunk,
                        score=overlap / sum(terms.values()),
                        source=MatchSource.KEYWORD,
                    )
                )
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:limit]

    async def search_hybrid(
        self, vector: Vector, query: str, limit: int
    ) -> list[ScoredChunk]:
        vector_hits = await self.search_vector(vector, limit)
        keyword_hits = await self.search_keyword(query, limit)
        return reciprocal_rank_fusion([vector_hits, keyword_hits], k=self._rrf_k, limit=limit)


def _cosine_similarity(left: Vector, right: Vector) -> float:
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def _tokenize(text: str) -> list[str]:
    return _TOKEN_PATTERN.findall(text.lower())


@vector_store_registry.register("memory")
def _build(config: ComponentConfig) -> VectorStore:
    dimensions = int(config.options.get("dimensions", 0))
    rrf_k = int(config.options.get("rrf_k", 60))
    return MemoryVectorStore(dimensions=dimensions, rrf_k=rrf_k)
