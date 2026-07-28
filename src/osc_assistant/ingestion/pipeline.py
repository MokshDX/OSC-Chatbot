"""The ingestion pipeline: documents in, embedded chunks in the store.

Idempotent by content hash. Re-running over an unchanged corpus does no work and
costs nothing in embedding calls, which is what makes it safe to run on a schedule
and safe to re-run by hand while iterating on chunking.

Depends only on protocols, so the same pipeline ingests into Postgres in
production and into the in-memory store in tests, with any embedding provider.
"""

from __future__ import annotations

import time
from collections.abc import AsyncIterator
from dataclasses import dataclass, field

from ..logging import get_logger
from ..protocols import Chunker, EmbeddingModel, VectorStore
from ..types import Document, EmbeddedChunk

log = get_logger(__name__)


@dataclass(slots=True)
class IngestionReport:
    """What a sync did. Returned to the CLI and logged for the admin view."""

    processed: int = 0
    indexed: int = 0
    skipped: int = 0
    deleted: int = 0
    chunks: int = 0
    failures: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0

    @property
    def succeeded(self) -> bool:
        return not self.failures


class IngestionPipeline:
    """Chunks, embeds and stores documents."""

    def __init__(
        self,
        chunker: Chunker,
        embeddings: EmbeddingModel,
        store: VectorStore,
        embed_batch_size: int = 64,
    ) -> None:
        self._chunker = chunker
        self._embeddings = embeddings
        self._store = store
        self._embed_batch_size = embed_batch_size

    async def ingest(
        self, documents: AsyncIterator[Document], *, prune: bool = True
    ) -> IngestionReport:
        """Sync `documents` into the store.

        Args:
            documents: The full current contents of the source.
            prune: Delete indexed documents absent from `documents`. Correct for a
                full sync; must be False when ingesting a subset, or the rest of the
                corpus is deleted.

        Returns:
            A report of what changed.
        """
        started = time.perf_counter()
        report = IngestionReport()
        known_hashes = await self._store.list_document_hashes()
        seen: set[str] = set()

        async for document in documents:
            report.processed += 1
            seen.add(document.id)

            if known_hashes.get(document.id) == document.hash:
                report.skipped += 1
                continue

            try:
                chunk_count = await self._index(document)
            # Broad by intent: any single document failure is recorded and the
            # sync continues. One malformed file must not block the corpus.
            except Exception as exc:
                report.failures.append(f"{document.source_uri}: {exc}")
                log.exception(
                    "ingestion.document_failed",
                    extra={"document_id": document.id, "source_uri": document.source_uri},
                )
                continue

            report.indexed += 1
            report.chunks += chunk_count

        if prune:
            report.deleted = await self._prune(seen, set(known_hashes))

        report.duration_seconds = time.perf_counter() - started
        log.info(
            "ingestion.complete",
            extra={
                "processed": report.processed,
                "indexed": report.indexed,
                "skipped": report.skipped,
                "deleted": report.deleted,
                "chunks": report.chunks,
                "failures": len(report.failures),
                "duration_seconds": round(report.duration_seconds, 3),
            },
        )
        return report

    async def _index(self, document: Document) -> int:
        chunks = self._chunker.split(document)
        if not chunks:
            log.warning("ingestion.empty_document", extra={"document_id": document.id})
            return 0

        vectors = await self._embeddings.embed_documents([chunk.text for chunk in chunks])
        if len(vectors) != len(chunks):
            raise ValueError(
                f"Embedding provider returned {len(vectors)} vectors for "
                f"{len(chunks)} chunks."
            )

        embedded = [
            EmbeddedChunk(chunk=chunk, vector=vector, embedding_model=self._embeddings.model_id)
            for chunk, vector in zip(chunks, vectors, strict=True)
        ]

        # One atomic call: the store records the document hash only once its
        # chunks are durable. Splitting this into separate writes let a crash in
        # between leave a current hash with no chunks, which the skip check then
        # read as "already indexed" — the document silently invisible forever.
        await self._store.replace_document(document, embedded)
        return len(embedded)

    async def _prune(self, seen: set[str], known: set[str]) -> int:
        removed = known - seen
        for document_id in removed:
            await self._store.delete_document(document_id)
            log.info("ingestion.document_removed", extra={"document_id": document_id})
        return len(removed)
