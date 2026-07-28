"""Corpus connectors.

A loader is any object with `load() -> AsyncIterator[Document]`. It turns an
external system into a stream of documents and nothing else: no chunking, no
embedding, no persistence. That keeps a new connector (Confluence, Drive,
SharePoint) a self-contained addition with no reach into the rest of the pipeline.

Documents are yielded lazily so a large corpus never has to be held in memory.
"""

from __future__ import annotations

import hashlib
from collections.abc import AsyncIterator, Iterable, Sequence
from datetime import UTC, datetime
from pathlib import Path

from ..chunking import normalize_whitespace
from ..logging import get_logger
from ..types import Document

log = get_logger(__name__)

DEFAULT_EXTENSIONS: tuple[str, ...] = (".md", ".markdown", ".txt", ".rst")


def stable_document_id(source_uri: str) -> str:
    """Derive a stable id from a source URI.

    Hashed rather than slugified so the id is fixed-length and safe in a URL, and
    so two documents whose paths differ only in characters a slug would strip
    cannot collide.
    """
    return hashlib.sha256(source_uri.encode("utf-8")).hexdigest()[:24]


class FilesystemLoader:
    """Loads text documents from a directory tree.

    The Phase 1 connector: it needs no credentials, which makes it the fastest way
    to get real content in front of the retrieval and evaluation stack.
    """

    def __init__(
        self,
        root: Path,
        extensions: Sequence[str] = DEFAULT_EXTENSIONS,
        encoding: str = "utf-8",
    ) -> None:
        self._root = root
        self._extensions = {extension.lower() for extension in extensions}
        self._encoding = encoding

    async def load(self) -> AsyncIterator[Document]:
        if not self._root.exists():
            raise FileNotFoundError(f"Corpus directory not found: {self._root}")

        for path in sorted(self._root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in self._extensions:
                continue
            document = self._read(path)
            if document is not None:
                yield document

    def _read(self, path: Path) -> Document | None:
        try:
            raw = path.read_text(encoding=self._encoding)
        except (OSError, UnicodeDecodeError) as exc:
            # One unreadable file must not abort a corpus-wide sync.
            log.warning("loader.unreadable", extra={"path": str(path), "error": str(exc)})
            return None

        text = normalize_whitespace(raw).strip()
        if not text:
            return None

        source_uri = path.resolve().as_uri()
        return Document(
            id=stable_document_id(source_uri),
            source_uri=source_uri,
            title=_derive_title(text, path),
            text=text,
            metadata={"relative_path": str(path.relative_to(self._root))},
            updated_at=datetime.fromtimestamp(path.stat().st_mtime, tz=UTC),
        )


class InMemoryLoader:
    """Serves a fixed list of documents. Used by tests and the evaluation harness."""

    def __init__(self, documents: Iterable[Document]) -> None:
        self._documents = list(documents)

    async def load(self) -> AsyncIterator[Document]:
        for document in self._documents:
            yield document


def _derive_title(text: str, path: Path) -> str:
    """Use the first Markdown heading as the title, else the filename.

    Titles are shown next to every citation, so a readable one materially improves
    whether a user trusts an answer.
    """
    for line in text.splitlines()[:10]:
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                return heading
    return path.stem.replace("-", " ").replace("_", " ").title()
