"""Composition root.

The only module that knows both which providers exist and how they fit together.
Everything else depends on protocols, which is what keeps providers swappable.

Components are built lazily so that a command uses only what it needs: `ingest`
never constructs a chat model, and therefore never requires an LLM credential.

No dependency-injection framework. The object graph is a dozen nodes and is
written out below in full — a container library would add indirection without
removing a single line of the wiring it would replace.
"""

from __future__ import annotations

import inspect
from functools import cached_property
from typing import Self

from . import providers as _providers  # noqa: F401 - registers built-in providers
from .chunking import RecursiveChunker  # noqa: F401 - registers built-in chunkers
from .generation import Answerer
from .ingestion import IngestionPipeline
from .logging import get_logger
from .protocols import ChatModel, Chunker, EmbeddingModel, Reranker, VectorStore
from .registries import (
    chunker_registry,
    embedding_registry,
    llm_registry,
    reranker_registry,
    vector_store_registry,
)
from .registry import ComponentConfig
from .retrieval import QueryRewriter, RetrievalPipeline
from .settings import Settings

log = get_logger(__name__)


class Container:
    """Builds and owns the application's components."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    # ------------------------------------------------------------- components

    @cached_property
    def embeddings(self) -> EmbeddingModel:
        model = embedding_registry.create(self.settings.embeddings)
        log.info(
            "component.built",
            extra={
                "component": "embeddings",
                "provider": self.settings.embeddings.provider,
                "model": model.model_id,
                "dimensions": model.dimensions,
            },
        )
        return model

    @cached_property
    def vector_store(self) -> VectorStore:
        """Build the store, injecting values it cannot know on its own.

        Vector width, the active embedding model id, the DSN and the workspace all
        live outside the store's own configuration block, so they are merged in
        here. This keeps a profile short — selecting a store is one line — and keeps
        the store from reaching into global settings itself.
        """
        config = self.settings.vector_store
        options = {
            "dsn": self.settings.database.dsn,
            "workspace_id": self.settings.workspace_id,
            "min_pool_size": self.settings.database.min_pool_size,
            "max_pool_size": self.settings.database.max_pool_size,
            "rrf_k": self.settings.retrieval.rrf_k,
            **config.options,
            # Derived from the embedding model, so never operator-supplied.
            "dimensions": self.embeddings.dimensions,
            "embedding_model": self.embeddings.model_id,
        }
        store = vector_store_registry.create(
            ComponentConfig(provider=config.provider, model=config.model, options=options)
        )
        log.info(
            "component.built",
            extra={"component": "vector_store", "provider": config.provider},
        )
        return store

    @cached_property
    def chunker(self) -> Chunker:
        chunking = self.settings.chunking
        return chunker_registry.create(
            ComponentConfig(
                provider=chunking.strategy,
                options={
                    "chunk_size": chunking.chunk_size,
                    "chunk_overlap": chunking.chunk_overlap,
                },
            )
        )

    @cached_property
    def llm(self) -> ChatModel:
        model = llm_registry.create(self.settings.llm)
        log.info(
            "component.built",
            extra={
                "component": "llm",
                "provider": self.settings.llm.provider,
                "model": model.model_id,
                "native_citations": model.supports_citations,
            },
        )
        return model

    @cached_property
    def fast_llm(self) -> ChatModel:
        """A cheaper model for auxiliary steps such as query rewriting."""
        return llm_registry.create(self.settings.fast_llm)

    @cached_property
    def reranker(self) -> Reranker:
        return reranker_registry.create(self.settings.reranker)

    # -------------------------------------------------------------- pipelines

    @cached_property
    def retrieval(self) -> RetrievalPipeline:
        rewriter = (
            QueryRewriter(self.fast_llm) if self.settings.retrieval.rewrite_queries else None
        )
        return RetrievalPipeline(
            store=self.vector_store,
            embeddings=self.embeddings,
            reranker=self.reranker,
            settings=self.settings.retrieval,
            rewriter=rewriter,
        )

    @cached_property
    def answerer(self) -> Answerer:
        return Answerer(
            retrieval=self.retrieval,
            model=self.llm,
            settings=self.settings.generation,
        )

    @cached_property
    def ingestion(self) -> IngestionPipeline:
        return IngestionPipeline(
            chunker=self.chunker,
            embeddings=self.embeddings,
            store=self.vector_store,
        )

    # -------------------------------------------------------------- lifecycle

    async def startup(self) -> None:
        await self.vector_store.setup()

    async def shutdown(self) -> None:
        """Release everything that was actually built.

        Only components whose `cached_property` was touched are torn down —
        `cached_property` stores into the instance `__dict__`, so its presence there
        is exactly the record of what was constructed. That matters because
        `ingest` never builds a chat model, and shutting one down would construct
        the very thing the lazy graph exists to avoid, then fail for want of a
        credential.

        Previously this closed the vector store and nothing else, so the HTTP
        clients inside the Voyage, OpenAI and Gemini adapters were left open:
        harmless at process exit, a leak in tests and in any future in-process
        reload.
        """
        for name in ("vector_store", "llm", "fast_llm", "embeddings", "reranker"):
            component = self.__dict__.get(name)
            if component is not None:
                await _release(component)


    async def __aenter__(self) -> Self:
        await self.startup()
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.shutdown()


async def _release(component: object) -> None:
    """Close a component if it offers a way to be closed.

    Probed rather than required by the protocols: most providers hold no resource,
    and adding a mandatory `close()` to all five seams to serve the three that do
    would make every adapter and every test double carry an empty method.
    """
    for method_name in ("aclose", "close"):
        method = getattr(component, method_name, None)
        if method is None:
            continue
        try:
            result = method()
            if inspect.isawaitable(result):
                await result
        # Broad by intent: shutdown runs on the failure path too, and a provider
        # that cannot close cleanly must not mask the error that caused shutdown.
        except Exception as exc:
            log.warning(
                "component.close_failed",
                extra={"component": type(component).__name__, "error": str(exc)},
            )
        return
