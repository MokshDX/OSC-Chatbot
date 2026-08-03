"""Core domain types.

These are the only types that cross module boundaries. Nothing here knows about
HTTP, SQL, or any provider SDK — provider adapters translate to and from these
shapes at their own edges, which is what makes providers swappable.

Frozen dataclasses are used rather than Pydantic models because these values are
constructed internally and never parsed from untrusted input; validation belongs
at the trust boundary (the API schemas and the settings module), not here.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any

type Vector = list[float]
"""A dense embedding. Length is fixed by the active embedding model."""

type Metadata = Mapping[str, Any]


def content_hash(text: str) -> str:
    """Return a stable digest of `text`, used to skip unchanged documents on re-sync."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- corpus


@dataclass(frozen=True, slots=True)
class Document:
    """A source document as fetched by a connector, before chunking."""

    id: str
    source_uri: str
    title: str
    text: str
    metadata: Metadata = field(default_factory=dict)
    updated_at: datetime | None = None

    @property
    def hash(self) -> str:
        return content_hash(self.text)


@dataclass(frozen=True, slots=True)
class LoadFailure:
    """A source file a connector found but could not turn into a `Document`.

    Carries the `document_id` the file *would* have had, which is what lets the
    ingestion pipeline distinguish "this document was deleted from the source"
    from "this document is still there but unreadable today". Without that
    distinction a transient parse failure would prune a healthy document out of
    the index.
    """

    document_id: str
    source_uri: str
    error: str


@dataclass(frozen=True, slots=True)
class Chunk:
    """A retrievable span of a document.

    `title` and `source_uri` are denormalised from the parent document so that a
    retrieval hit is self-describing: the generation layer can cite it without a
    second lookup, and non-SQL vector stores need not support joins.
    """

    id: str
    document_id: str
    ordinal: int
    text: str
    title: str
    source_uri: str
    metadata: Metadata = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class EmbeddedChunk:
    """A chunk paired with the vector produced for it, tagged with its model.

    The model id travels with the vector so a store can refuse to compare vectors
    produced by different models.
    """

    chunk: Chunk
    vector: Vector
    embedding_model: str


class MatchSource(StrEnum):
    """Where a retrieval hit came from. Recorded for tracing and evaluation."""

    VECTOR = "vector"
    KEYWORD = "keyword"
    HYBRID = "hybrid"
    RERANK = "rerank"


@dataclass(frozen=True, slots=True)
class ScoredChunk:
    """A chunk with a relevance score.

    Scores are only comparable within a single retrieval strategy: a cosine
    similarity, an RRF score, and a cross-encoder logit are on different scales.
    `source` records which produced this score.
    """

    chunk: Chunk
    score: float
    source: MatchSource


# ---------------------------------------------------------------------- inspection


@dataclass(frozen=True, slots=True)
class DocumentSummary:
    """What the store knows about one indexed document.

    Distinct from `Document`: it carries no text (a corpus document can be
    megabytes) but does carry what only the store knows — how many chunks the
    document produced and when it was last indexed. Those two facts answer most
    "why is this document not being retrieved?" questions on their own.
    """

    id: str
    title: str
    source_uri: str
    content_hash: str
    chunk_count: int
    metadata: Metadata = field(default_factory=dict)
    updated_at: datetime | None = None
    indexed_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class IndexStatistics:
    """Aggregate state of the index.

    Chunk length percentiles are here because chunk size is the highest-leverage
    retrieval knob in the system and the only honest way to check the configured
    target is being met is to measure what was actually stored — a `chunk_size` of
    900 with a p95 of 180 means the separators are firing far too early.
    """

    workspace_id: str
    documents: int
    chunks: int
    embedding_models: list[str]
    dimensions: int
    chunk_chars_min: int = 0
    chunk_chars_mean: float = 0.0
    chunk_chars_p50: int = 0
    chunk_chars_p95: int = 0
    chunk_chars_max: int = 0
    documents_by_extension: Mapping[str, int] = field(default_factory=dict)
    last_indexed_at: datetime | None = None


# ------------------------------------------------------------------------ inference


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True, slots=True)
class Message:
    role: Role
    content: str


@dataclass(frozen=True, slots=True)
class SourceDocument:
    """A retrieved chunk presented to the model as grounding material."""

    chunk_id: str
    document_id: str
    title: str
    source_uri: str
    text: str


@dataclass(frozen=True, slots=True)
class Citation:
    """A reference from the answer back to the material that supports it.

    `index` is the 1-based marker rendered in the answer text (`[1]`, `[2]`, ...),
    so both natively-citing providers and marker-parsing fallbacks produce the same
    shape for the client.
    """

    index: int
    chunk_id: str
    document_id: str
    title: str
    source_uri: str
    quoted_text: str = ""


@dataclass(frozen=True, slots=True)
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0

    def __add__(self, other: Usage) -> Usage:
        return Usage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            cached_input_tokens=self.cached_input_tokens + other.cached_input_tokens,
        )


@dataclass(frozen=True, slots=True)
class ChatRequest:
    """A provider-neutral generation request.

    `sources`, when present, is grounding material. Providers with native citation
    support attach it as structured documents; the rest render it into the prompt.
    Either way the response carries `Citation` objects.

    `temperature` is advisory: several current models reject sampling parameters
    outright, so adapters are free to ignore it. Do not rely on it for determinism.
    """

    messages: list[Message]
    system: str | None = None
    sources: list[SourceDocument] = field(default_factory=list)
    max_tokens: int = 4096
    temperature: float | None = None


@dataclass(frozen=True, slots=True)
class ChatResponse:
    text: str
    citations: list[Citation] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)
    model: str = ""
    stop_reason: str | None = None


@dataclass(frozen=True, slots=True)
class TextDelta:
    """An incremental fragment of the answer."""

    text: str


@dataclass(frozen=True, slots=True)
class CitationDelta:
    """A citation resolved mid-stream."""

    citation: Citation


@dataclass(frozen=True, slots=True)
class StreamEnd:
    usage: Usage
    stop_reason: str | None = None


type StreamEvent = TextDelta | CitationDelta | StreamEnd


# ------------------------------------------------------------------------- answers


@dataclass(frozen=True, slots=True)
class Answer:
    """The result of one question, with everything needed to audit it.

    `trace_id` identifies the execution trace that produced this answer. It is
    returned to clients and printed by the CLI so that "this answer is wrong" can
    be turned into "here is every stage that produced it" without reproducing the
    request — the single most useful thing to have when a user reports a bad answer
    hours later.
    """

    text: str
    citations: list[Citation]
    retrieved: list[ScoredChunk]
    usage: Usage
    model: str
    abstained: bool = False
    trace_id: str = ""
