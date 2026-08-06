"""FastAPI application.

Thin by design: it validates input, calls one pipeline method, and encodes the
result. Every decision that matters — retrieval strategy, abstention, citation
policy — lives in the modules below it and is therefore testable without HTTP.

Authentication is not implemented here yet. The service exposes no write endpoint
(ingestion is a CLI operation) and must be deployed behind the corporate identity
proxy until OIDC lands.
"""

from __future__ import annotations

import time
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

from ..container import Container
from ..errors import AssistantError, ConfigurationError
from ..generation import AnswerComplete, RetrievalReady
from ..logging import configure_logging, get_logger
from ..observability import RECORDER, configure_observability
from ..protocols import StoreInspector
from ..settings import Settings, load_settings, log_resolved_settings
from ..types import CitationDelta, TextDelta
from .banner import describe_shutdown, describe_startup, startup_notes
from .schemas import (
    AnswerBody,
    ChatRequestBody,
    CitationBody,
    ComponentBody,
    ErrorBody,
    HealthBody,
    IndexStatusBody,
    RetrievedChunkBody,
    SearchRequestBody,
    SearchResponseBody,
    TraceListBody,
)
from .sse import SSE_HEADERS, SSE_MEDIA_TYPE, encode_event

log = get_logger(__name__)

router = APIRouter(prefix="/api")

# Separate router because it is mounted conditionally: traces contain question text
# and retrieved chunk ids, and nothing on this service is authenticated yet.
trace_router = APIRouter(prefix="/api/traces", tags=["observability"])

# A single static page, served from one route. The client is expected to be
# replaced by a richer one; keeping it to a file plus this route means that
# replacement touches nothing else in the service.
_INDEX = Path(__file__).parent / "static" / "index.html"


def create_app(settings: Settings | None = None, *, banner: bool = False) -> FastAPI:
    """Build the ASGI application.

    Accepting settings makes the app constructible in tests against an in-memory
    store with stub providers, with no environment manipulation.

    `banner` prints a human-readable summary to stderr on startup. Off by default
    because the common non-CLI caller is a test or an ASGI server embedding this
    app, and neither wants decoration on a stream; `osc-assistant serve` turns it
    on, which is the case where a person is watching.
    """
    settings = settings or load_settings()
    configure_logging(
        settings.log_level,
        settings.log_format,
        directory=settings.logging.directory,
        max_bytes=settings.logging.max_bytes,
        backup_count=settings.logging.backup_count,
        audit=settings.logging.audit,
        audit_max_bytes=settings.logging.audit_max_bytes,
        audit_backup_count=settings.logging.audit_backup_count,
        capture_payloads=settings.logging.capture_payloads,
    )
    configure_observability(
        enabled=settings.observability.enabled,
        capacity=settings.observability.trace_buffer_size,
        max_spans=settings.observability.max_spans_per_trace,
        log_traces=settings.observability.log_traces,
        log_spans=settings.logging.log_spans,
        capture_text=settings.observability.capture_text,
        persist=settings.observability.persist_traces,
        trace_dir=settings.observability.trace_dir,
        max_trace_bytes=settings.observability.max_trace_file_bytes,
    )
    log_resolved_settings(settings)
    container = Container(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        await container.startup()
        notes = await startup_notes(container, settings)
        # Logged as well as printed: a condition worth interrupting a developer
        # for is worth appearing in the log a collector keeps.
        log.info(
            "service.started",
            extra={
                "environment": settings.environment,
                "workspace_id": settings.workspace_id,
                "llm": f"{settings.llm.provider}/{settings.llm.model}",
                "embeddings": f"{settings.embeddings.provider}/{settings.embeddings.model}",
                "vector_store": settings.vector_store.provider,
                "traces_exposed": settings.traces_are_exposed,
                "notes": notes,
            },
        )
        if banner:
            await describe_startup(container, settings)
        try:
            yield
        finally:
            await container.shutdown()
            log.info("service.stopped")
            if banner:
                describe_shutdown()

    app = FastAPI(
        title="OSC Knowledge Assistant",
        version="0.1.0",
        summary="Grounded answers over OSC's internal documents.",
        lifespan=lifespan,
    )
    app.state.container = container

    @app.middleware("http")
    async def _log_requests(request: Request, call_next: Any) -> Any:
        """One record per HTTP request, with a correlation id.

        `request_id` is generated here rather than taken from the client, because a
        client-supplied id can collide or be forged. It is stamped on the response
        as `X-Request-Id` so an operator holding a failing response can find the
        exact line in the log, and it sits alongside `trace_id` — request id spans
        the whole HTTP exchange, trace id covers the pipeline work inside it.

        Streaming responses complete when the *headers* are sent, not when the body
        finishes, so `duration_ms` here is time-to-first-byte for `/api/chat` in
        streaming mode. The full generation time is on the trace.
        """
        request_id = uuid.uuid4().hex[:12]
        started = time.perf_counter()
        context = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else None,
        }
        log.info("http.request", extra=context)
        try:
            response = await call_next(request)
        except Exception as exc:
            log.exception(
                "http.request_failed",
                extra={
                    **context,
                    "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                    "error": f"{type(exc).__name__}: {exc}",
                },
            )
            raise
        response.headers["X-Request-Id"] = request_id
        log.info(
            "http.response",
            extra={
                **context,
                "status": response.status_code,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
            },
        )
        return response

    if settings.server.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.server.cors_origins,
            allow_methods=["GET", "POST"],
            allow_headers=["*"],
        )

    app.include_router(router)
    if settings.traces_are_exposed:
        # Registered conditionally rather than gated inside the handler, so a
        # non-development deployment does not merely refuse the request — the route
        # is absent from the app and from its OpenAPI schema entirely.
        app.include_router(trace_router)
    _register_ui(app)
    _register_error_handlers(app)
    return app


def _register_ui(app: FastAPI) -> None:
    """Serve the bundled chat client at the site root.

    Registered outside the `/api` router so the wire API and the page that happens
    to consume it stay independently versionable.
    """

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        if not _INDEX.is_file():  # pragma: no cover - only if the package is broken
            raise HTTPException(status_code=404, detail="UI is not installed.")
        return FileResponse(_INDEX, media_type="text/html")


def _container(request: Request) -> Container:
    container: Container = request.app.state.container
    return container


@router.get("/health", response_model=HealthBody)
async def health(request: Request) -> HealthBody:
    """Liveness plus the active component set.

    Returning the resolved configuration makes "which model answered this?" a
    question anyone can answer against a running deployment.
    """
    settings = _container(request).settings
    return HealthBody(
        status="ok",
        environment=settings.environment,
        workspace_id=settings.workspace_id,
        llm=ComponentBody(provider=settings.llm.provider, model=settings.llm.model),
        embeddings=ComponentBody(
            provider=settings.embeddings.provider, model=settings.embeddings.model
        ),
        vector_store=ComponentBody(
            provider=settings.vector_store.provider, model=settings.vector_store.model
        ),
        reranker=ComponentBody(
            provider=settings.reranker.provider, model=settings.reranker.model
        ),
        chunking_strategy=settings.chunking.strategy,
        retrieval_strategy=settings.retrieval.strategy,
    )


@router.get("/status", response_model=IndexStatusBody)
async def status(request: Request) -> IndexStatusBody:
    """What is currently indexed.

    Separate from `/health` because it queries the store: health must stay a cheap
    liveness probe that a load balancer can call every second, and counting several
    million chunks is not that.
    """
    store = _container(request).vector_store
    if not isinstance(store, StoreInspector):
        raise HTTPException(
            status_code=501,
            detail="The configured vector store offers no inspection interface.",
        )
    return IndexStatusBody.from_domain(await store.statistics())


@router.post("/search", response_model=SearchResponseBody)
async def search(request: Request, body: SearchRequestBody) -> SearchResponseBody:
    """Run retrieval only.

    Exposed as its own endpoint because retrieval quality is measurable and
    generation quality mostly is not: this is where the golden set is scored and
    where a bad answer is diagnosed.
    """
    result = await _container(request).retrieval.retrieve(body.query)
    return SearchResponseBody(
        query=result.query,
        original_query=result.original_query,
        results=[RetrievedChunkBody.from_domain(hit) for hit in result.chunks],
        candidates_considered=result.candidates_considered,
        duration_seconds=result.duration_seconds,
        trace_id=result.trace_id,
        trace=_trace_payload(result.trace_id) if body.explain else None,
    )


@trace_router.get("", response_model=TraceListBody)
async def list_traces(limit: int = 20) -> TraceListBody:
    """Recent execution traces, most recent first."""
    return TraceListBody(
        traces=[recorded.to_dict() for recorded in RECORDER.recent(limit=limit)]
    )


@trace_router.get("/{trace_id}")
async def get_trace(trace_id: str) -> dict[str, object]:
    """One execution trace in full, by id or unique prefix."""
    recorded = RECORDER.get(trace_id)
    if recorded is None:
        raise HTTPException(status_code=404, detail=f"No trace {trace_id!r} in the buffer.")
    return recorded.to_dict()


def _trace_payload(trace_id: str) -> dict[str, object] | None:
    """The trace for `trace_id`, if it is still in the buffer.

    Returned inline on request rather than requiring a second call, because the
    caller wanting an explanation is usually a developer at a terminal and a second
    round trip is a second chance to lose the id.
    """
    recorded = RECORDER.get(trace_id) if trace_id else None
    return recorded.to_dict() if recorded else None


# response_model is disabled because this endpoint returns either an SSE stream or
# a JSON body; the union cannot be expressed as a single response model. The
# non-streaming branch still returns a validated AnswerBody.
@router.post("/chat", response_model=None)
async def chat(request: Request, body: ChatRequestBody) -> StreamingResponse | AnswerBody:
    """Answer a question, streaming by default."""
    answerer = _container(request).answerer
    history = body.domain_history()

    if not body.stream:
        answer = await answerer.answer(body.question, history)
        return AnswerBody.from_domain(
            answer, trace=_trace_payload(answer.trace_id) if body.explain else None
        )

    async def events() -> AsyncIterator[str]:
        try:
            async for event in answerer.stream(body.question, history):
                match event:
                    case RetrievalReady():
                        yield encode_event(
                            "sources",
                            [
                                RetrievedChunkBody.from_domain(hit).model_dump()
                                for hit in event.result.chunks
                            ],
                        )
                    case TextDelta():
                        yield encode_event("delta", {"text": event.text})
                    case CitationDelta():
                        yield encode_event(
                            "citation", CitationBody.from_domain(event.citation).model_dump()
                        )
                    case AnswerComplete():
                        yield encode_event(
                            "complete", AnswerBody.from_domain(event.answer).model_dump()
                        )
        # Broad by intent. The response has already begun, so the status code is
        # fixed at 200 and a failure can only be reported in band. Catching only
        # `AssistantError` meant an unexpected exception — a bug, a provider SDK
        # raising something undocumented — closed the stream with no terminal
        # event, and a client that is told nothing waits forever. Every exit from
        # this generator now emits a terminal event.
        except Exception as exc:
            log.exception("chat.stream_failed")
            detail = (
                str(exc)
                if isinstance(exc, AssistantError)
                # An unexpected exception's message is not part of the API and may
                # carry internals, so clients get a stable message and the detail
                # goes to the log with its traceback.
                else "The assistant failed to complete this answer."
            )
            yield encode_event("error", {"error": type(exc).__name__, "detail": detail})

    return StreamingResponse(events(), media_type=SSE_MEDIA_TYPE, headers=SSE_HEADERS)


def _register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ConfigurationError)
    async def _configuration_error(_: Request, exc: ConfigurationError) -> JSONResponse:
        # A misconfiguration is an operator problem, not a client one: 500, and the
        # message is safe to surface because it never contains request data.
        log.error("api.configuration_error", extra={"detail": str(exc)})
        return JSONResponse(
            status_code=500,
            content=ErrorBody(error="configuration_error", detail=str(exc)).model_dump(),
        )

    @app.exception_handler(AssistantError)
    async def _assistant_error(_: Request, exc: AssistantError) -> JSONResponse:
        log.exception("api.request_failed")
        return JSONResponse(
            status_code=502,
            content=ErrorBody(error=type(exc).__name__, detail=str(exc)).model_dump(),
        )
