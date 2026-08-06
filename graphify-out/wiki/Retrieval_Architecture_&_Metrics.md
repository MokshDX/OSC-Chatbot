# Retrieval Architecture & Metrics

> 18 nodes · cohesion 0.16

## Key Concepts

- **Six-Stage Retrieval Pipeline** (11 connections) — `docs/engineering/architecture/retrieval.md`
- **PostgreSQL + pgvector** (11 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **ADR 0003 — Hybrid Retrieval With RRF Fused In SQL** (9 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **Hybrid Search (default)** (5 connections) — `docs/engineering/architecture/retrieval.md`
- **SQL-Side RRF Fusion (two CTEs)** (4 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Keyword Search (tsvector / BM25-equivalent)** (3 connections) — `docs/engineering/architecture/retrieval.md`
- **Reciprocal Rank Fusion (k = 60)** (3 connections) — `docs/engineering/architecture/retrieval.md`
- **recall@k** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **VectorStore Protocol** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Cormack, Clarke & Buettcher, Reciprocal Rank Fusion (SIGIR 2009)** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **min_score Applied Before Reranking** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **Vector Search** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **Rejected: Fusion In Application Code Over Two Queries** (2 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **search_vector Is A Generated Column** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **min_score Is Nearly Useless In Hybrid Mode** (1 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **rrf_k = 60 Is Adopted On Authority, Not Tuned Here** (1 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **Rejected: Weighted Score Combination Instead Of RRF** (1 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **One Datastore Holds Everything** (1 connections) — `docs/engineering/technologies/postgresql-pgvector.md`

## Relationships

- [Evaluation Harness & CI Gate](Evaluation_Harness_%26_CI_Gate.md) (5 shared connections)
- [Chunking & Embedding Architecture](Chunking_%26_Embedding_Architecture.md) (3 shared connections)
- [Architecture Overview & Weak Points](Architecture_Overview_%26_Weak_Points.md) (3 shared connections)
- [Module Map & Dependency Rules](Module_Map_%26_Dependency_Rules.md) (2 shared connections)
- [Chunk Size & Vector Dimension Decisions](Chunk_Size_%26_Vector_Dimension_Decisions.md) (1 shared connections)
- [Trace Persistence Decision (ADR 0004)](Trace_Persistence_Decision_%28ADR_0004%29.md) (1 shared connections)
- [Corpus Boundary & Golden Set Curation](Corpus_Boundary_%26_Golden_Set_Curation.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/decisions/0003-hybrid-retrieval.md`
- `docs/engineering/technologies/postgresql-pgvector.md`

## Audit Trail

- EXTRACTED: 52 (81%)
- INFERRED: 12 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*