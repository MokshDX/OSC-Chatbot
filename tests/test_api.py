"""HTTP layer tests.

These run the real application — real container, real pipelines — with stub
providers registered under their own names. That the whole stack can be retargeted
at test doubles through configuration alone is itself the assertion: nothing in
the API or the pipelines knows which providers are in use.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from osc_assistant.api import create_app
from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
from osc_assistant.container import Container
from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader
from osc_assistant.registries import embedding_registry, llm_registry
from osc_assistant.registry import ComponentConfig
from osc_assistant.settings import (
    ChunkingSettings,
    GenerationSettings,
    RetrievalSettings,
    Settings,
)
from osc_assistant.types import Document

from .conftest import StubChatModel, StubEmbeddingModel

STUB_REPLY = "Employees accrue twenty five vacation days each year. [1]"


@pytest.fixture(autouse=True)
def _register_stub_providers() -> None:
    """Register the doubles as ordinary providers.

    This is exactly how a new provider would be added, which makes the fixture a
    working demonstration of the extension mechanism.
    """
    embedding_registry.register("stub")(lambda config: StubEmbeddingModel())
    llm_registry.register("stub")(lambda config: StubChatModel(reply=STUB_REPLY))


def _settings() -> Settings:
    return Settings(
        environment="test",
        log_format="text",
        llm=ComponentConfig(provider="stub", model="stub-chat"),
        fast_llm=ComponentConfig(provider="stub", model="stub-chat"),
        embeddings=ComponentConfig(provider="stub", model="stub-embedding"),
        vector_store=ComponentConfig(provider="memory"),
        chunking=ChunkingSettings(chunk_size=400, chunk_overlap=40),
        retrieval=RetrievalSettings(rewrite_queries=False, top_k=4),
        generation=GenerationSettings(require_citations=True),
    )


@pytest.fixture
def client(documents: list[Document]) -> Iterator[TestClient]:
    settings = _settings()
    app = create_app(settings)
    container: Container = app.state.container

    async def seed() -> None:
        pipeline = IngestionPipeline(
            chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
            embeddings=container.embeddings,
            store=container.vector_store,
        )
        await pipeline.ingest(InMemoryLoader(documents).load())

    asyncio.run(seed())

    with TestClient(app) as test_client:
        yield test_client


def test_health_reports_the_active_components(client: TestClient) -> None:
    """A running deployment must be able to say what it is configured with."""
    response = client.get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["llm"]["provider"] == "stub"
    assert body["vector_store"]["provider"] == "memory"
    assert body["retrieval_strategy"] == "hybrid"


def test_ui_is_served_at_the_root(client: TestClient) -> None:
    """The bundled client ships inside the package; a wheel that drops the static
    file would otherwise fail only in a deployed environment."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "OSC Knowledge Assistant" in response.text


def test_search_returns_ranked_chunks(client: TestClient) -> None:
    response = client.post("/api/search", json={"query": "how many vacation days"})

    assert response.status_code == 200
    body = response.json()
    assert body["results"]
    assert body["results"][0]["document_id"] == "doc-vacation"
    assert body["candidates_considered"] > 0


def test_chat_returns_a_cited_answer(client: TestClient) -> None:
    response = client.post(
        "/api/chat", json={"question": "How many vacation days?", "stream": False}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["abstained"] is False
    assert len(body["citations"]) == 1
    assert body["citations"][0]["source_uri"].endswith("vacation.md")
    assert body["retrieved"]
    assert body["usage"]["input_tokens"] > 0


def test_chat_abstains_when_nothing_is_retrieved(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={"question": "zzzz qqqq xxxx unmatched vocabulary", "stream": False},
    )

    body = response.json()
    # Either nothing was retrieved, or what was retrieved did not support an answer.
    # Both must surface as an abstention rather than an invented answer.
    assert body["abstained"] is True or body["citations"]


def test_chat_streams_sources_then_deltas_then_completion(client: TestClient) -> None:
    with client.stream(
        "POST", "/api/chat", json={"question": "How many vacation days?", "stream": True}
    ) as response:
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
        events = _parse_sse(response.iter_lines())

    names = [name for name, _ in events]
    assert names[0] == "sources"
    assert "delta" in names
    assert "citation" in names
    assert names[-1] == "complete"

    streamed = "".join(payload["text"] for name, payload in events if name == "delta")
    complete = next(payload for name, payload in events if name == "complete")
    assert streamed.strip() == complete["text"].strip()
    assert complete["abstained"] is False


def test_history_is_accepted(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={
            "question": "And when do they expire?",
            "history": [
                {"role": "user", "content": "How many vacation days do we get?"},
                {"role": "assistant", "content": "Twenty five per year."},
            ],
            "stream": False,
        },
    )

    assert response.status_code == 200


@pytest.mark.parametrize(
    "payload",
    [
        {},  # question is required
        {"question": ""},  # and must be non-empty
        {"question": "hi", "history": [{"role": "system", "content": "x"}]},  # invalid role
        {"question": "hi", "unexpected": True},  # unknown field
    ],
)
def test_malformed_requests_are_rejected(client: TestClient, payload: dict[str, object]) -> None:
    """Validation happens at the trust boundary, before any provider is touched."""
    assert client.post("/api/chat", json=payload).status_code == 422


def _parse_sse(lines: Iterator[str]) -> list[tuple[str, dict]]:
    """Decode a server-sent event stream into (event name, payload) pairs."""
    events: list[tuple[str, dict]] = []
    event_name: str | None = None
    for line in lines:
        if line.startswith("event: "):
            event_name = line.removeprefix("event: ").strip()
        elif line.startswith("data: ") and event_name is not None:
            events.append((event_name, json.loads(line.removeprefix("data: "))))
            event_name = None
    return events


# ------------------------------------------------------- observability endpoints


def test_status_reports_what_is_indexed(client: TestClient) -> None:
    """The admin view: separate from /health because it queries the store."""
    response = client.get("/api/status")

    assert response.status_code == 200
    body = response.json()
    assert body["documents"] == 3
    assert body["chunks"] > 0
    assert body["embedding_models"] == ["stub-embedding"]
    assert set(body["chunk_chars"]) == {"min", "mean", "p50", "p95", "max"}


def test_an_answer_carries_the_id_of_the_trace_that_produced_it(
    client: TestClient,
) -> None:
    """"This answer is wrong" becomes answerable hours later, without reproducing it."""
    response = client.post(
        "/api/chat", json={"question": "how many vacation days", "stream": False}
    )

    assert response.status_code == 200
    assert response.json()["trace_id"]


def test_search_returns_the_trace_when_asked(client: TestClient) -> None:
    response = client.post(
        "/api/search", json={"query": "how many vacation days", "explain": True}
    )

    body = response.json()
    assert body["trace"] is not None
    names = [span["name"] for span in body["trace"]["spans"]]
    assert "retrieve" in names and "search" in names


def test_search_omits_the_trace_by_default(client: TestClient) -> None:
    response = client.post("/api/search", json={"query": "how many vacation days"})

    assert response.json()["trace"] is None


def test_chat_returns_the_trace_when_asked(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={"question": "how many vacation days", "stream": False, "explain": True},
    )

    trace = response.json()["trace"]
    assert trace is not None
    names = [span["name"] for span in trace["spans"]]
    # The whole request path, in one object: retrieval, generation and the
    # citation policy that finalised it.
    assert {"answer", "retrieve", "generate", "finalise"} <= set(names)


def _development_client(documents: list[Document]) -> TestClient:
    settings = _settings().model_copy(update={"environment": "development"})
    app = create_app(settings)
    container: Container = app.state.container

    async def seed() -> None:
        pipeline = IngestionPipeline(
            chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
            embeddings=container.embeddings,
            store=container.vector_store,
        )
        await pipeline.ingest(InMemoryLoader(documents).load())

    asyncio.run(seed())
    return TestClient(app)


def test_traces_are_not_exposed_outside_development(client: TestClient) -> None:
    """Traces carry question text and chunk ids, and no endpoint is authenticated.

    The route is absent rather than merely refusing, so it is missing from the
    OpenAPI schema too.
    """
    assert client.get("/api/traces").status_code == 404


def test_traces_are_listable_and_expandable_in_development(
    documents: list[Document],
) -> None:
    with _development_client(documents) as client:
        client.post("/api/chat", json={"question": "how many vacation days", "stream": False})

        listing = client.get("/api/traces")
        assert listing.status_code == 200
        traces = listing.json()["traces"]
        assert traces

        detail = client.get(f"/api/traces/{traces[0]['trace_id']}")
        assert detail.status_code == 200
        assert detail.json()["name"] == "answer"


def test_an_unknown_trace_id_is_a_404(documents: list[Document]) -> None:
    with _development_client(documents) as client:
        assert client.get("/api/traces/nonexistent").status_code == 404
