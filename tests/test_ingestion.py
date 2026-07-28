"""Ingestion tests.

Idempotency is the property that matters: a re-run over an unchanged corpus must
do no work and spend nothing on embeddings, otherwise scheduled syncs become
expensive and iterating on chunking becomes painful.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
from osc_assistant.ingestion import FilesystemLoader, IngestionPipeline, InMemoryLoader
from osc_assistant.providers.vectorstores.memory import MemoryVectorStore
from osc_assistant.types import Document

from .conftest import StubEmbeddingModel


@pytest.fixture
def pipeline(store: MemoryVectorStore, embeddings: StubEmbeddingModel) -> IngestionPipeline:
    return IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions(chunk_size=200, chunk_overlap=20)),
        embeddings=embeddings,
        store=store,
    )


async def test_documents_are_indexed(
    pipeline: IngestionPipeline, store: MemoryVectorStore, documents: list[Document]
) -> None:
    report = await pipeline.ingest(InMemoryLoader(documents).load())

    assert report.indexed == 3
    assert report.chunks > 0
    assert await store.document_ids() == {"doc-vacation", "doc-expenses", "doc-onboarding"}


async def test_reingesting_unchanged_documents_does_no_work(
    pipeline: IngestionPipeline, embeddings: StubEmbeddingModel, documents: list[Document]
) -> None:
    await pipeline.ingest(InMemoryLoader(documents).load())
    calls_after_first = embeddings.embed_calls

    report = await pipeline.ingest(InMemoryLoader(documents).load())

    assert report.skipped == 3
    assert report.indexed == 0
    assert embeddings.embed_calls == calls_after_first, "no embedding calls should be made"


async def test_edited_document_is_reindexed(
    pipeline: IngestionPipeline, store: MemoryVectorStore, documents: list[Document]
) -> None:
    await pipeline.ingest(InMemoryLoader(documents).load())

    edited = [
        Document(
            id=documents[0].id,
            source_uri=documents[0].source_uri,
            title=documents[0].title,
            text="# Vacation Policy\n\nEmployees now accrue thirty vacation days.",
        ),
        *documents[1:],
    ]
    report = await pipeline.ingest(InMemoryLoader(edited).load())

    assert report.indexed == 1
    assert report.skipped == 2

    hits = await store.search_keyword("thirty vacation days", limit=10)
    assert any("thirty vacation days" in hit.chunk.text for hit in hits), (
        "the edited text must be retrievable"
    )

    # The superseded chunks must be gone, not merely outranked: stale text that is
    # still retrievable can be cited as if current.
    stale = await store.search_keyword("accrue twenty five vacation days", limit=10)
    assert not [hit for hit in stale if "twenty five" in hit.chunk.text], (
        "the superseded text must not remain retrievable"
    )


async def test_removed_documents_are_pruned(
    pipeline: IngestionPipeline, store: MemoryVectorStore, documents: list[Document]
) -> None:
    await pipeline.ingest(InMemoryLoader(documents).load())

    report = await pipeline.ingest(InMemoryLoader(documents[:2]).load(), prune=True)

    assert report.deleted == 1
    assert "doc-onboarding" not in await store.document_ids()


async def test_prune_disabled_leaves_other_documents_alone(
    pipeline: IngestionPipeline, store: MemoryVectorStore, documents: list[Document]
) -> None:
    """Partial ingestion must not delete the rest of the corpus."""
    await pipeline.ingest(InMemoryLoader(documents).load())

    report = await pipeline.ingest(InMemoryLoader(documents[:1]).load(), prune=False)

    assert report.deleted == 0
    assert len(await store.document_ids()) == 3


async def test_one_bad_document_does_not_abort_the_sync(
    store: MemoryVectorStore, documents: list[Document]
) -> None:
    class FailsOnVacation(StubEmbeddingModel):
        async def embed_documents(self, texts: list[str]) -> list[list[float]]:  # type: ignore[override]
            if any("Vacation" in text for text in texts):
                raise RuntimeError("embedding provider rejected this batch")
            return await super().embed_documents(texts)

    pipeline = IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions()),
        embeddings=FailsOnVacation(),
        store=store,
    )

    report = await pipeline.ingest(InMemoryLoader(documents).load())

    assert report.indexed == 2
    assert len(report.failures) == 1
    assert not report.succeeded


async def test_filesystem_loader_reads_a_tree(tmp_path: Path) -> None:
    (tmp_path / "nested").mkdir()
    (tmp_path / "policy.md").write_text("# Vacation Policy\n\nTwenty five days.")
    (tmp_path / "nested" / "guide.txt").write_text("Onboarding guide contents.")
    (tmp_path / "ignored.png").write_bytes(b"\x89PNG")

    loaded = [document async for document in FilesystemLoader(tmp_path).load()]

    assert len(loaded) == 2
    titles = {document.title for document in loaded}
    assert "Vacation Policy" in titles, "a Markdown heading should become the title"
    assert "Guide" in titles, "a file without a heading falls back to its filename"


async def test_filesystem_loader_ids_are_stable(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("Content.")

    first = [document.id async for document in FilesystemLoader(tmp_path).load()]
    second = [document.id async for document in FilesystemLoader(tmp_path).load()]

    assert first == second


async def test_missing_corpus_directory_is_an_error(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        [document async for document in FilesystemLoader(tmp_path / "nope").load()]
