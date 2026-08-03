"""LangChain integration tests.

Three surfaces, three concerns:

* **Chunkers** — that a LangChain splitter behind the `Chunker` protocol keeps the
  properties ingestion depends on: stable ids, contiguous ordinals, and text the
  document actually contained.
* **The chat bridge** — that an arbitrary LangChain model is translated to and from
  OSC types correctly, including citations, usage and truncation.
* **The retriever** — that OSC is usable *from* LangChain, not only the reverse.

All of it runs against LangChain's own in-process fakes: no network, no credential.
"""

from __future__ import annotations

import pytest
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

from osc_assistant.chunking import (
    ChunkerOptions,
    LangChainChunkerOptions,
    LangChainRecursiveChunker,
    MarkdownChunker,
    RecursiveChunker,
)
from osc_assistant.errors import ConfigurationError, DimensionMismatchError, ProviderError
from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader
from osc_assistant.integrations.langchain import OSCRetriever
from osc_assistant.protocols import Chunker, EmbeddingModel
from osc_assistant.providers.embeddings.langchain_bridge import (
    LangChainEmbeddingModel,
    LangChainEmbeddingOptions,
)
from osc_assistant.providers.llm.langchain_bridge import (
    LangChainChatModel,
    LangChainChatOptions,
)
from osc_assistant.providers.reranking.noop import NoopReranker
from osc_assistant.registries import chunker_registry, embedding_registry, llm_registry
from osc_assistant.registry import ComponentConfig
from osc_assistant.retrieval import RetrievalPipeline
from osc_assistant.settings import RetrievalSettings
from osc_assistant.types import (
    ChatRequest,
    Document,
    Message,
    Role,
    SourceDocument,
    TextDelta,
)

MARKDOWN = """# Expense Policy

Claims must be submitted within thirty days of the expense being incurred.

## Approval thresholds

Any single item above 500 EUR needs line manager approval. Above 2,500 EUR the
finance director must approve it before the cost is incurred.

## Meals

The daily meal allowance while travelling is 65 EUR in tier-one cities.
"""


def _document(text: str = MARKDOWN) -> Document:
    return Document(
        id="doc-1", source_uri="file:///expenses.md", title="Expense Policy", text=text
    )


# ---------------------------------------------------------------------- chunkers


@pytest.mark.parametrize("strategy", ["langchain_recursive", "markdown"])
def test_langchain_chunkers_are_registered_and_satisfy_the_protocol(strategy: str) -> None:
    chunker = chunker_registry.create(
        ComponentConfig(provider=strategy, options={"chunk_size": 200, "chunk_overlap": 20})
    )
    assert isinstance(chunker, Chunker)
    assert chunker.split(_document())


@pytest.mark.parametrize(
    "chunker_class", [LangChainRecursiveChunker, MarkdownChunker]
)
def test_chunk_ids_are_stable_across_runs(chunker_class: type) -> None:
    """Ingestion skips unchanged documents by hash; drifting ids would re-index all."""
    chunker = chunker_class(LangChainChunkerOptions(chunk_size=200, chunk_overlap=20))
    document = _document()

    assert [chunk.id for chunk in chunker.split(document)] == [
        chunk.id for chunk in chunker.split(document)
    ]


@pytest.mark.parametrize("chunker_class", [LangChainRecursiveChunker, MarkdownChunker])
def test_ordinals_are_contiguous(chunker_class: type) -> None:
    chunker = chunker_class(LangChainChunkerOptions(chunk_size=150, chunk_overlap=20))
    chunks = chunker.split(_document())

    assert [chunk.ordinal for chunk in chunks] == list(range(len(chunks)))


@pytest.mark.parametrize("chunker_class", [LangChainRecursiveChunker, MarkdownChunker])
def test_chunking_preserves_document_content(chunker_class: type) -> None:
    """Chunk text is quoted back as citation evidence, so no character may be invented.

    Compared with whitespace collapsed, exactly as the built-in chunker's own test
    does: boundaries are trimmed by design, but visible characters must survive.
    """
    chunker = chunker_class(LangChainChunkerOptions(chunk_size=200, chunk_overlap=0))
    chunks = chunker.split(_document())

    rebuilt = "".join("".join(chunk.text.split()) for chunk in chunks)
    assert rebuilt == "".join(MARKDOWN.split())


def test_langchain_recursive_respects_the_size_budget() -> None:
    """The reason for adopting the library: OSC's own chunker can overshoot by the overlap."""
    chunker = LangChainRecursiveChunker(
        LangChainChunkerOptions(chunk_size=120, chunk_overlap=20)
    )
    chunks = chunker.split(_document("Paragraph about OSC policy. " * 60))

    assert len(chunks) > 1
    assert all(len(chunk.text) <= 120 for chunk in chunks)


def test_unbroken_text_is_still_split() -> None:
    """No separator exists in one long token; the hard fallback must catch it."""
    chunker = LangChainRecursiveChunker(
        LangChainChunkerOptions(chunk_size=100, chunk_overlap=0)
    )
    chunks = chunker.split(_document("x" * 500))

    assert len(chunks) >= 5
    assert all(len(chunk.text) <= 100 for chunk in chunks)


def test_markdown_chunker_records_the_heading_path() -> None:
    """A retrieval hit should say which section it came from without a second lookup."""
    chunker = MarkdownChunker(LangChainChunkerOptions(chunk_size=200, chunk_overlap=0))
    chunks = chunker.split(_document())

    sections = {chunk.metadata.get("section") for chunk in chunks}
    assert "Expense Policy > Approval thresholds" in sections


def test_markdown_chunker_keeps_headings_in_the_chunk_text() -> None:
    """Stripping the heading would make the stored text differ from the source."""
    chunker = MarkdownChunker(LangChainChunkerOptions(chunk_size=400, chunk_overlap=0))
    chunks = chunker.split(_document())

    assert any(chunk.text.lstrip().startswith("## Approval thresholds") for chunk in chunks)


def test_empty_document_produces_no_chunks() -> None:
    chunker = MarkdownChunker(LangChainChunkerOptions())
    assert chunker.split(_document("   \n\n  ")) == []


# -------------------------------------------------------------------- chat bridge


def _bridge(reply: str = "Claims are due within thirty days. [1]") -> LangChainChatModel:
    """A bridge over LangChain's own fake chat model — no network, no credential."""
    from langchain_core.messages import AIMessage

    model = LangChainChatModel.__new__(LangChainChatModel)
    model._model_name = "fake-model"
    model._options = LangChainChatOptions(class_path="x.Y", bind_max_tokens=False)
    model._client = GenericFakeChatModel(messages=iter([AIMessage(content=reply)]))
    return model


_SOURCES = [
    SourceDocument(
        chunk_id="chunk-1",
        document_id="doc-1",
        title="Expense Policy",
        source_uri="file:///expenses.md",
        text="Claims must be submitted within thirty days.",
    )
]


async def test_bridge_translates_a_completion_and_parses_citations() -> None:
    response = await _bridge().complete(
        ChatRequest(
            messages=[Message(role=Role.USER, content="When are claims due?")],
            system="Answer from the sources.",
            sources=_SOURCES,
        )
    )

    assert "thirty days" in response.text
    assert [citation.chunk_id for citation in response.citations] == ["chunk-1"]


async def test_bridge_streams_text_then_citations() -> None:
    """The streaming contract must match the OpenAI-compatible adapter's exactly."""
    events = [
        event
        async for event in _bridge().stream(
            ChatRequest(
                messages=[Message(role=Role.USER, content="When are claims due?")],
                sources=_SOURCES,
            )
        )
    ]

    text = "".join(event.text for event in events if isinstance(event, TextDelta))
    assert "thirty days" in text
    # Citations cannot be resolved until the full text is known: a marker can
    # straddle a chunk boundary.
    assert type(events[-1]).__name__ == "StreamEnd"
    assert any(type(event).__name__ == "CitationDelta" for event in events)


async def test_bridge_reports_an_empty_completion_rather_than_abstaining() -> None:
    """An empty answer looks identical to "the corpus has nothing" further down."""
    with pytest.raises(ProviderError, match="empty completion"):
        await _bridge(reply="").complete(
            ChatRequest(messages=[Message(role=Role.USER, content="x")])
        )


async def test_bridge_strips_a_leaked_reasoning_block() -> None:
    """A `[2]` written while thinking aloud must never become a citation."""
    response = await _bridge(
        reply="<think>I should cite [2] maybe</think>Claims are due in thirty days. [1]"
    ).complete(
        ChatRequest(messages=[Message(role=Role.USER, content="x")], sources=_SOURCES)
    )

    assert response.text.startswith("Claims are due")
    assert [citation.index for citation in response.citations] == [1]


def test_bridge_never_claims_native_citation_support() -> None:
    """Claiming it would assert a verification the bridge does not perform."""
    assert _bridge().supports_citations is False


def test_bridge_reports_a_missing_integration_package_actionably() -> None:
    from osc_assistant.errors import MissingDependencyError

    with pytest.raises(MissingDependencyError, match="langchain_nonexistent"):
        LangChainChatModel(
            "m", LangChainChatOptions(class_path="langchain_nonexistent.ChatThing")
        )


def test_bridge_rejects_a_class_path_without_a_module() -> None:
    with pytest.raises(ConfigurationError, match="dotted path"):
        LangChainChatModel("m", LangChainChatOptions(class_path="ChatThing"))


def test_the_bridges_are_registered_under_the_langchain_name() -> None:
    assert "langchain" in llm_registry.names()
    assert "langchain" in embedding_registry.names()


# --------------------------------------------------------------- embedding bridge


class _FakeEmbeddings(Embeddings):
    """A LangChain `Embeddings` with no dependencies.

    LangChain's own `DeterministicFakeEmbedding` needs numpy; the bridge is what is
    under test here, not the embedding maths, so a hash is enough.
    """

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return [float((hash(text) >> shift) % 7) for shift in range(16)]


def _embedding_bridge(dimensions: int = 16) -> LangChainEmbeddingModel:
    model = LangChainEmbeddingModel.__new__(LangChainEmbeddingModel)
    model._model_name = "fake-embedding"
    model._options = LangChainEmbeddingOptions(
        class_path="x.Y", dimensions=dimensions
    )
    model._client = _FakeEmbeddings()
    return model


async def test_embedding_bridge_satisfies_the_protocol() -> None:
    model = _embedding_bridge()
    assert isinstance(model, EmbeddingModel)

    vectors = await model.embed_documents(["one", "two"])
    assert len(vectors) == 2
    assert all(len(vector) == 16 for vector in vectors)
    assert len(await model.embed_query("one")) == 16


async def test_embedding_bridge_rejects_a_misdeclared_width() -> None:
    """A wrong `dimensions` would embed the corpus at one width and query at another."""
    with pytest.raises(DimensionMismatchError):
        await _embedding_bridge(dimensions=768).embed_query("one")


async def test_embedding_bridge_short_circuits_an_empty_batch() -> None:
    assert await _embedding_bridge().embed_documents([]) == []


# ------------------------------------------------------------ outbound retriever


async def test_osc_retrieval_is_usable_as_a_langchain_retriever(
    store, embeddings, documents
) -> None:
    """OSC's index, ranking and tuning, consumable from a LangChain application."""

    pipeline = IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions()), embeddings=embeddings, store=store
    )
    await pipeline.ingest(InMemoryLoader(documents).load())

    retriever = OSCRetriever(
        RetrievalPipeline(
            store=store,
            embeddings=embeddings,
            reranker=NoopReranker(),
            settings=RetrievalSettings(rewrite_queries=False, top_k=2),
        )
    )
    found = await retriever.ainvoke("vacation days")

    assert found
    # The score and the match source travel in metadata rather than being dropped:
    # a downstream chain still needs to build a real citation.
    assert found[0].metadata["source_uri"].endswith("vacation.md")
    assert "score" in found[0].metadata and "match_source" in found[0].metadata


def test_the_langchain_retriever_refuses_the_synchronous_path() -> None:
    """Silently spinning a second event loop would be worse than refusing."""

    retriever = OSCRetriever(
        RetrievalPipeline(
            store=None,  # type: ignore[arg-type] - never reached
            embeddings=None,  # type: ignore[arg-type]
            reranker=None,  # type: ignore[arg-type]
            settings=RetrievalSettings(),
        )
    )
    with pytest.raises(NotImplementedError, match="async-only"):
        retriever.invoke("anything")
