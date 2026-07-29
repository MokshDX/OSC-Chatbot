-- Initial schema for the OSC knowledge assistant.
--
-- {{EMBEDDING_DIMENSIONS}} is substituted by the migration runner from the active
-- embedding model. Vector width is fixed at DDL time because pgvector cannot index
-- an unconstrained vector column; changing embedding model therefore means a new
-- migration and a full re-index, which the runner detects and reports rather than
-- silently mixing incompatible vectors.

CREATE EXTENSION IF NOT EXISTS vector;

-- Every table is partitioned by workspace_id from the outset. There is one
-- workspace today. Adding this key later would be a data migration; carrying it
-- now costs one column and one index prefix.
CREATE TABLE IF NOT EXISTS documents (
    workspace_id  TEXT        NOT NULL,
    id            TEXT        NOT NULL,
    source_uri    TEXT        NOT NULL,
    title         TEXT        NOT NULL,
    content_hash  TEXT        NOT NULL,
    metadata      JSONB       NOT NULL DEFAULT '{}'::jsonb,
    updated_at    TIMESTAMPTZ,
    indexed_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (workspace_id, id)
);

CREATE TABLE IF NOT EXISTS chunks (
    workspace_id     TEXT        NOT NULL,
    id               TEXT        NOT NULL,
    document_id      TEXT        NOT NULL,
    ordinal          INTEGER     NOT NULL,
    content          TEXT        NOT NULL,
    title            TEXT        NOT NULL,
    source_uri       TEXT        NOT NULL,
    metadata         JSONB       NOT NULL DEFAULT '{}'::jsonb,
    embedding_model  TEXT        NOT NULL,
    embedding        VECTOR({{EMBEDDING_DIMENSIONS}}) NOT NULL,
    -- Generated rather than maintained by the application: it cannot drift from
    -- the content, and a re-index needs no application change.
    tsv              TSVECTOR GENERATED ALWAYS AS
                         (to_tsvector('english'::regconfig, content)) STORED,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (workspace_id, id),
    FOREIGN KEY (workspace_id, document_id)
        REFERENCES documents (workspace_id, id) ON DELETE CASCADE
);

-- Cosine distance, matching the similarity used by every embedding provider here.
--
-- pgvector cannot build an HNSW index on a column wider than 2000 dimensions, and
-- several supported models exceed that (OpenAI text-embedding-3-large is 3072).
-- Creating it unconditionally would abort the migration for those models, so above
-- the limit the column is left unindexed: search falls back to an exact scan, which
-- is correct but O(n) and will need revisiting as the corpus grows.
DO $$
BEGIN
    IF {{EMBEDDING_DIMENSIONS}} <= 2000 THEN
        CREATE INDEX IF NOT EXISTS chunks_embedding_idx
            ON chunks USING hnsw (embedding vector_cosine_ops);
    ELSE
        RAISE WARNING
            'Embedding width % exceeds pgvector''s 2000-dimension HNSW limit; '
            'vector search will use an exact scan. Choose a narrower embedding '
            'model, or halfvec, before the corpus grows large.',
            {{EMBEDDING_DIMENSIONS}};
    END IF;
END
$$;

CREATE INDEX IF NOT EXISTS chunks_tsv_idx
    ON chunks USING gin (tsv);

CREATE INDEX IF NOT EXISTS chunks_document_idx
    ON chunks (workspace_id, document_id);

-- Retrieval always filters by workspace and embedding model, so both belong in
-- the same index as the lookup path.
CREATE INDEX IF NOT EXISTS chunks_workspace_model_idx
    ON chunks (workspace_id, embedding_model);
