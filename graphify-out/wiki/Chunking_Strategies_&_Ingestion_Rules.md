# Chunking Strategies & Ingestion Rules

> 24 nodes

## Key Concepts

- **Chunking And Embedding Pipeline** (17 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **ADR 0006 — Keep recursive As The Default Until Measured** (12 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **Shared Chunk Id Helper And Idempotent Ingestion** (7 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **markdown Chunking Strategy** (5 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Relevance Scored At Document Level** (5 connections) — `docs/engineering/architecture/evaluation.md`
- **recursive Chunking Strategy (default)** (4 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Unparseable Files Are Recorded As Failures, Not Deleted** (4 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **FAQ Split Into 17 Topic Files** (4 connections) — `docs/engineering/architecture/knowledge-corpus.md`
- **The Ingestion Path** (4 connections) — `docs/engineering/architecture/overview.md`
- **A Retrieval Change Ships With A Measured Improvement** (4 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **langchain-text-splitters** (4 connections) — `docs/engineering/technologies/langchain.md`
- **langchain_recursive Chunking Strategy** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **fixed Chunking Strategy** (2 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **A Failed Case Never Aborts The Run** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **Corpus Authoring Conventions** (2 connections) — `docs/engineering/architecture/knowledge-corpus.md`
- **Chunker Protocol** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Cross-Encoder Reranking (off by default)** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **Rejected: Keep The FAQ As One File** (2 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- **Ingestion Assumes A Single Writer** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Chunk Denormalises Title And Source URI** (1 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **EmbeddedChunk Carries Its Embedding Model Id** (1 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **fixed Retained As An Evaluation Control** (1 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **Character-Based Rather Than Token-Based Sizing** (1 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **Semantic Chunking Deferred** (1 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`

## Relationships

- [ADRs — Protocol & LangChain Decisions](ADRs_%E2%80%94_Protocol_%26_LangChain_Decisions.md) (7 shared connections)
- [Evaluation Metrics & CI Gate](Evaluation_Metrics_%26_CI_Gate.md) (5 shared connections)
- [ADR 0007 — Corpus Root Is docs/company/; The FAQ Is Split...](ADR_0007_%E2%80%94_Corpus_Root_Is_docs-company-%3B_The_FAQ_Is_Split.md) (4 shared connections)
- [The Five Protocol Seams](The_Five_Protocol_Seams.md) (4 shared connections)
- [Embedding & Chunk-Size Decisions](Embedding_%26_Chunk-Size_Decisions.md) (2 shared connections)
- [Persistent Tracing Design (ADR 0004)](Persistent_Tracing_Design_%28ADR_0004%29.md) (1 shared connections)
- [Golden Set & Config Layering](Golden_Set_%26_Config_Layering.md) (1 shared connections)
- [Four Test Tiers](Four_Test_Tiers.md) (1 shared connections)
- [Hybrid Retrieval & RRF (ADR 0003)](Hybrid_Retrieval_%26_RRF_%28ADR_0003%29.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/chunking-and-embeddings.md`
- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/knowledge-corpus.md`
- `docs/engineering/architecture/overview.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/decisions/0006-chunking-strategy.md`
- `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- `docs/engineering/technologies/langchain.md`
- `docs/engineering/technologies/postgresql-pgvector.md`

## Audit Trail

- EXTRACTED: 67 (73%)
- INFERRED: 25 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*