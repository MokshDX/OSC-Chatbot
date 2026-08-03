"""Exposing OSC to LangChain, rather than the other way round.

Every other LangChain touchpoint in this repository brings LangChain *in* — a
splitter, a chat model, an embedder — behind an OSC protocol. This module points
the other way: it presents OSC's retrieval pipeline as a LangChain `BaseRetriever`,
so an application built on LangChain or LangGraph can use OSC's corpus, hybrid
search, reranking and workspace scoping as a component.

That direction matters more than it first appears. OSC's value is the *indexed
corpus and how it is retrieved*, not the answer-generation loop, and teams inside
the company will build agents on frameworks OSC does not control. Making the
retriever consumable means they use the same index, the same ranking and the same
tuning rather than standing up a parallel one that drifts.

    from osc_assistant.container import Container
    from osc_assistant.integrations.langchain import OSCRetriever
    from osc_assistant.settings import load_settings

    container = Container(load_settings())
    await container.startup()
    retriever = OSCRetriever(container.retrieval)
    documents = await retriever.ainvoke("What is the expense limit?")

Nothing else in the codebase imports this module: it is an outbound adapter, and
the dependency points from LangChain's world into ours and never back.

Retrieved chunks arrive as LangChain `Document`s carrying the full OSC metadata —
chunk id, document id, score, match source, source URI — so a downstream chain can
still build a citation that points at the real document.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict

from ..retrieval import RetrievalPipeline
from ..types import ScoredChunk

if TYPE_CHECKING:  # pragma: no cover - import-time typing only
    from langchain_core.callbacks import (
        AsyncCallbackManagerForRetrieverRun,
        CallbackManagerForRetrieverRun,
    )
    from langchain_core.documents import Document as LangChainDocument


def to_langchain_document(scored: ScoredChunk) -> LangChainDocument:
    """Translate one retrieval hit into a LangChain document.

    The score and the match source travel in metadata rather than being dropped:
    "which stage found this?" is the first question when a hybrid result looks
    wrong, and LangChain has nowhere else to put it.
    """
    from langchain_core.documents import Document as LangChainDocument

    return LangChainDocument(
        id=scored.chunk.id,
        page_content=scored.chunk.text,
        metadata={
            **dict(scored.chunk.metadata),
            "chunk_id": scored.chunk.id,
            "document_id": scored.chunk.document_id,
            "ordinal": scored.chunk.ordinal,
            "title": scored.chunk.title,
            "source_uri": scored.chunk.source_uri,
            "score": scored.score,
            "match_source": scored.source.value,
        },
    )


def OSCRetriever(pipeline: RetrievalPipeline, **kwargs: Any) -> Any:  # noqa: N802
    """Build a LangChain `BaseRetriever` over an OSC retrieval pipeline.

    A factory function rather than a module-level class, because subclassing
    `BaseRetriever` requires importing `langchain_core` at module import time.
    Every other LangChain integration here is optional at runtime, and this one has
    no reason to be the exception that makes the package unimportable without it.
    """
    from langchain_core.retrievers import BaseRetriever

    class _OSCRetriever(BaseRetriever):
        """OSC's hybrid retrieval pipeline as a LangChain retriever."""

        osc_pipeline: RetrievalPipeline

        # RetrievalPipeline is a plain class, not a pydantic model, and
        # BaseRetriever is one — so it has to be told the field is allowed.
        model_config = ConfigDict(arbitrary_types_allowed=True)

        async def _aget_relevant_documents(
            self, query: str, *, run_manager: AsyncCallbackManagerForRetrieverRun
        ) -> list[LangChainDocument]:
            result = await self.osc_pipeline.retrieve(query)
            return [to_langchain_document(hit) for hit in result.chunks]

        def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
        ) -> list[LangChainDocument]:
            # The whole pipeline is async — the store, the embedder and the reranker
            # are all awaited — and there is no correct way to run it from a thread
            # that may already own a running loop. Refusing is better than the
            # deadlock or the silent second event loop the alternatives produce.
            raise NotImplementedError(
                "OSCRetriever is async-only. Use `ainvoke` / `aget_relevant_documents`."
            )

    return _OSCRetriever(osc_pipeline=pipeline, **kwargs)
