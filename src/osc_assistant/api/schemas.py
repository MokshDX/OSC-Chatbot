"""HTTP request and response models.

These are separate from the domain types in `types` on purpose. They are the trust
boundary — this is where untrusted input is validated and where the wire format is
pinned — and keeping them apart means an internal refactor cannot silently change
the public API, nor a wire-format change leak into the domain.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ..types import Answer, Citation, Message, Role, ScoredChunk

MAX_QUESTION_LENGTH = 4000
MAX_HISTORY_MESSAGES = 40


class MessageBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=MAX_QUESTION_LENGTH)

    def to_domain(self) -> Message:
        return Message(role=Role(self.role), content=self.content)


class ChatRequestBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1, max_length=MAX_QUESTION_LENGTH)
    history: list[MessageBody] = Field(default_factory=list, max_length=MAX_HISTORY_MESSAGES)
    stream: bool = Field(
        default=True,
        description="Server-sent events when true, a single JSON response when false.",
    )

    def domain_history(self) -> list[Message]:
        return [message.to_domain() for message in self.history]


class SearchRequestBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1, max_length=MAX_QUESTION_LENGTH)


class CitationBody(BaseModel):
    index: int
    chunk_id: str
    document_id: str
    title: str
    source_uri: str
    quoted_text: str

    @classmethod
    def from_domain(cls, citation: Citation) -> CitationBody:
        return cls(
            index=citation.index,
            chunk_id=citation.chunk_id,
            document_id=citation.document_id,
            title=citation.title,
            source_uri=citation.source_uri,
            quoted_text=citation.quoted_text,
        )


class RetrievedChunkBody(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    source_uri: str
    score: float
    source: str
    excerpt: str

    @classmethod
    def from_domain(cls, scored: ScoredChunk, excerpt_chars: int = 320) -> RetrievedChunkBody:
        return cls(
            chunk_id=scored.chunk.id,
            document_id=scored.chunk.document_id,
            title=scored.chunk.title,
            source_uri=scored.chunk.source_uri,
            score=scored.score,
            source=scored.source.value,
            excerpt=scored.chunk.text[:excerpt_chars],
        )


class UsageBody(BaseModel):
    input_tokens: int
    output_tokens: int
    cached_input_tokens: int


class AnswerBody(BaseModel):
    """The final answer.

    `abstained` is authoritative: when true the assistant declined to answer, and
    any text streamed earlier in the same request must be discarded by the client.
    """

    text: str
    citations: list[CitationBody]
    retrieved: list[RetrievedChunkBody]
    usage: UsageBody
    model: str
    abstained: bool

    @classmethod
    def from_domain(cls, answer: Answer) -> AnswerBody:
        return cls(
            text=answer.text,
            citations=[CitationBody.from_domain(citation) for citation in answer.citations],
            retrieved=[RetrievedChunkBody.from_domain(hit) for hit in answer.retrieved],
            usage=UsageBody(
                input_tokens=answer.usage.input_tokens,
                output_tokens=answer.usage.output_tokens,
                cached_input_tokens=answer.usage.cached_input_tokens,
            ),
            model=answer.model,
            abstained=answer.abstained,
        )


class SearchResponseBody(BaseModel):
    """Retrieval results without generation. The debugging and evaluation surface."""

    query: str
    original_query: str
    results: list[RetrievedChunkBody]
    candidates_considered: int
    duration_seconds: float


class ComponentBody(BaseModel):
    provider: str
    model: str


class HealthBody(BaseModel):
    """Health plus the active component set, so a deployment is self-describing."""

    status: Literal["ok"]
    environment: str
    workspace_id: str
    llm: ComponentBody
    embeddings: ComponentBody
    vector_store: ComponentBody
    reranker: ComponentBody
    chunking_strategy: str
    retrieval_strategy: str


class ErrorBody(BaseModel):
    error: str
    detail: str
