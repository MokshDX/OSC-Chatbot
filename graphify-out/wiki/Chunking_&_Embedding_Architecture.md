# Chunking & Embedding Architecture

> 21 nodes · cohesion 0.14

## Key Concepts

- **Chunking And Embedding Pipeline** (16 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **ADR 0006 — Keep recursive As The Default Until Measured** (9 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **Shared Chunk Id Helper And Idempotent Ingestion** (7 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **markdown Chunking Strategy** (5 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **recursive Chunking Strategy (default)** (4 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **The Ingestion Path** (4 connections) — `docs/engineering/architecture/overview.md`
- **A Retrieval Change Ships With A Measured Improvement** (4 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **langchain-text-splitters** (4 connections) — `docs/engineering/technologies/langchain.md`
- **langchain_recursive Chunking Strategy** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Unparseable Files Are Recorded As Failures, Not Deleted** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **fixed Chunking Strategy** (2 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **A Failed Case Never Aborts The Run** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **Corpus Authoring Conventions** (2 connections) — `docs/engineering/architecture/knowledge-corpus.md`
- **Chunker Protocol** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Cross-Encoder Reranking (off by default)** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **Ingestion Assumes A Single Writer** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Chunk Denormalises Title And Source URI** (1 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **EmbeddedChunk Carries Its Embedding Model Id** (1 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Character-Based Rather Than Token-Based Sizing** (1 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **fixed Retained As An Evaluation Control** (1 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **Semantic Chunking Deferred** (1 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`

## Relationships

- [Corpus Boundary & Golden Set Curation](Corpus_Boundary_%26_Golden_Set_Curation.md) (5 shared connections)
- [Module Map & Dependency Rules](Module_Map_%26_Dependency_Rules.md) (5 shared connections)
- [Retrieval Architecture & Metrics](Retrieval_Architecture_%26_Metrics.md) (3 shared connections)
- [Chunk Size & Vector Dimension Decisions](Chunk_Size_%26_Vector_Dimension_Decisions.md) (2 shared connections)
- [Evaluation Harness & CI Gate](Evaluation_Harness_%26_CI_Gate.md) (2 shared connections)
- [Graphify Graph Findings](Graphify_Graph_Findings.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/chunking-and-embeddings.md`
- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/knowledge-corpus.md`
- `docs/engineering/architecture/overview.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/decisions/0006-chunking-strategy.md`
- `docs/engineering/technologies/langchain.md`
- `docs/engineering/technologies/postgresql-pgvector.md`

## Audit Trail

- EXTRACTED: 59 (78%)
- INFERRED: 17 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*