"""Integration tests for the PostgreSQL store.

Skipped unless `OSC_TEST_DSN` points at a Postgres instance with pgvector:

    docker compose up -d
    OSC_TEST_DSN=postgresql://postgres:postgres@localhost:5432/osc_assistant pytest

The rest of the suite runs against the in-memory store, which cannot exercise the
migration runner, the generated tsvector column or the SQL rank-fusion query.
Those are the parts of this codebase that only a real database can verify, so they
get their own tests rather than being taken on trust.

The schema is shared; isolation comes from giving each test a unique
`workspace_id` and deleting its documents afterwards. That makes the suite safe to
run repeatedly, and repeatedly against the same database, while also exercising
the partition key that every query is scoped by.
"""

from __future__ import annotations

import os
import uuid
from collections.abc import AsyncIterator

import pytest

from osc_assistant.providers.vectorstores.pgvector import PgVectorOptions, PgVectorStore
from osc_assistant.types import Chunk, Document, EmbeddedChunk, MatchSource

from .conftest import EMBEDDING_DIMENSIONS, StubEmbeddingModel

DSN = os.environ.get("OSC_TEST_DSN")

# The `chunks` table fixes its vector width at migration time, so this suite has to
# use whatever width the target database was created with. Against a dedicated test
# database that is the narrow stub width, which keeps the tests fast. Against a
# database an application already migrated — the common case when Postgres is a
# shared local instance — set OSC_TEST_DIMENSIONS to the deployed embedding model's
# width, or the store will correctly refuse to start on a dimension mismatch.
DIMENSIONS = int(os.environ.get("OSC_TEST_DIMENSIONS", EMBEDDING_DIMENSIONS))

pytestmark = pytest.mark.skipif(
    not DSN, reason="Set OSC_TEST_DSN to run the PostgreSQL integration tests."
)


@pytest.fixture
def embeddings() -> StubEmbeddingModel:
    """Overrides the shared fixture so vectors match the target table's width."""
    return StubEmbeddingModel(DIMENSIONS)

CORPUS: list[tuple[str, str]] = [
    ("vacation", "OSC employees accrue twenty five vacation days each calendar year."),
    ("expenses", "Expense claims must be submitted within thirty days with receipts."),
    ("onboarding", "New joiners receive a laptop on their first day at OSC."),
]


@pytest.fixture
async def store() -> AsyncIterator[PgVectorStore]:
    """A store scoped to a unique workspace, cleaned up afterwards.

    The workspace key is what isolates concurrent runs, which is a useful check in
    its own right: it proves the partition key is actually honoured on every query.
    """
    workspace = f"test-{uuid.uuid4().hex[:8]}"
    instance = PgVectorStore(
        PgVectorOptions(
            dsn=DSN or "",
            workspace_id=workspace,
            dimensions=DIMENSIONS,
            embedding_model="stub-embedding",
        )
    )
    await instance.setup()
    try:
        yield instance
    finally:
        for document_id, _ in CORPUS:
            await instance.delete_document(document_id)
        await instance.close()


@pytest.fixture
async def populated(store: PgVectorStore, embeddings: StubEmbeddingModel) -> PgVectorStore:
    for document_id, text in CORPUS:
        document = Document(
            id=document_id,
            source_uri=f"file:///handbook/{document_id}.md",
            title=document_id.title(),
            text=text,
        )
        chunk = Chunk(
            id=f"{document_id}:0",
            document_id=document_id,
            ordinal=0,
            text=text,
            title=document.title,
            source_uri=document.source_uri,
            metadata={"section": "handbook"},
        )
        vector = (await embeddings.embed_documents([text]))[0]
        await store.replace_document(
            document,
            [EmbeddedChunk(chunk=chunk, vector=vector, embedding_model="stub-embedding")],
        )
    return store


async def test_migrations_are_applied_and_idempotent(store: PgVectorStore) -> None:
    """setup() ran the migrations; running them again must be a no-op."""
    await store.setup()
    assert store.dimensions == DIMENSIONS


async def test_vector_search_finds_the_nearest_chunk(
    populated: PgVectorStore, embeddings: StubEmbeddingModel
) -> None:
    query = await embeddings.embed_query("how many vacation days do we accrue")

    hits = await populated.search_vector(query, limit=3)

    assert hits
    assert hits[0].chunk.document_id == "vacation"
    assert hits[0].source is MatchSource.VECTOR


async def test_keyword_search_uses_the_generated_tsvector(populated: PgVectorStore) -> None:
    hits = await populated.search_keyword("laptop first day", limit=3)

    assert hits
    assert hits[0].chunk.document_id == "onboarding"


async def test_hybrid_search_fuses_both_rankings(
    populated: PgVectorStore, embeddings: StubEmbeddingModel
) -> None:
    query = await embeddings.embed_query("expense receipts submitted")

    hits = await populated.search_hybrid(query, "expense receipts submitted", limit=3)

    assert hits
    assert hits[0].chunk.document_id == "expenses"
    assert all(hit.source is MatchSource.HYBRID for hit in hits)


async def test_metadata_round_trips_as_json(
    populated: PgVectorStore, embeddings: StubEmbeddingModel
) -> None:
    query = await embeddings.embed_query("laptop")

    hits = await populated.search_vector(query, limit=1)

    assert hits[0].chunk.metadata == {"section": "handbook"}


async def test_replace_document_supersedes_the_old_chunks(
    populated: PgVectorStore, embeddings: StubEmbeddingModel
) -> None:
    """Chunk ids incorporate content, so an edit yields new ids. Without the
    delete inside the transaction the superseded chunks stay retrievable."""
    replacement = "OSC employees accrue thirty vacation days each calendar year."
    document = Document(
        id="vacation",
        source_uri="file:///handbook/vacation.md",
        title="Vacation",
        text=replacement,
    )
    chunk = Chunk(
        id="vacation:0-edited",
        document_id="vacation",
        ordinal=0,
        text=replacement,
        title="Vacation",
        source_uri="file:///handbook/vacation.md",
    )
    vector = (await embeddings.embed_documents([replacement]))[0]

    await populated.replace_document(
        document,
        [EmbeddedChunk(chunk=chunk, vector=vector, embedding_model="stub-embedding")],
    )

    hits = await populated.search_keyword("thirty vacation days", limit=5)
    assert any("thirty" in hit.chunk.text for hit in hits)
    assert not any("twenty five" in hit.chunk.text for hit in hits)


async def test_deleting_a_document_cascades_to_its_chunks(
    populated: PgVectorStore, embeddings: StubEmbeddingModel
) -> None:
    await populated.delete_document("vacation")

    assert "vacation" not in await populated.document_ids()
    assert not await populated.search_keyword("vacation days accrue", limit=5)


async def test_failed_replace_leaves_no_hash_without_chunks(
    populated: PgVectorStore, embeddings: StubEmbeddingModel
) -> None:
    """The skip check reads a recorded hash as "chunks are present". A partial
    write would make the document permanently invisible, so the whole replacement
    must roll back together."""
    document = Document(
        id="rollback", source_uri="file:///handbook/rollback.md", title="R", text="body"
    )
    vector = (await embeddings.embed_documents(["body"]))[0]
    good = Chunk(
        id="rollback:0", document_id="rollback", ordinal=0,
        text="body", title="R", source_uri="file:///handbook/rollback.md",
    )
    bad = Chunk(
        id="rollback:1", document_id="rollback", ordinal=1,
        text="body", title="R", source_uri="file:///handbook/rollback.md",
    )
    # The second chunk carries a wrong-width vector, which pgvector rejects at
    # insert time — a mid-batch failure after the document row is already written.
    batch = [
        EmbeddedChunk(chunk=good, vector=vector, embedding_model="stub-embedding"),
        EmbeddedChunk(chunk=bad, vector=[0.1, 0.2], embedding_model="stub-embedding"),
    ]

    with pytest.raises(Exception):  # noqa: B017 - asyncpg raises a driver-specific error
        await populated.replace_document(document, batch)

    assert "rollback" not in await populated.list_document_hashes()
    assert not await populated.search_keyword("body", limit=5)


async def test_document_hashes_support_incremental_sync(populated: PgVectorStore) -> None:
    hashes = await populated.list_document_hashes()

    assert set(hashes) == {document_id for document_id, _ in CORPUS}
    assert all(len(value) == 64 for value in hashes.values())


async def test_workspace_isolates_queries(
    populated: PgVectorStore, embeddings: StubEmbeddingModel
) -> None:
    """Content in one workspace must be invisible to another."""
    other = PgVectorStore(
        PgVectorOptions(
            dsn=DSN or "",
            workspace_id=f"test-{uuid.uuid4().hex[:8]}",
            dimensions=DIMENSIONS,
            embedding_model="stub-embedding",
        )
    )
    await other.setup()
    try:
        query = await embeddings.embed_query("vacation days")
        assert await other.search_vector(query, limit=5) == []
    finally:
        await other.close()


async def test_search_ignores_other_embedding_models(
    populated: PgVectorStore, embeddings: StubEmbeddingModel
) -> None:
    """Vectors from a different model must never be compared against these."""
    mismatched = PgVectorStore(
        PgVectorOptions(
            dsn=DSN or "",
            workspace_id=populated.workspace_id,
            dimensions=DIMENSIONS,
            embedding_model="some-other-model",
        )
    )
    await mismatched.setup()
    try:
        query = await embeddings.embed_query("vacation days")
        assert await mismatched.search_vector(query, limit=5) == []
    finally:
        await mismatched.close()
