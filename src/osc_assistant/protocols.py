"""The five seams of the system.

Every swappable component is defined here as a `Protocol`. Implementations do not
import or subclass anything from this module — structural typing means a provider
adapter is compatible by virtue of its shape alone, which keeps adapters free of
inheritance and makes them trivially replaceable with test doubles.

Business logic (ingestion, retrieval, generation) depends only on these protocols
and on `types`. It never imports a provider module.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Sequence
from typing import Protocol, runtime_checkable

from .types import (
    ChatRequest,
    ChatResponse,
    Chunk,
    Document,
    EmbeddedChunk,
    ScoredChunk,
    StreamEvent,
    Vector,
)


@runtime_checkable
class ChatModel(Protocol):
    """A text-generating model."""

    @property
    def model_id(self) -> str:
        """The provider's identifier for the underlying model, for logs and traces."""

    @property
    def supports_citations(self) -> bool:
        """True if the provider resolves citations itself from structured sources.

        When False the generation layer falls back to instructing the model to emit
        `[n]` markers and parsing them out. Callers never branch on this — the
        adapter handles both paths and returns the same `ChatResponse` shape.
        """

    async def complete(self, request: ChatRequest) -> ChatResponse:
        """Generate a complete response."""

    def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        """Generate a response incrementally."""


@runtime_checkable
class EmbeddingModel(Protocol):
    """A text embedding model.

    Document and query embedding are separate methods because several models are
    asymmetric — they expect a different prefix or task type for each.
    """

    @property
    def model_id(self) -> str: ...

    @property
    def dimensions(self) -> int:
        """Vector width. Must match the vector store's configured dimension."""

    async def embed_documents(self, texts: Sequence[str]) -> list[Vector]:
        """Embed corpus text. Returns one vector per input, in order."""

    async def embed_query(self, text: str) -> Vector:
        """Embed a search query."""


@runtime_checkable
class VectorStore(Protocol):
    """Persistence and retrieval of embedded chunks.

    Implementations that cannot do lexical search should return an empty list from
    `search_keyword`; `search_hybrid` then degrades to pure vector search rather
    than failing, so business logic does not need to know the store's capabilities.
    """

    async def setup(self) -> None:
        """Prepare the store (connect, create collections). Idempotent."""

    async def close(self) -> None: ...

    @property
    def dimensions(self) -> int:
        """The vector width this store is configured to hold."""

    async def replace_document(
        self, document: Document, chunks: Sequence[EmbeddedChunk]
    ) -> None:
        """Atomically replace a document and all of its chunks.

        Must be all-or-nothing. `list_document_hashes` reports a document's hash,
        and the ingestion pipeline reads that as "this document's chunks are
        present" — so a partial write that records the hash without the chunks
        would make the document permanently invisible to retrieval, silently.
        Implementations that cannot offer a transaction must write the document
        record last.
        """

    async def delete_document(self, document_id: str) -> None:
        """Remove a document and every chunk belonging to it."""

    async def list_document_hashes(self) -> dict[str, str]:
        """Map document id to stored content hash, for incremental sync."""

    async def document_ids(self) -> set[str]:
        """Every document id currently indexed."""

    async def search_vector(self, vector: Vector, limit: int) -> list[ScoredChunk]: ...

    async def search_keyword(self, query: str, limit: int) -> list[ScoredChunk]:
        """Lexical search. Return `[]` if the store has no lexical index."""

    async def search_hybrid(self, vector: Vector, query: str, limit: int) -> list[ScoredChunk]:
        """Combined lexical and vector search, fused into a single ranking."""


@runtime_checkable
class Reranker(Protocol):
    """A second-stage relevance model applied to retrieval candidates."""

    @property
    def model_id(self) -> str: ...

    async def rerank(
        self, query: str, candidates: Sequence[ScoredChunk], top_k: int
    ) -> list[ScoredChunk]:
        """Return the `top_k` most relevant candidates, most relevant first."""


@runtime_checkable
class Chunker(Protocol):
    """Splits a document into retrievable units."""

    def split(self, document: Document) -> list[Chunk]:
        """Split `document`. Chunk ids must be stable across runs for the same input."""
