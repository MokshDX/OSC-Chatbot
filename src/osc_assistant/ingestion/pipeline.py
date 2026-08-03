"""The ingestion pipeline: documents in, embedded chunks in the store.

Idempotent by content hash. Re-running over an unchanged corpus does no work and
costs nothing in embedding calls, which is what makes it safe to run on a schedule
and safe to re-run by hand while iterating on chunking.

Depends only on protocols, so the same pipeline ingests into Postgres in
production and into the in-memory store in tests, with any embedding provider.
"""

from __future__ import annotations

import time
from collections.abc import AsyncIterator, Sequence
from dataclasses import dataclass, field

from ..logging import get_logger
from ..observability import annotate, span, trace
from ..protocols import Chunker, EmbeddingModel, VectorStore
from ..types import Document, EmbeddedChunk, LoadFailure

log = get_logger(__name__)


@dataclass(slots=True)
class IngestionReport:
    """What a sync did. Returned to the CLI and logged for the admin view."""

    processed: int = 0
    indexed: int = 0
    skipped: int = 0
    deleted: int = 0
    chunks: int = 0
    unreadable: int = 0
    failures: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    trace_id: str = ""

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
        self,
        documents: AsyncIterator[Document],
        *,
        prune: bool = True,
        reindex: bool = False,
        source_failures: Sequence[LoadFailure] | None = None,
    ) -> IngestionReport:
        """Sync `documents` into the store.

        Args:
            documents: The full current contents of the source.
            prune: Delete indexed documents absent from `documents`. Correct for a
                full sync; must be False when ingesting a subset, or the rest of the
                corpus is deleted.
            reindex: Re-chunk, re-embed and re-store every document even when its
                content hash is unchanged. Required after changing the chunker or
                the embedding model, neither of which the content hash covers.
            source_failures: Files the connector found but could not read. These are
                reported as failures and, critically, are exempt from pruning: an
                unreadable file is still present at the source, and deleting its
                indexed copy would turn a transient parse error into permanent data
                loss. Read only once `documents` is exhausted, so a connector may
                append to the sequence it passed while it is being iterated.

        Returns:
            A report of what changed.
        """
        started = time.perf_counter()
        report = IngestionReport()

        with trace(
            "ingest",
            chunker=type(self._chunker).__name__,
            embedding_model=self._embeddings.model_id,
            prune=prune,
            reindex=reindex,
        ) as sync:
            report.trace_id = sync.trace_id

            with span("load_hashes") as stage:
                known_hashes = await self._store.list_document_hashes()
                stage.set(indexed_documents=len(known_hashes))

            seen: set[str] = set()

            async for document in documents:
                report.processed += 1
                seen.add(document.id)

                # `reindex` forces work the content hash says is unnecessary. It
                # exists because the hash covers the document text and nothing
                # else: change the chunker or its settings and every stored chunk
                # is stale while every hash still matches, so an ordinary sync
                # would report `skipped` and quietly leave the old chunks in place.
                if not reindex and known_hashes.get(document.id) == document.hash:
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

            # Recorded after the stream is exhausted: a connector discovers
            # unreadable files as it walks the source, so the list is only complete
            # by now.
            unreadable = list(source_failures or [])
            report.unreadable = len(unreadable)
            report.failures.extend(
                f"{failure.source_uri}: {failure.error}" for failure in unreadable
            )

            if prune:
                with span("prune") as stage:
                    protected = seen | {failure.document_id for failure in unreadable}
                    report.deleted = await self._prune(protected, set(known_hashes))
                    stage.set(deleted=report.deleted, protected=len(protected))

            report.duration_seconds = time.perf_counter() - started
            # The innermost open span here is the trace root, so the totals land on
            # it and a reader sees the outcome of the whole sync on its first line.
            annotate(
                processed=report.processed,
                indexed=report.indexed,
                skipped=report.skipped,
                deleted=report.deleted,
                chunks=report.chunks,
                unreadable=report.unreadable,
                failures=len(report.failures),
            )

        log.info(
            "ingestion.complete",
            extra={
                "processed": report.processed,
                "indexed": report.indexed,
                "skipped": report.skipped,
                "deleted": report.deleted,
                "chunks": report.chunks,
                "unreadable": report.unreadable,
                "failures": len(report.failures),
                "duration_seconds": round(report.duration_seconds, 3),
                "trace_id": report.trace_id,
            },
        )
        return report

    async def _index(self, document: Document) -> int:
        """Chunk, embed and store one document.

        Each of the three stages gets its own span. That split is what turns "the
        sync is slow" into an answerable question: chunking is CPU in-process,
        embedding is a provider round trip per batch, and storing is a database
        transaction — three different problems with three different fixes, and
        indistinguishable from a single duration.
        """
        with span(
            "document", document_id=document.id, source_uri=document.source_uri
        ) as document_span:
            document_span.set(text_chars=len(document.text))

            with span("chunk", chunker=type(self._chunker).__name__) as stage:
                chunks = self._chunker.split(document)
                sizes = [len(chunk.text) for chunk in chunks]
                stage.set(
                    chunks=len(chunks),
                    mean_chars=round(sum(sizes) / len(sizes)) if sizes else 0,
                    max_chars=max(sizes, default=0),
                )

            if not chunks:
                document_span.set(indexed=False, reason="no_chunks")
                log.warning("ingestion.empty_document", extra={"document_id": document.id})
                return 0

            with span("embed", model=self._embeddings.model_id, texts=len(chunks)) as stage:
                vectors = await self._embeddings.embed_documents(
                    [chunk.text for chunk in chunks]
                )
                stage.set(
                    vectors=len(vectors),
                    dimensions=len(vectors[0]) if vectors else 0,
                )

            if len(vectors) != len(chunks):
                raise ValueError(
                    f"Embedding provider returned {len(vectors)} vectors for "
                    f"{len(chunks)} chunks."
                )

            embedded = [
                EmbeddedChunk(
                    chunk=chunk, vector=vector, embedding_model=self._embeddings.model_id
                )
                for chunk, vector in zip(chunks, vectors, strict=True)
            ]

            # One atomic call: the store records the document hash only once its
            # chunks are durable. Splitting this into separate writes let a crash in
            # between leave a current hash with no chunks, which the skip check then
            # read as "already indexed" — the document silently invisible forever.
            with span("store", chunks=len(embedded)):
                await self._store.replace_document(document, embedded)

            document_span.set(indexed=True, chunks=len(embedded))
            return len(embedded)

    async def _prune(self, keep: set[str], known: set[str]) -> int:
        """Delete indexed documents that the source no longer offers.

        `keep` is every document the source still has: those loaded successfully
        plus those that failed to load. Only what is genuinely gone is removed.
        """
        removed = known - keep
        for document_id in removed:
            await self._store.delete_document(document_id)
            log.info("ingestion.document_removed", extra={"document_id": document_id})
        return len(removed)
