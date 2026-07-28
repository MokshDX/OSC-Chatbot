"""FastAPI application.

Thin by design: it validates input, calls one pipeline method, and encodes the
result. Every decision that matters — retrieval strategy, abstention, citation
policy — lives in the modules below it and is therefore testable without HTTP.

Authentication is not implemented here yet. The service exposes no write endpoint
(ingestion is a CLI operation) and must be deployed behind the corporate identity
proxy until OIDC lands.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from ..container import Container
from ..errors import AssistantError, ConfigurationError
from ..generation import AnswerComplete, RetrievalReady
from ..logging import configure_logging, get_logger
from ..settings import Settings, load_settings
from ..types import CitationDelta, TextDelta
from .schemas import (
    AnswerBody,
    ChatRequestBody,
    CitationBody,
    ComponentBody,
    ErrorBody,
    HealthBody,
    RetrievedChunkBody,
    SearchRequestBody,
    SearchResponseBody,
)
from .sse import SSE_HEADERS, SSE_MEDIA_TYPE, encode_event

log = get_logger(__name__)

router = APIRouter(prefix="/api")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the ASGI application.

    Accepting settings makes the app constructible in tests against an in-memory
    store with stub providers, with no environment manipulation.
    """
    settings = settings or load_settings()
    configure_logging(settings.log_level, settings.log_format)
    container = Container(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        await container.startup()
        log.info("service.started", extra={"environment": settings.environment})
        try:
            yield
        finally:
            await container.shutdown()
            log.info("service.stopped")

    app = FastAPI(
        title="OSC Knowledge Assistant",
        version="0.1.0",
        summary="Grounded answers over OSC's internal documents.",
        lifespan=lifespan,
    )
    app.state.container = container

    if settings.server.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.server.cors_origins,
            allow_methods=["GET", "POST"],
            allow_headers=["*"],
        )

    app.include_router(router)
    _register_error_handlers(app)
    return app


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
    )


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
        return AnswerBody.from_domain(answer)

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
        except AssistantError as exc:
            # The response has already begun, so the status code is fixed at 200.
            # Failures are therefore reported in-band as a terminal error event.
            log.exception("chat.stream_failed")
            yield encode_event("error", {"error": type(exc).__name__, "detail": str(exc)})

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
