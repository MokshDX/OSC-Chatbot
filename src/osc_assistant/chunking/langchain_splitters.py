"""Chunkers backed by `langchain-text-splitters`.

**Why adopt a library here, of all places.** Chunking is the one part of this
system where the problem is genuinely generic — split text on the coarsest
boundary that fits — and where OSC's own implementation was carrying known rough
edges: overlap is prepended after packing, so a chunk can exceed its size budget by
up to `chunk_overlap`, and the overlap slice can cut mid-word. Those are solved
problems. `langchain-text-splitters` is a small, pure-Python package with no vendor
dependency, and it brings structure-aware splitting that would otherwise have to be
written and maintained here.

**Why `recursive` is still the default.** Switching the default chunker changes
every chunk boundary and therefore every chunk id in a live index, and the project's
own rule is that a retrieval change ships with a measured improvement. There is no
golden set yet. The LangChain strategies are registered, tested and one profile line
away; the number that justifies promoting one belongs to the evaluation harness.
Until then `recursive` stays, and nobody's index moves without asking.

Two strategies are registered:

* `langchain_recursive` — the direct counterpart to OSC's `recursive`, with the
  overlap handled correctly.
* `markdown` — splits on heading structure first, then packs each section to size.
  The heading path is attached to chunk metadata, so a retrieved passage knows
  which section of which document it came from without re-reading the source.

Chunk ids come from the same helper the built-in chunkers use, so idempotent
ingestion behaves identically whichever strategy is configured.

Note on text fidelity: these splitters trim whitespace at boundaries, as OSC's own
chunker does. Neither adds, removes or reorders visible characters, which is the
invariant that matters — chunk text is quoted back as citation evidence.
"""

from __future__ import annotations

from typing import Any

from pydantic import ConfigDict, Field

from ..errors import MissingDependencyError
from ..protocols import Chunker
from ..registries import chunker_registry
from ..registry import ComponentConfig
from ..types import Chunk, Document
from .recursive import DEFAULT_SEPARATORS, ChunkerOptions, to_chunks

# Markdown levels worth splitting on. Deeper levels (`####` and below) are treated
# as body text: splitting there produces fragments too small to answer a question,
# which costs more in retrieval quality than the extra structure returns.
_MARKDOWN_HEADERS: list[tuple[str, str]] = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]


class LangChainChunkerOptions(ChunkerOptions):
    """`ChunkerOptions` plus the settings only the LangChain splitters expose."""

    model_config = ConfigDict(extra="forbid")

    keep_separator: bool = Field(
        default=True,
        description=(
            "Retain the separator in the chunk that follows it. On by default: a "
            "section that loses its own heading loses the terms most likely to match "
            "a query about it."
        ),
    )


def _require_splitters() -> Any:
    try:
        import langchain_text_splitters
    except ImportError as exc:  # pragma: no cover - a core dependency
        raise MissingDependencyError(
            "langchain chunker", "langchain-text-splitters", "langchain"
        ) from exc
    return langchain_text_splitters


class LangChainRecursiveChunker:
    """`RecursiveCharacterTextSplitter` behind the OSC `Chunker` protocol."""

    def __init__(self, options: LangChainChunkerOptions) -> None:
        self._options = options.validated()
        splitters = _require_splitters()
        self._splitter = splitters.RecursiveCharacterTextSplitter(
            chunk_size=options.chunk_size,
            chunk_overlap=options.chunk_overlap,
            separators=[*options.separators, ""],
            keep_separator=options.keep_separator,
        )

    def split(self, document: Document) -> list[Chunk]:
        return to_chunks(document, self._splitter.split_text(document.text.strip()))


class MarkdownChunker:
    """Heading-aware splitting: structure first, then size.

    Two passes, because either alone is wrong. Splitting only on headings produces
    chunks of wildly varying size — a long section becomes one chunk too big for the
    prompt budget. Splitting only on size cuts across section boundaries and puts
    the answer to a question in a chunk that does not contain that question's
    heading. Structure first, then pack, gets both.

    The heading path is recorded on each chunk's metadata (`section`), which makes
    a retrieval hit self-describing: "Expense Policy > Approval thresholds" is a
    materially better thing to show beside a citation than a chunk ordinal.
    """

    def __init__(self, options: LangChainChunkerOptions) -> None:
        self._options = options.validated()
        splitters = _require_splitters()
        # strip_headers=False keeps the heading line inside the chunk text. Removing
        # it would make the stored text differ from the source, and that text is
        # quoted back to users as citation evidence.
        self._headers = splitters.MarkdownHeaderTextSplitter(
            _MARKDOWN_HEADERS, strip_headers=False
        )
        self._packer = splitters.RecursiveCharacterTextSplitter(
            chunk_size=options.chunk_size,
            chunk_overlap=options.chunk_overlap,
            separators=[*options.separators, ""],
            keep_separator=options.keep_separator,
        )

    def split(self, document: Document) -> list[Chunk]:
        text = document.text.strip()
        if not text:
            return []

        texts: list[str] = []
        sections: list[str] = []
        for section in self._headers.split_text(text):
            heading = _heading_path(section.metadata)
            for piece in self._packer.split_text(section.page_content):
                texts.append(piece)
                sections.append(heading)

        chunks = to_chunks(document, texts, extra_metadata=_section_metadata(sections))
        return chunks


def _heading_path(metadata: dict[str, Any]) -> str:
    """Join whichever heading levels are present into a readable path."""
    return " > ".join(
        str(metadata[key]) for _, key in _MARKDOWN_HEADERS if metadata.get(key)
    )


def _section_metadata(sections: list[str]) -> list[dict[str, Any]]:
    return [{"section": section} if section else {} for section in sections]


@chunker_registry.register("langchain_recursive")
def _build_langchain_recursive(config: ComponentConfig) -> Chunker:
    return LangChainRecursiveChunker(LangChainChunkerOptions.model_validate(config.options))


@chunker_registry.register("markdown")
def _build_markdown(config: ComponentConfig) -> Chunker:
    return MarkdownChunker(LangChainChunkerOptions.model_validate(config.options))


__all__ = [
    "DEFAULT_SEPARATORS",
    "LangChainChunkerOptions",
    "LangChainRecursiveChunker",
    "MarkdownChunker",
]
