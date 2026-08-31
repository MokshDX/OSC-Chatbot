# Retrieval Metric Functions

> 17 nodes

## Key Concepts

- **PostgreSQL + pgvector** (10 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **ADR 0004 — Persist Traces To A Bounded JSONL File** (5 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **Ingestion Path** (3 connections) — `docs/engineering/architecture/overview.md`
- **Never Let A Vendor Exception Escape An Adapter** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Rejected: A traces Table In PostgreSQL** (2 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **asyncpg Errors Translated To VectorStoreError** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Ingestion Assumes A Single Writer** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **One Database Is One Failure Domain** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Every Case Records Its Trace Id** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **VectorStore Protocol** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Auto-Explain On Failure** (1 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **OpenTelemetry Exporter Deferred, Span Stays OTel-Shaped** (1 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **Bounded Means Lossy — Not An Audit Log** (1 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **One Datastore Holds Everything** (1 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **search_vector Is A Generated Column** (1 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **SQL-Side RRF Fusion (two CTEs)** (1 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **workspace_id On Every Table** (1 connections) — `docs/engineering/technologies/postgresql-pgvector.md`

## Relationships

- [LangChain Splitters](LangChain_Splitters.md) (1 shared connections)
- [Reasoning-Model Hygiene](Reasoning-Model_Hygiene.md) (1 shared connections)
- [Embeddings & Vector Width](Embeddings_%26_Vector_Width.md) (1 shared connections)
- [Conversational Evaluation Tests](Conversational_Evaluation_Tests.md) (1 shared connections)
- [Corpus Boundary Rules](Corpus_Boundary_Rules.md) (1 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/overview.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/decisions/0004-persistent-tracing.md`
- `docs/engineering/technologies/postgresql-pgvector.md`

## Audit Trail

- EXTRACTED: 28 (74%)
- INFERRED: 10 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*