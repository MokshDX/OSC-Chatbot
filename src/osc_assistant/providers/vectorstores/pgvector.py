"""PostgreSQL + pgvector store: the production default.

One datastore holds chunk text, embeddings, lexical index and document metadata,
so a chunk and its vector are always consistent, there is one backup to take, and
hybrid retrieval is a single round trip instead of a fan-out across two systems.

Fusion is performed in SQL using the same Reciprocal Rank Fusion formula as
`fusion.reciprocal_rank_fusion`, so the in-memory store used by tests and the
production store rank identically.

Raw SQL over asyncpg rather than an ORM: this module issues eight statements, one
of which is a hand-tuned ranking query that no ORM would express well.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ...errors import ConfigurationError, VectorStoreError
from ...logging import get_logger
from ...protocols import VectorStore
from ...registries import vector_store_registry
from ...registry import ComponentConfig
from ...types import (
    Chunk,
    Document,
    EmbeddedChunk,
    MatchSource,
    ScoredChunk,
    Vector,
)

log = get_logger(__name__)

DIMENSION_PLACEHOLDER = "{{EMBEDDING_DIMENSIONS}}"

_SEARCH_VECTOR_SQL = """
SELECT id, document_id, ordinal, content, title, source_uri, metadata,
       1 - (embedding <=> $1::vector) AS score
FROM chunks
WHERE workspace_id = $2 AND embedding_model = $3
ORDER BY embedding <=> $1::vector
LIMIT $4
"""

_SEARCH_KEYWORD_SQL = """
SELECT c.id, c.document_id, c.ordinal, c.content, c.title, c.source_uri, c.metadata,
       ts_rank_cd(c.tsv, q.query) AS score
FROM chunks c, websearch_to_tsquery('english', $1) AS q(query)
WHERE c.workspace_id = $2 AND c.embedding_model = $3 AND c.tsv @@ q.query
ORDER BY score DESC
LIMIT $4
"""

# Reciprocal Rank Fusion over the two rankings. A FULL OUTER JOIN keeps chunks
# found by only one of them, which is the entire point of hybrid retrieval.
_SEARCH_HYBRID_SQL = """
WITH vector_hits AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> $1::vector) AS rank
    FROM chunks
    WHERE workspace_id = $2 AND embedding_model = $3
    ORDER BY embedding <=> $1::vector
    LIMIT $4
),
keyword_hits AS (
    SELECT c.id, ROW_NUMBER() OVER (ORDER BY ts_rank_cd(c.tsv, q.query) DESC) AS rank
    FROM chunks c, websearch_to_tsquery('english', $5) AS q(query)
    WHERE c.workspace_id = $2 AND c.embedding_model = $3 AND c.tsv @@ q.query
    ORDER BY ts_rank_cd(c.tsv, q.query) DESC
    LIMIT $4
),
fused AS (
    SELECT COALESCE(v.id, k.id) AS id,
           COALESCE(1.0 / ($6::float + v.rank), 0.0)
         + COALESCE(1.0 / ($6::float + k.rank), 0.0) AS score
    FROM vector_hits v
    FULL OUTER JOIN keyword_hits k ON v.id = k.id
)
SELECT c.id, c.document_id, c.ordinal, c.content, c.title, c.source_uri, c.metadata,
       f.score
FROM fused f
JOIN chunks c ON c.workspace_id = $2 AND c.id = f.id
ORDER BY f.score DESC
LIMIT $7
"""

_UPSERT_CHUNK_SQL = """
INSERT INTO chunks (workspace_id, id, document_id, ordinal, content, title,
                    source_uri, metadata, embedding_model, embedding)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb, $9, $10::vector)
ON CONFLICT (workspace_id, id) DO UPDATE SET
    document_id     = EXCLUDED.document_id,
    ordinal         = EXCLUDED.ordinal,
    content         = EXCLUDED.content,
    title           = EXCLUDED.title,
    source_uri      = EXCLUDED.source_uri,
    metadata        = EXCLUDED.metadata,
    embedding_model = EXCLUDED.embedding_model,
    embedding       = EXCLUDED.embedding
"""

_UPSERT_DOCUMENT_SQL = """
INSERT INTO documents (workspace_id, id, source_uri, title, content_hash, metadata,
                       updated_at, indexed_at)
VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7, now())
ON CONFLICT (workspace_id, id) DO UPDATE SET
    source_uri   = EXCLUDED.source_uri,
    title        = EXCLUDED.title,
    content_hash = EXCLUDED.content_hash,
    metadata     = EXCLUDED.metadata,
    updated_at   = EXCLUDED.updated_at,
    indexed_at   = now()
"""


class PgVectorOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dsn: str = "postgresql://postgres:postgres@localhost:5432/osc_assistant"
    workspace_id: str = "default"
    dimensions: int = Field(default=0, ge=0)
    embedding_model: str = ""
    rrf_k: int = Field(default=60, ge=1)
    min_pool_size: int = Field(default=1, ge=1)
    max_pool_size: int = Field(default=10, ge=1)
    migrations_path: Path = Path("migrations")
    auto_migrate: bool = Field(
        default=True, description="Apply pending migrations during setup()."
    )


class PgVectorStore:
    """Adapter over PostgreSQL with the pgvector extension."""

    def __init__(self, options: PgVectorOptions) -> None:
        if options.dimensions <= 0:
            raise ConfigurationError(
                "PgVectorStore needs the embedding dimension. It is injected by the "
                "container from the active embedding model."
            )
        self._options = options
        self._pool: Any = None

    @property
    def dimensions(self) -> int:
        return self._options.dimensions

    @property
    def workspace_id(self) -> str:
        """The partition this store reads and writes. Every query is scoped to it."""
        return self._options.workspace_id

    async def setup(self) -> None:
        """Open the pool and, unless disabled, apply pending migrations."""
        if self._pool is not None:
            return
        try:
            import asyncpg
        except ImportError as exc:  # pragma: no cover - asyncpg is a core dependency
            raise VectorStoreError("asyncpg is required for the pgvector store.") from exc

        self._pool = await asyncpg.create_pool(
            dsn=self._options.dsn,
            min_size=self._options.min_pool_size,
            max_size=self._options.max_pool_size,
            init=_register_codecs,
        )
        if self._options.auto_migrate:
            await self._migrate()

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def replace_document(
        self, document: Document, chunks: Sequence[EmbeddedChunk]
    ) -> None:
        """Replace a document and its chunks in a single transaction.

        Delete-then-insert rather than upsert: chunk ids incorporate content, so an
        edit yields new ids and the superseded chunks would otherwise linger and
        stay retrievable. The transaction is what makes the document hash a
        truthful claim that the chunks exist.
        """
        rows = [
            (
                self._options.workspace_id,
                embedded.chunk.id,
                embedded.chunk.document_id,
                embedded.chunk.ordinal,
                embedded.chunk.text,
                embedded.chunk.title,
                embedded.chunk.source_uri,
                # Passed as a dict, not a JSON string: the connection registers a
                # jsonb codec (`_register_codecs`) that serialises it. Encoding it
                # here as well stored a JSON *string containing JSON*, so metadata
                # read back as `str` rather than `dict` and every consumer of
                # `Chunk.metadata` silently received the wrong type.
                dict(embedded.chunk.metadata),
                embedded.embedding_model,
                _encode_vector(embedded.vector),
            )
            for embedded in chunks
        ]

        async with self._acquire() as connection, connection.transaction():
            # Cascades to the old chunks via the composite foreign key.
            await connection.execute(
                "DELETE FROM documents WHERE workspace_id = $1 AND id = $2",
                self._options.workspace_id,
                document.id,
            )
            await connection.execute(
                _UPSERT_DOCUMENT_SQL,
                self._options.workspace_id,
                document.id,
                document.source_uri,
                document.title,
                document.hash,
                dict(document.metadata),
                document.updated_at,
            )
            if rows:
                await connection.executemany(_UPSERT_CHUNK_SQL, rows)

    async def delete_document(self, document_id: str) -> None:
        # Chunks are removed by the ON DELETE CASCADE on the composite foreign key.
        async with self._acquire() as connection:
            await connection.execute(
                "DELETE FROM documents WHERE workspace_id = $1 AND id = $2",
                self._options.workspace_id,
                document_id,
            )

    async def list_document_hashes(self) -> dict[str, str]:
        async with self._acquire() as connection:
            rows = await connection.fetch(
                "SELECT id, content_hash FROM documents WHERE workspace_id = $1",
                self._options.workspace_id,
            )
        return {row["id"]: row["content_hash"] for row in rows}

    async def document_ids(self) -> set[str]:
        return set(await self.list_document_hashes())

    async def search_vector(self, vector: Vector, limit: int) -> list[ScoredChunk]:
        async with self._acquire() as connection:
            rows = await connection.fetch(
                _SEARCH_VECTOR_SQL,
                _encode_vector(vector),
                self._options.workspace_id,
                self._options.embedding_model,
                limit,
            )
        return [_to_scored_chunk(row, MatchSource.VECTOR) for row in rows]

    async def search_keyword(self, query: str, limit: int) -> list[ScoredChunk]:
        async with self._acquire() as connection:
            rows = await connection.fetch(
                _SEARCH_KEYWORD_SQL,
                query,
                self._options.workspace_id,
                self._options.embedding_model,
                limit,
            )
        return [_to_scored_chunk(row, MatchSource.KEYWORD) for row in rows]

    async def search_hybrid(
        self, vector: Vector, query: str, limit: int
    ) -> list[ScoredChunk]:
        async with self._acquire() as connection:
            rows = await connection.fetch(
                _SEARCH_HYBRID_SQL,
                _encode_vector(vector),
                self._options.workspace_id,
                self._options.embedding_model,
                limit,
                query,
                self._options.rrf_k,
                limit,
            )
        return [_to_scored_chunk(row, MatchSource.HYBRID) for row in rows]

    def _acquire(self) -> Any:
        if self._pool is None:
            raise VectorStoreError("Vector store used before setup() was called.")
        return self._pool.acquire()

    async def _migrate(self) -> None:
        """Apply unapplied migration files in filename order.

        A hand-rolled runner rather than Alembic: migrations here are plain SQL with
        one substitution, applied forward only. Alembic's autogeneration and
        branching model would be more machinery than that warrants.
        """
        directory = self._options.migrations_path
        if not directory.is_dir():
            raise ConfigurationError(f"Migrations directory not found: {directory}")

        async with self._acquire() as connection:
            await connection.execute(
                "CREATE TABLE IF NOT EXISTS schema_migrations ("
                "  version TEXT PRIMARY KEY,"
                "  applied_at TIMESTAMPTZ NOT NULL DEFAULT now()"
                ")"
            )
            applied = {
                row["version"]
                for row in await connection.fetch("SELECT version FROM schema_migrations")
            }

            for path in sorted(directory.glob("*.sql")):
                if path.name in applied:
                    continue
                sql = path.read_text(encoding="utf-8").replace(
                    DIMENSION_PLACEHOLDER, str(self._options.dimensions)
                )
                async with connection.transaction():
                    await connection.execute(sql)
                    await connection.execute(
                        "INSERT INTO schema_migrations (version) VALUES ($1)", path.name
                    )
                log.info("migration.applied", extra={"version": path.name})

        await self._assert_dimensions_match()

    async def _assert_dimensions_match(self) -> None:
        """Fail loudly if the stored vector width disagrees with the active model.

        Silently comparing vectors of different widths, or from different models of
        the same width, produces plausible-looking nonsense. Better to refuse to start.
        """
        async with self._acquire() as connection:
            actual = await connection.fetchval(
                "SELECT atttypmod FROM pg_attribute "
                "WHERE attrelid = 'chunks'::regclass AND attname = 'embedding'"
            )
        if actual is not None and actual > 0 and actual != self._options.dimensions:
            raise ConfigurationError(
                f"The chunks table stores {actual}-dimensional vectors but the "
                f"configured embedding model produces {self._options.dimensions}. "
                f"Create a new database (or drop and re-create the chunks table) and "
                f"re-index the corpus."
            )


async def _register_codecs(connection: Any) -> None:
    """Decode JSONB into Python objects instead of raw strings."""
    await connection.set_type_codec(
        "jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )


def _encode_vector(vector: Vector) -> str:
    """Render a vector in pgvector's literal form for the `::vector` cast."""
    return "[" + ",".join(format(value, ".8g") for value in vector) + "]"


def _to_scored_chunk(row: Any, source: MatchSource) -> ScoredChunk:
    return ScoredChunk(
        chunk=Chunk(
            id=row["id"],
            document_id=row["document_id"],
            ordinal=row["ordinal"],
            text=row["content"],
            title=row["title"],
            source_uri=row["source_uri"],
            metadata=row["metadata"] or {},
        ),
        score=float(row["score"]),
        source=source,
    )


@vector_store_registry.register("pgvector")
@vector_store_registry.register("postgres")
def _build(config: ComponentConfig) -> VectorStore:
    return PgVectorStore(PgVectorOptions.model_validate(config.options))
