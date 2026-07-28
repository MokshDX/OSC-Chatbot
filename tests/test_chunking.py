"""Chunking tests.

Chunk id stability is the load-bearing property here: ingestion idempotency
depends on identical input producing identical ids.
"""

from __future__ import annotations

import pytest

from osc_assistant.chunking import ChunkerOptions, FixedSizeChunker, RecursiveChunker
from osc_assistant.types import Document


def _document(text: str) -> Document:
    return Document(
        id="doc-1",
        source_uri="file:///doc.md",
        title="Doc",
        text=text,
    )


def test_short_document_is_a_single_chunk() -> None:
    chunker = RecursiveChunker(ChunkerOptions(chunk_size=1000, chunk_overlap=50))
    chunks = chunker.split(_document("A short policy statement."))

    assert len(chunks) == 1
    assert chunks[0].text == "A short policy statement."
    assert chunks[0].ordinal == 0


def test_chunks_respect_the_size_budget() -> None:
    chunker = RecursiveChunker(ChunkerOptions(chunk_size=200, chunk_overlap=20))
    paragraphs = "\n\n".join(f"Paragraph {index} about OSC policy." for index in range(40))

    chunks = chunker.split(_document(paragraphs))

    assert len(chunks) > 1
    # Overlap is prepended after packing, so a chunk may exceed the target by up
    # to the overlap. Anything beyond that means the packing logic is broken.
    assert all(len(chunk.text) <= 200 + 20 for chunk in chunks)


def test_ordinals_are_contiguous() -> None:
    chunker = RecursiveChunker(ChunkerOptions(chunk_size=120, chunk_overlap=10))
    chunks = chunker.split(_document("word " * 400))

    assert [chunk.ordinal for chunk in chunks] == list(range(len(chunks)))


def test_chunk_ids_are_stable_across_runs() -> None:
    """Ingestion skips unchanged documents by hash; ids must not drift."""
    chunker = RecursiveChunker(ChunkerOptions(chunk_size=150, chunk_overlap=20))
    document = _document("Policy sentence. " * 40)

    first = [chunk.id for chunk in chunker.split(document)]
    second = [chunk.id for chunk in chunker.split(document)]

    assert first == second


def test_chunk_ids_change_when_content_changes() -> None:
    """Otherwise an edit would leave stale chunks retrievable after re-indexing."""
    chunker = RecursiveChunker(ChunkerOptions(chunk_size=150, chunk_overlap=20))

    original = chunker.split(_document("The limit is twenty euros."))[0]
    edited = chunker.split(_document("The limit is fifty euros."))[0]

    assert original.id != edited.id


def test_document_metadata_is_denormalised_onto_chunks() -> None:
    """A retrieval hit must be citable without a second lookup."""
    chunker = RecursiveChunker(ChunkerOptions())
    chunks = chunker.split(_document("Some content."))

    assert chunks[0].title == "Doc"
    assert chunks[0].source_uri == "file:///doc.md"
    assert chunks[0].document_id == "doc-1"


def test_empty_document_produces_no_chunks() -> None:
    chunker = RecursiveChunker(ChunkerOptions())
    assert chunker.split(_document("   \n\n  ")) == []


def test_unbroken_text_is_still_split() -> None:
    """No separator exists in a single long token; the hard split must catch it."""
    chunker = RecursiveChunker(ChunkerOptions(chunk_size=100, chunk_overlap=0))
    chunks = chunker.split(_document("x" * 500))

    assert len(chunks) >= 5
    assert all(len(chunk.text) <= 100 for chunk in chunks)


def test_fixed_chunker_overlaps_windows() -> None:
    chunker = FixedSizeChunker(ChunkerOptions(chunk_size=100, chunk_overlap=25))
    chunks = chunker.split(_document("abcdefghij" * 30))

    assert len(chunks) > 1
    # Consecutive windows advance by (size - overlap), so the tail of one appears
    # at the head of the next.
    assert chunks[0].text[-25:] == chunks[1].text[:25]


def test_overlap_must_be_smaller_than_chunk_size() -> None:
    with pytest.raises(ValueError, match="chunk_overlap"):
        RecursiveChunker(ChunkerOptions(chunk_size=100, chunk_overlap=100))


def test_chunking_preserves_document_content() -> None:
    """Chunk text is quoted back to users as citation evidence, so the chunker
    must not add or drop a character. It previously appended a separator to the
    final fragment, making cited "evidence" text the source never contained."""
    chunker = RecursiveChunker(ChunkerOptions(chunk_size=100, chunk_overlap=0))
    text = ("Alpha beta gamma delta. " * 12).strip()

    chunks = chunker.split(_document(text))

    # Compared without whitespace: chunk boundaries are deliberately trimmed, but
    # no visible character may be invented or lost.
    assert "".join("".join(chunk.text.split()) for chunk in chunks) == "".join(text.split())


def test_chunking_preserves_content_across_separator_kinds() -> None:
    chunker = RecursiveChunker(ChunkerOptions(chunk_size=120, chunk_overlap=0))
    text = "# Title\n\nFirst para. Second sentence here.\n\n## Section\n\n" + "word " * 60

    chunks = chunker.split(_document(text))

    assert "".join("".join(chunk.text.split()) for chunk in chunks) == "".join(text.split())
