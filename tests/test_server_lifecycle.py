"""Startup, shutdown and in-flight failure behaviour of the service.

These cover the parts of running a server that only show up when something is
wrong or unusual: a stream that fails after the headers are sent, an empty index
that makes a healthy service look broken, and provider resources that were never
released because nobody had asked them to be.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterator, Sequence

import pytest
from fastapi.testclient import TestClient

from osc_assistant.api import create_app
from osc_assistant.api.banner import startup_notes
from osc_assistant.container import Container
from osc_assistant.errors import ProviderError
from osc_assistant.registries import embedding_registry, llm_registry
from osc_assistant.registry import ComponentConfig
from osc_assistant.settings import (
    ChunkingSettings,
    GenerationSettings,
    RetrievalSettings,
    Settings,
)
from osc_assistant.types import (
    ChatRequest,
    ChatResponse,
    Document,
    StreamEvent,
    TextDelta,
    Usage,
    Vector,
)

from .conftest import StubChatModel, StubEmbeddingModel


def _settings(**overrides: object) -> Settings:
    base = {
        "environment": "test",
        "log_format": "text",
        "llm": ComponentConfig(provider="stub", model="stub-chat"),
        "fast_llm": ComponentConfig(provider="stub", model="stub-chat"),
        "embeddings": ComponentConfig(provider="stub", model="stub-embedding"),
        "vector_store": ComponentConfig(provider="memory"),
        "chunking": ChunkingSettings(chunk_size=400, chunk_overlap=40),
        "retrieval": RetrievalSettings(rewrite_queries=False, top_k=4),
        "generation": GenerationSettings(require_citations=True),
    }
    return Settings(**{**base, **overrides})  # type: ignore[arg-type]


@pytest.fixture(autouse=True)
def _stub_providers() -> None:
    embedding_registry.register("stub")(lambda config: StubEmbeddingModel())
    llm_registry.register("stub")(lambda config: StubChatModel())


# --------------------------------------------------------------- startup notes


async def test_an_empty_index_is_reported_at_startup() -> None:
    """A service that starts perfectly and abstains from everything looks broken.

    It is indistinguishable from a failing model unless somebody thinks to look, so
    the service says it before the first request rather than after the first
    confusing answer.
    """
    async with Container(_settings()) as container:
        notes = await startup_notes(container, container.settings)

    assert any("index is empty" in note for note in notes)


async def test_a_populated_index_produces_no_note(documents: list[Document]) -> None:
    from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
    from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader

    # `development`, so the unauthenticated-service note does not fire and the
    # assertion is about the index alone.
    settings = _settings(environment="development")
    async with Container(settings) as container:
        pipeline = IngestionPipeline(
            chunker=RecursiveChunker(ChunkerOptions()),
            embeddings=container.embeddings,
            store=container.vector_store,
        )
        await pipeline.ingest(InMemoryLoader(documents).load())

        assert await startup_notes(container, settings) == []


async def test_a_non_development_environment_is_called_out() -> None:
    """A chat UI on an unauthenticated service is the state most easily mistaken
    for something deployable."""
    settings = _settings(environment="production")

    async with Container(settings) as container:
        notes = await startup_notes(container, settings)

    assert any("authentication" in note for note in notes)


def test_startup_notes_reach_the_structured_log_too(caplog) -> None:
    """A condition worth interrupting a developer for belongs in the log as well."""
    import logging

    # create_app installs this project's logging, which clears root handlers —
    # caplog's included. Re-attaching afterwards is what makes the record visible.
    app = create_app(_settings())
    logging.getLogger().addHandler(caplog.handler)

    with caplog.at_level(logging.INFO), TestClient(app):
        pass

    started = [record for record in caplog.records if record.getMessage() == "service.started"]
    assert started
    assert any("index is empty" in note for note in started[0].notes)  # type: ignore[attr-defined]


# ------------------------------------------------------- in-flight stream failure


class _ExplodingChatModel:
    """Fails partway through a stream, after deltas have already been sent."""

    @property
    def model_id(self) -> str:
        return "exploding"

    @property
    def supports_citations(self) -> bool:
        return False

    async def complete(self, request: ChatRequest) -> ChatResponse:
        raise ProviderError("upstream died")

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        yield TextDelta(text="The answer begins")
        raise RuntimeError("connection reset")


@pytest.fixture
def exploding_client(documents: list[Document]) -> Iterator[TestClient]:
    from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
    from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader

    llm_registry.register("stub")(lambda config: _ExplodingChatModel())
    app = create_app(_settings())
    container: Container = app.state.container

    async def seed() -> None:
        pipeline = IngestionPipeline(
            chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
            embeddings=container.embeddings,
            store=container.vector_store,
        )
        await pipeline.ingest(InMemoryLoader(documents).load())

    asyncio.run(seed())
    with TestClient(app) as client:
        yield client


def test_an_unexpected_stream_failure_still_ends_the_stream(
    exploding_client: TestClient,
) -> None:
    """A client told nothing waits forever.

    The handler previously caught only `AssistantError`, so a bug or an
    undocumented SDK exception closed the connection with no terminal event and
    left the UI spinning. Every exit from the generator must emit one.
    """
    with exploding_client.stream(
        "POST", "/api/chat", json={"question": "how many vacation days", "stream": True}
    ) as response:
        body = "".join(response.iter_text())

    assert "event: error" in body
    assert "RuntimeError" in body


def test_an_unexpected_failure_does_not_leak_internals_to_the_client(
    exploding_client: TestClient,
) -> None:
    """An unexpected exception's message is not part of the API contract."""
    with exploding_client.stream(
        "POST", "/api/chat", json={"question": "how many vacation days", "stream": True}
    ) as response:
        body = "".join(response.iter_text())

    assert "connection reset" not in body
    assert "failed to complete this answer" in body


def test_a_known_provider_failure_keeps_its_actionable_message(
    documents: list[Document],
) -> None:
    """`AssistantError` messages are written for operators and are safe to surface."""
    from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
    from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader

    class _FailingStream(_ExplodingChatModel):
        async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
            yield TextDelta(text="partial")
            raise ProviderError("the completion budget was exhausted")

    llm_registry.register("stub")(lambda config: _FailingStream())
    app = create_app(_settings())
    container: Container = app.state.container

    async def seed() -> None:
        pipeline = IngestionPipeline(
            chunker=RecursiveChunker(ChunkerOptions()),
            embeddings=container.embeddings,
            store=container.vector_store,
        )
        await pipeline.ingest(InMemoryLoader(documents).load())

    asyncio.run(seed())
    with TestClient(app) as client, client.stream(
        "POST", "/api/chat", json={"question": "how many vacation days", "stream": True}
    ) as response:
        body = "".join(response.iter_text())

    assert "budget was exhausted" in body


# ------------------------------------------------------------------- shutdown


class _ClosableEmbedding(StubEmbeddingModel):
    """Holds a resource, like the Voyage and OpenAI adapters do."""

    def __init__(self) -> None:
        super().__init__()
        self.closed = False

    async def aclose(self) -> None:
        self.closed = True


class _SyncClosableReranker:
    """Closes synchronously, to prove both shapes are handled."""

    def __init__(self) -> None:
        self.closed = False

    @property
    def model_id(self) -> str:
        return "closable"

    async def rerank(self, query: str, candidates: Sequence[object], top_k: int) -> list:
        return list(candidates)[:top_k]

    def close(self) -> None:
        self.closed = True


async def test_shutdown_releases_every_component_that_was_built() -> None:
    """Only the vector store was closed before; provider HTTP clients leaked."""
    from osc_assistant.registries import reranker_registry

    embedding = _ClosableEmbedding()
    reranker = _SyncClosableReranker()
    embedding_registry.register("closable")(lambda config: embedding)
    reranker_registry.register("closable")(lambda config: reranker)

    settings = _settings(
        embeddings=ComponentConfig(provider="closable"),
        reranker=ComponentConfig(provider="closable"),
    )
    container = Container(settings)
    await container.startup()
    _ = container.reranker

    await container.shutdown()

    assert embedding.closed
    assert reranker.closed


async def test_shutdown_does_not_construct_what_was_never_used() -> None:
    """`ingest` never builds a chat model; tearing one down would build it.

    That would defeat the lazy graph and fail for want of a credential the command
    never needed.
    """
    built: list[str] = []

    def _explode(config: ComponentConfig) -> object:
        built.append("llm")
        raise AssertionError("the chat model must not be constructed during shutdown")

    llm_registry.register("never")(_explode)

    container = Container(_settings(llm=ComponentConfig(provider="never")))
    await container.startup()
    await container.shutdown()

    assert built == []


async def test_a_component_that_fails_to_close_does_not_break_shutdown() -> None:
    """Shutdown runs on the failure path too; it must not mask the original error."""

    class _BadClose(StubEmbeddingModel):
        async def aclose(self) -> None:
            raise RuntimeError("close failed")

    embedding_registry.register("bad-close")(lambda config: _BadClose())
    container = Container(_settings(embeddings=ComponentConfig(provider="bad-close")))
    await container.startup()

    await container.shutdown()  # must not raise


async def test_embedding_vectors_are_unaffected_by_the_close_probe() -> None:
    """A sanity check that the probe does not disturb a normal component."""
    container = Container(_settings())
    await container.startup()
    vector: Vector = await container.embeddings.embed_query("x")
    await container.shutdown()

    assert len(vector) == 32
    assert Usage() == Usage()
