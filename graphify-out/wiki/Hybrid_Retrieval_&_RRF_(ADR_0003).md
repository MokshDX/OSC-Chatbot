# Hybrid Retrieval & RRF (ADR 0003)

> 15 nodes

## Key Concepts

- **PostgreSQL + pgvector** (12 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **ADR 0003 — Hybrid Retrieval With RRF Fused In SQL** (11 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **Hybrid Search (default)** (5 connections) — `docs/engineering/architecture/retrieval.md`
- **SQL-Side RRF Fusion (two CTEs)** (4 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Keyword Search (tsvector / BM25-equivalent)** (3 connections) — `docs/engineering/architecture/retrieval.md`
- **Reciprocal Rank Fusion (k = 60)** (3 connections) — `docs/engineering/architecture/retrieval.md`
- **VectorStore Protocol** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Vector Search** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **Cormack, Clarke & Buettcher, Reciprocal Rank Fusion (SIGIR 2009)** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **Rejected: Fusion In Application Code Over Two Queries** (2 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **search_vector Is A Generated Column** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Rejected: Weighted Score Combination Instead Of RRF** (1 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **rrf_k = 60 Is Adopted On Authority, Not Tuned Here** (1 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **min_score Is Nearly Useless In Hybrid Mode** (1 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **One Datastore Holds Everything** (1 connections) — `docs/engineering/technologies/postgresql-pgvector.md`

## Relationships

- [Evaluation Metrics & CI Gate](Evaluation_Metrics_%26_CI_Gate.md) (4 shared connections)
- [ADRs — Protocol & LangChain Decisions](ADRs_%E2%80%94_Protocol_%26_LangChain_Decisions.md) (3 shared connections)
- [The Five Protocol Seams](The_Five_Protocol_Seams.md) (2 shared connections)
- [Embedding & Chunk-Size Decisions](Embedding_%26_Chunk-Size_Decisions.md) (2 shared connections)
- [Observability & API Weak Points](Observability_%26_API_Weak_Points.md) (2 shared connections)
- [Persistent Tracing Design (ADR 0004)](Persistent_Tracing_Design_%28ADR_0004%29.md) (1 shared connections)
- [Chunking Strategies & Ingestion Rules](Chunking_Strategies_%26_Ingestion_Rules.md) (1 shared connections)
- [ADR 0007 — Corpus Root Is docs/company/; The FAQ Is Split...](ADR_0007_%E2%80%94_Corpus_Root_Is_docs-company-%3B_The_FAQ_Is_Split.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/decisions/0003-hybrid-retrieval.md`
- `docs/engineering/technologies/postgresql-pgvector.md`

## Audit Trail

- EXTRACTED: 41 (79%)
- INFERRED: 11 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*