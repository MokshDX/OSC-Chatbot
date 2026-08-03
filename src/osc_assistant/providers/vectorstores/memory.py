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
    Chunk,
    Document,
    DocumentSummary,
    EmbeddedChunk,
    IndexStatistics,
    MatchSource,
    ScoredChunk,
    Vector,
)

_TOKEN_PATTERN = re.compile(r"\w+")


class MemoryVectorStore:
    """A dictionary-backed `VectorStore`."""

    def __init__(self, dimensions: int, rrf_k: int = 60, workspace_id: str = "default") -> None:
        self._dimensions = dimensions
        self._rrf_k = rrf_k
        self._workspace_id = workspace_id
        self._chunks: dict[str, EmbeddedChunk] = {}
        self._hashes: dict[str, str] = {}
        # Retained so inspection can report titles, URIs and metadata without
        # reconstructing them from a chunk. Chunks denormalise those fields, but a
        # document with zero chunks has none to read them from — and a document
        # that indexed to zero chunks is exactly the one an operator is looking for.
        self._documents: dict[str, Document] = {}

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
        self._documents[document.id] = document

    async def delete_document(self, document_id: str) -> None:
        stale = [
            chunk_id
            for chunk_id, embedded in self._chunks.items()
            if embedded.chunk.document_id == document_id
        ]
        for chunk_id in stale:
            del self._chunks[chunk_id]
        self._hashes.pop(document_id, None)
        self._documents.pop(document_id, None)

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

    # ----------------------------------------------------- StoreInspector
    #
    # Implemented here as well as in pgvector so that the inspection commands are
    # testable without a database, on the same principle that makes this the
    # reference implementation of `VectorStore`.

    async def statistics(self) -> IndexStatistics:
        sizes = sorted(len(embedded.chunk.text) for embedded in self._chunks.values())
        extensions = Counter(
            str(document.metadata.get("extension", "unknown"))
            for document in self._documents.values()
        )
        return IndexStatistics(
            workspace_id=self._workspace_id,
            documents=len(self._hashes),
            chunks=len(self._chunks),
            embedding_models=sorted(
                {embedded.embedding_model for embedded in self._chunks.values()}
            ),
            dimensions=self._dimensions,
            chunk_chars_min=sizes[0] if sizes else 0,
            chunk_chars_mean=round(sum(sizes) / len(sizes), 1) if sizes else 0.0,
            chunk_chars_p50=_percentile(sizes, 0.50),
            chunk_chars_p95=_percentile(sizes, 0.95),
            chunk_chars_max=sizes[-1] if sizes else 0,
            documents_by_extension=dict(extensions),
            last_indexed_at=None,
        )

    async def list_documents(
        self, limit: int = 50, offset: int = 0, search: str | None = None
    ) -> list[DocumentSummary]:
        summaries = [self._summarise(document) for document in self._documents.values()]
        if search:
            needle = search.lower()
            summaries = [
                summary
                for summary in summaries
                if needle in summary.title.lower() or needle in summary.source_uri.lower()
            ]
        summaries.sort(key=lambda summary: summary.source_uri)
        return summaries[offset : offset + limit]

    async def get_document(self, document_id: str) -> DocumentSummary | None:
        document = self._documents.get(document_id)
        return self._summarise(document) if document else None

    async def document_chunks(self, document_id: str) -> list[Chunk]:
        chunks = [
            embedded.chunk
            for embedded in self._chunks.values()
            if embedded.chunk.document_id == document_id
        ]
        return sorted(chunks, key=lambda chunk: chunk.ordinal)

    async def get_chunk(self, chunk_id: str) -> Chunk | None:
        embedded = self._chunks.get(chunk_id)
        return embedded.chunk if embedded else None

    def _summarise(self, document: Document) -> DocumentSummary:
        return DocumentSummary(
            id=document.id,
            title=document.title,
            source_uri=document.source_uri,
            content_hash=self._hashes.get(document.id, ""),
            chunk_count=sum(
                1
                for embedded in self._chunks.values()
                if embedded.chunk.document_id == document.id
            ),
            metadata=document.metadata,
            updated_at=document.updated_at,
        )


def _percentile(sorted_sizes: list[int], fraction: float) -> int:
    """Nearest-rank percentile over a pre-sorted list. Empty input is 0."""
    if not sorted_sizes:
        return 0
    index = min(len(sorted_sizes) - 1, int(fraction * len(sorted_sizes)))
    return sorted_sizes[index]


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
    workspace_id = str(config.options.get("workspace_id", "default"))
    return MemoryVectorStore(dimensions=dimensions, rrf_k=rrf_k, workspace_id=workspace_id)
