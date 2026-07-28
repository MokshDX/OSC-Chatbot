"""Shared test fixtures and in-process test doubles.

The doubles are deliberately real implementations of the protocols rather than
mocks: the point of the protocol layer is that the pipelines cannot tell a stub
from a provider, and these prove it. Every test in this suite runs with no
network, no database and no API credential.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import AsyncIterator, Sequence

import pytest

from osc_assistant.providers.vectorstores.memory import MemoryVectorStore
from osc_assistant.types import (
    ChatRequest,
    ChatResponse,
    Citation,
    Document,
    StreamEnd,
    StreamEvent,
    TextDelta,
    Usage,
    Vector,
)

EMBEDDING_DIMENSIONS = 32
_TOKEN_PATTERN = re.compile(r"\w+")


class StubEmbeddingModel:
    """A deterministic bag-of-words embedder.

    Hashes each token into a fixed number of buckets, so texts sharing vocabulary
    land near each other under cosine similarity. That makes retrieval assertions
    meaningful without a model download, and identical on every machine.
    """

    def __init__(self, dimensions: int = EMBEDDING_DIMENSIONS) -> None:
        self._dimensions = dimensions
        self.embed_calls = 0

    @property
    def model_id(self) -> str:
        return "stub-embedding"

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed_documents(self, texts: Sequence[str]) -> list[Vector]:
        self.embed_calls += 1
        return [self._encode(text) for text in texts]

    async def embed_query(self, text: str) -> Vector:
        return self._encode(text)

    def _encode(self, text: str) -> Vector:
        vector = [0.0] * self._dimensions
        for token in _TOKEN_PATTERN.findall(text.lower()):
            digest = hashlib.sha256(token.encode()).digest()
            vector[digest[0] % self._dimensions] += 1.0
        return vector


class StubChatModel:
    """A chat model that returns a scripted reply.

    `supports_citations` is False, so it exercises the marker-parsing path that
    every non-Anthropic provider uses.
    """

    def __init__(self, reply: str = "The answer is documented. [1]") -> None:
        self.reply = reply
        self.requests: list[ChatRequest] = []

    @property
    def model_id(self) -> str:
        return "stub-chat"

    @property
    def supports_citations(self) -> bool:
        return False

    async def complete(self, request: ChatRequest) -> ChatResponse:
        from osc_assistant.grounding import parse_marker_citations

        self.requests.append(request)
        return ChatResponse(
            text=self.reply,
            citations=parse_marker_citations(self.reply, request.sources),
            usage=Usage(input_tokens=100, output_tokens=20),
            model=self.model_id,
        )

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        from osc_assistant.grounding import parse_marker_citations
        from osc_assistant.types import CitationDelta

        self.requests.append(request)
        # Split into several deltas so tests exercise reassembly rather than a
        # single-chunk fast path.
        for word in self.reply.split(" "):
            yield TextDelta(text=word + " ")
        for citation in parse_marker_citations(self.reply, request.sources):
            yield CitationDelta(citation=citation)
        yield StreamEnd(usage=Usage(input_tokens=100, output_tokens=20))


class NativeCitationChatModel:
    """A chat model that resolves citations itself, as Anthropic does."""

    def __init__(self, text: str = "Grounded answer.[1]") -> None:
        self.text = text

    @property
    def model_id(self) -> str:
        return "stub-native"

    @property
    def supports_citations(self) -> bool:
        return True

    async def complete(self, request: ChatRequest) -> ChatResponse:
        citations = [
            Citation(
                index=1,
                chunk_id=request.sources[0].chunk_id,
                document_id=request.sources[0].document_id,
                title=request.sources[0].title,
                source_uri=request.sources[0].source_uri,
                quoted_text=request.sources[0].text[:40],
            )
        ]
        return ChatResponse(text=self.text, citations=citations, model=self.model_id)

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        from osc_assistant.types import CitationDelta

        response = await self.complete(request)
        yield TextDelta(text=response.text)
        for citation in response.citations:
            yield CitationDelta(citation=citation)
        yield StreamEnd(usage=Usage())


class FailingChatModel:
    """Raises on every call. Used to prove graceful degradation."""

    @property
    def model_id(self) -> str:
        return "failing"

    @property
    def supports_citations(self) -> bool:
        return False

    async def complete(self, request: ChatRequest) -> ChatResponse:
        raise RuntimeError("provider unavailable")

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        raise RuntimeError("provider unavailable")
        yield  # pragma: no cover - unreachable, makes this an async generator


@pytest.fixture
def embeddings() -> StubEmbeddingModel:
    return StubEmbeddingModel()


@pytest.fixture
def store() -> MemoryVectorStore:
    return MemoryVectorStore(dimensions=EMBEDDING_DIMENSIONS)


@pytest.fixture
def documents() -> list[Document]:
    return [
        Document(
            id="doc-vacation",
            source_uri="file:///handbook/vacation.md",
            title="Vacation Policy",
            text=(
                "# Vacation Policy\n\n"
                "OSC employees accrue twenty five vacation days each calendar year. "
                "Vacation requests are approved by your line manager. "
                "Unused vacation days expire on the thirty first of March."
            ),
        ),
        Document(
            id="doc-expenses",
            source_uri="file:///handbook/expenses.md",
            title="Expense Policy",
            text=(
                "# Expense Policy\n\n"
                "Expense claims must be submitted within thirty days. "
                "Receipts are required for any expense above twenty euros. "
                "Reimbursement is paid with the next payroll run."
            ),
        ),
        Document(
            id="doc-onboarding",
            source_uri="file:///handbook/onboarding.md",
            title="Onboarding Guide",
            text=(
                "# Onboarding Guide\n\n"
                "New joiners receive a laptop on their first day. "
                "Accounts are provisioned by the platform team within one working day."
            ),
        ),
    ]
