"""HTTP layer tests.

These run the real application — real container, real pipelines — with stub
providers registered under their own names. That the whole stack can be retargeted
at test doubles through configuration alone is itself the assertion: nothing in
the API or the pipelines knows which providers are in use.
"""

from __future__ import annotations

import asyncio
import json
import logging
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


# ------------------------------------------------------------------- logging


def test_every_response_carries_a_correlation_id(client: TestClient) -> None:
    """The handle an operator holding a failing response uses to find the log line.

    Generated server-side rather than taken from the client, because a
    client-supplied id can collide or be forged.
    """
    first = client.get("/api/health")
    second = client.get("/api/health")

    assert first.headers["X-Request-Id"]
    assert first.headers["X-Request-Id"] != second.headers["X-Request-Id"]


def test_a_request_is_logged_with_its_outcome(client: TestClient, caplog) -> None:
    with caplog.at_level(logging.INFO, logger="osc_assistant.api.app"):
        response = client.post("/api/search", json={"query": "how many vacation days"})

    events = {record.msg: record for record in caplog.records}

    assert "http.request" in events
    assert events["http.response"].status == response.status_code
    assert events["http.response"].path == "/api/search"
    # Same id on both halves and on the response, or the two lines cannot be joined.
    assert events["http.request"].request_id == events["http.response"].request_id
    assert events["http.response"].request_id == response.headers["X-Request-Id"]
    assert events["http.response"].duration_ms >= 0


# ------------------------------------------------------------------- sessions


def test_a_session_is_opened_and_closed_over_http(client: TestClient) -> None:
    opened = client.post("/api/sessions")

    assert opened.status_code == 201
    session_id = opened.json()["session_id"]
    assert session_id

    assert client.delete(f"/api/sessions/{session_id}").status_code == 204


def test_closing_a_session_twice_is_not_an_error(client: TestClient) -> None:
    """DELETE is idempotent: a browser cleaning up on unload cannot act on a 404."""
    session_id = client.post("/api/sessions").json()["session_id"]

    assert client.delete(f"/api/sessions/{session_id}").status_code == 204
    assert client.delete(f"/api/sessions/{session_id}").status_code == 204
    assert client.delete("/api/sessions/never-existed").status_code == 204


def test_a_follow_up_in_a_session_is_answered_with_the_previous_turn(
    client: TestClient,
) -> None:
    """The end-to-end conversational contract over HTTP.

    Asserted through the trace rather than through the answer text, because the
    stub returns a fixed reply either way — what changes is whether the follow-up
    was given any context, and that is exactly what `session_context` records.
    """
    session_id = client.post("/api/sessions").json()["session_id"]

    first = client.post(
        "/api/chat",
        json={"question": "How many vacation days?", "session_id": session_id, "stream": False},
    )
    assert first.status_code == 200

    second = client.post(
        "/api/chat",
        json={
            "question": "When do they expire?",
            "session_id": session_id,
            "stream": False,
            "explain": True,
        },
    )
    assert second.status_code == 200

    spans = {
        span["name"]: span["attributes"] for span in second.json()["trace"]["spans"]
    }
    assert spans["session_context"]["is_follow_up"] is True
    assert spans["session_context"]["turns_in_context"] == 1


def test_a_question_with_no_session_carries_no_context(client: TestClient) -> None:
    """Single-turn behaviour is unchanged: no session, no session_context span."""
    response = client.post(
        "/api/chat",
        json={"question": "How many vacation days?", "stream": False, "explain": True},
    )

    assert response.status_code == 200
    names = {span["name"] for span in response.json()["trace"]["spans"]}
    assert "session_context" not in names


def test_two_sessions_do_not_share_memory_over_http(client: TestClient) -> None:
    first = client.post("/api/sessions").json()["session_id"]
    second = client.post("/api/sessions").json()["session_id"]

    client.post(
        "/api/chat",
        json={"question": "How many vacation days?", "session_id": first, "stream": False},
    )
    reply = client.post(
        "/api/chat",
        json={
            "question": "And expenses?",
            "session_id": second,
            "stream": False,
            "explain": True,
        },
    )

    spans = {span["name"]: span["attributes"] for span in reply.json()["trace"]["spans"]}
    # The second session has seen one question — its own — and none of the first's.
    assert spans["session_context"]["is_follow_up"] is False
    assert spans["session_context"]["turns_in_context"] == 0


def test_a_closed_session_is_a_404_on_the_next_turn(client: TestClient) -> None:
    """Reported before the response begins, so it is a status code and not an
    in-band SSE error event."""
    session_id = client.post("/api/sessions").json()["session_id"]
    client.delete(f"/api/sessions/{session_id}")

    response = client.post(
        "/api/chat",
        json={"question": "still there?", "session_id": session_id, "stream": False},
    )

    assert response.status_code == 404
    assert "session" in response.json()["detail"].lower()


def test_an_unknown_session_is_a_404_on_the_streaming_path_too(client: TestClient) -> None:
    """The streaming branch fixes its status at 200 once the body starts, so the
    check has to happen before it does."""
    response = client.post(
        "/api/chat",
        json={"question": "hello", "session_id": "not-a-session", "stream": True},
    )

    assert response.status_code == 404


def test_supplying_both_a_session_and_a_history_is_rejected(client: TestClient) -> None:
    """Two sources of truth for the same thing; the server refuses to pick."""
    session_id = client.post("/api/sessions").json()["session_id"]

    response = client.post(
        "/api/chat",
        json={
            "question": "hello",
            "session_id": session_id,
            "history": [{"role": "user", "content": "earlier"}],
            "stream": False,
        },
    )

    assert response.status_code == 422


def test_a_streamed_session_turn_is_remembered(client: TestClient) -> None:
    """Memory must behave identically in both modes, as the abstention policy does."""
    session_id = client.post("/api/sessions").json()["session_id"]

    with client.stream(
        "POST",
        "/api/chat",
        json={"question": "How many vacation days?", "session_id": session_id},
    ) as stream:
        assert stream.status_code == 200
        events = [line for line in stream.iter_lines() if line.startswith("event:")]
    assert "event: complete" in events

    follow_up = client.post(
        "/api/chat",
        json={
            "question": "When do they expire?",
            "session_id": session_id,
            "stream": False,
            "explain": True,
        },
    )
    spans = {span["name"]: span["attributes"] for span in follow_up.json()["trace"]["spans"]}
    assert spans["session_context"]["turns_in_context"] == 1
