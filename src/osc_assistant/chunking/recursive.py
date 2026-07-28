"""Chunking strategies.

Chunking is the single highest-leverage retrieval knob and the one we expect to
change most often, so both strategies are registered components selected by
configuration rather than a hard-coded function.

Chunk ids are derived from the document id and the chunk's content, which makes
ingestion idempotent: re-running over an unchanged document produces identical ids
and the upsert is a no-op.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict, Field

from ..protocols import Chunker
from ..registries import chunker_registry
from ..registry import ComponentConfig
from ..types import Chunk, Document

# Ordered coarsest to finest. Splitting at the coarsest boundary that fits keeps
# semantically related text together, which matters more for retrieval quality
# than hitting the target size exactly.
DEFAULT_SEPARATORS: tuple[str, ...] = ("\n## ", "\n### ", "\n\n", "\n", ". ", " ")


class ChunkerOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chunk_size: int = Field(default=1200, ge=100, description="Target size in characters.")
    chunk_overlap: int = Field(default=150, ge=0)
    separators: tuple[str, ...] = DEFAULT_SEPARATORS

    def validated(self) -> ChunkerOptions:
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        return self


class RecursiveChunker:
    """Splits on the coarsest separator that keeps chunks under the target size.

    Falls back to a hard character split when no separator helps, so a single
    enormous unbroken line can never produce an oversized chunk.
    """

    def __init__(self, options: ChunkerOptions) -> None:
        self._options = options.validated()

    def split(self, document: Document) -> list[Chunk]:
        pieces = self._split_text(document.text.strip(), list(self._options.separators))
        merged = _merge(pieces, self._options.chunk_size, self._options.chunk_overlap)
        return _to_chunks(document, merged)

    def _split_text(self, text: str, separators: list[str]) -> list[str]:
        if len(text) <= self._options.chunk_size:
            return [text] if text else []

        for index, separator in enumerate(separators):
            if separator not in text:
                continue
            remaining = separators[index + 1 :]
            output: list[str] = []
            for part in _split_keeping_separator(text, separator):
                if len(part) <= self._options.chunk_size:
                    output.append(part)
                else:
                    output.extend(self._split_text(part, remaining))
            return output

        size = self._options.chunk_size
        return [text[start : start + size] for start in range(0, len(text), size)]


class FixedSizeChunker:
    """Fixed-width character windows with overlap.

    Ignores document structure entirely. Kept as an evaluation baseline: if a
    structure-aware strategy cannot beat this on the golden set, it is not earning
    its complexity.
    """

    def __init__(self, options: ChunkerOptions) -> None:
        self._options = options.validated()

    def split(self, document: Document) -> list[Chunk]:
        text = document.text.strip()
        if not text:
            return []

        size = self._options.chunk_size
        stride = size - self._options.chunk_overlap
        windows = [text[start : start + size] for start in range(0, len(text), stride)]
        return _to_chunks(document, [window for window in windows if window.strip()])


def _split_keeping_separator(text: str, separator: str) -> list[str]:
    """Split `text` on `separator` without adding or dropping a character.

    `"".join(_split_keeping_separator(text, sep)) == text` for every input. That
    invariant is the point: chunk text is quoted back to users as citation
    evidence, so a chunker that rewrites its input makes the evidence a forgery.

    Which side the separator lands on depends on what it marks. A leading newline
    (`"\\n## "`) opens the section that follows it; sentence and word separators
    (`". "`, `" "`) close the fragment before them.
    """
    parts = text.split(separator)
    if len(parts) == 1:
        return [text]

    if separator.startswith("\n"):
        restored = [parts[0], *(separator + part for part in parts[1:])]
    else:
        restored = [*(part + separator for part in parts[:-1]), parts[-1]]
    return [part for part in restored if part]


def _merge(pieces: Sequence[str], chunk_size: int, overlap: int) -> list[str]:
    """Greedily pack pieces up to `chunk_size`, carrying `overlap` characters forward.

    The overlap prevents a fact that straddles a boundary from being invisible to
    both neighbouring chunks.
    """
    merged: list[str] = []
    current = ""

    for piece in pieces:
        if not current:
            current = piece
        elif len(current) + len(piece) <= chunk_size:
            current += piece
        else:
            merged.append(current.strip())
            current = (current[-overlap:] + piece) if overlap else piece

    if current.strip():
        merged.append(current.strip())
    return merged


def _to_chunks(document: Document, texts: Sequence[str]) -> list[Chunk]:
    return [
        Chunk(
            id=_chunk_id(document.id, ordinal, text),
            document_id=document.id,
            ordinal=ordinal,
            text=text,
            title=document.title,
            source_uri=document.source_uri,
            metadata=dict(document.metadata),
        )
        for ordinal, text in enumerate(texts)
        if text.strip()
    ]


def _chunk_id(document_id: str, ordinal: int, text: str) -> str:
    """A stable id for a chunk.

    Content is part of the digest so that an edit which shifts text between chunks
    produces new ids, and the sync's delete-then-insert leaves nothing stale behind.
    """
    digest = hashlib.sha256(f"{document_id}:{ordinal}:{text}".encode()).hexdigest()
    return f"{document_id}:{ordinal}:{digest[:12]}"


def normalize_whitespace(text: str) -> str:
    """Collapse runs of blank lines. Applied by loaders before chunking."""
    return re.sub(r"\n{3,}", "\n\n", text.replace("\r\n", "\n"))


@chunker_registry.register("recursive")
def _build_recursive(config: ComponentConfig) -> Chunker:
    return RecursiveChunker(ChunkerOptions.model_validate(config.options))


@chunker_registry.register("fixed")
def _build_fixed(config: ComponentConfig) -> Chunker:
    return FixedSizeChunker(ChunkerOptions.model_validate(config.options))
