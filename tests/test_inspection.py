"""Store inspection tests.

`StoreInspector` is what the operational commands are built on, so these assert the
contract they rely on rather than the SQL behind it. The memory store implements it
too, which is why they can run without a database — and why a change to the
interface that is awkward here is a change worth reconsidering.
"""

from __future__ import annotations

import pytest

from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader
from osc_assistant.protocols import StoreInspector
from osc_assistant.providers.vectorstores.memory import MemoryVectorStore
from osc_assistant.types import Document


@pytest.fixture
async def indexed(store: MemoryVectorStore, embeddings, documents) -> MemoryVectorStore:
    pipeline = IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions(chunk_size=120, chunk_overlap=20)),
        embeddings=embeddings,
        store=store,
    )
    await pipeline.ingest(InMemoryLoader(documents).load())
    return store


def test_both_built_in_stores_offer_inspection() -> None:
    """The protocol is optional; a store that cannot support it is still a store.

    Both of ours can, and tooling that degrades gracefully is only testable if at
    least one implementation exists to compare against.
    """
    from osc_assistant.providers.vectorstores.pgvector import PgVectorStore

    assert isinstance(MemoryVectorStore(dimensions=8), StoreInspector)
    assert issubclass(PgVectorStore, StoreInspector)


async def test_statistics_report_the_corpus(indexed: MemoryVectorStore) -> None:
    stats = await indexed.statistics()

    assert stats.documents == 3
    assert stats.chunks > 3
    assert stats.embedding_models == ["stub-embedding"]
    assert stats.dimensions == indexed.dimensions


async def test_chunk_size_percentiles_reflect_what_was_actually_stored(
    indexed: MemoryVectorStore,
) -> None:
    """The point of measuring is comparing against the configured target.

    A `chunk_size` of 120 with a p95 of 20 means the separators are firing far too
    early, and nothing else in the system would reveal that.
    """
    stats = await indexed.statistics()

    assert 0 < stats.chunk_chars_min <= stats.chunk_chars_p50 <= stats.chunk_chars_p95
    assert stats.chunk_chars_p95 <= stats.chunk_chars_max <= 120 + 20


async def test_statistics_on_an_empty_store_do_not_divide_by_zero() -> None:
    stats = await MemoryVectorStore(dimensions=8).statistics()

    assert stats.documents == 0 and stats.chunks == 0
    assert stats.chunk_chars_p50 == 0 and stats.chunk_chars_mean == 0.0


async def test_documents_can_be_listed_and_searched(indexed: MemoryVectorStore) -> None:
    listed = await indexed.list_documents()
    assert {summary.id for summary in listed} == {
        "doc-vacation",
        "doc-expenses",
        "doc-onboarding",
    }
    assert all(summary.chunk_count > 0 for summary in listed)

    matched = await indexed.list_documents(search="vacation")
    assert [summary.id for summary in matched] == ["doc-vacation"]


async def test_listing_is_paginated(indexed: MemoryVectorStore) -> None:
    first = await indexed.list_documents(limit=2)
    second = await indexed.list_documents(limit=2, offset=2)

    assert len(first) == 2 and len(second) == 1
    assert not {summary.id for summary in first} & {summary.id for summary in second}


async def test_a_document_reports_its_chunks_in_order(indexed: MemoryVectorStore) -> None:
    summary = await indexed.get_document("doc-vacation")
    assert summary is not None
    assert summary.title == "Vacation Policy"
    assert summary.content_hash

    chunks = await indexed.document_chunks("doc-vacation")
    assert [chunk.ordinal for chunk in chunks] == list(range(len(chunks)))
    assert len(chunks) == summary.chunk_count


async def test_a_chunk_can_be_fetched_by_id(indexed: MemoryVectorStore) -> None:
    """The last step of verifying a citation: the exact text the model was shown."""
    chunks = await indexed.document_chunks("doc-expenses")
    fetched = await indexed.get_chunk(chunks[0].id)

    assert fetched is not None
    assert fetched.text == chunks[0].text


async def test_missing_records_return_none_rather_than_raising(
    indexed: MemoryVectorStore,
) -> None:
    assert await indexed.get_document("nope") is None
    assert await indexed.get_chunk("nope") is None
    assert await indexed.document_chunks("nope") == []


async def test_a_deleted_document_leaves_no_trace(indexed: MemoryVectorStore) -> None:
    await indexed.delete_document("doc-vacation")

    assert await indexed.get_document("doc-vacation") is None
    assert await indexed.document_chunks("doc-vacation") == []
    assert (await indexed.statistics()).documents == 2


async def test_a_document_that_produced_no_chunks_is_still_visible(
    store: MemoryVectorStore, embeddings
) -> None:
    """The one an operator is hunting for: indexed, and invisible to retrieval."""
    empty = Document(id="doc-empty", source_uri="file:///empty.md", title="Empty", text="   ")
    pipeline = IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions()), embeddings=embeddings, store=store
    )
    await pipeline.ingest(InMemoryLoader([empty]).load())

    # The pipeline reports an empty document rather than storing it, so nothing is
    # indexed at all — which the statistics must show honestly.
    assert (await store.statistics()).documents == 0
