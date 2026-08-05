# Embedding & Chunk-Size Decisions

> 19 nodes

## Key Concepts

- **Ollama** (10 connections) — `docs/engineering/technologies/ollama.md`
- **A Found Defect Gets A Regression Test In The Same Commit** (4 connections) — `docs/engineering/architecture/testing.md`
- **qwen3:8b** (4 connections) — `docs/engineering/technologies/ollama.md`
- **Chunk Size As The Highest-Leverage Knob** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **nomic-embed-text (768 dimensions)** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Vector Dimension Fixed In The DDL / DimensionMismatchError** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Lazy cached_property Container Construction** (3 connections) — `docs/engineering/architecture/provider-architecture.md`
- **min_score Applied Before Reranking** (3 connections) — `docs/engineering/architecture/retrieval.md`
- **nomic-embed-text** (3 connections) — `docs/engineering/technologies/ollama.md`
- **4096-Token Context Caps The Corpus Per Answer** (3 connections) — `docs/engineering/technologies/ollama.md`
- **fact_match** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **Registry And Composition Root Wiring** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Container Injects Vector Width And Embedding Model Id** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Lifespan Owns The Container** (2 connections) — `docs/engineering/technologies/fastapi.md`
- **Every SSE Exit Path Emits A Terminal Event** (2 connections) — `docs/engineering/technologies/fastapi.md`
- **The Numeric-Fidelity Gap** (2 connections) — `docs/engineering/technologies/ollama.md`
- **Conditional HNSW Index (dimension <= 2000)** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Embedding Model Chosen Independently Of The Chat Model** (1 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Reached Through The openai_compatible Adapter** (1 connections) — `docs/engineering/technologies/ollama.md`

## Relationships

- [Evaluation Metrics & CI Gate](Evaluation_Metrics_%26_CI_Gate.md) (4 shared connections)
- [Observability & API Weak Points](Observability_%26_API_Weak_Points.md) (3 shared connections)
- [Chunking Strategies & Ingestion Rules](Chunking_Strategies_%26_Ingestion_Rules.md) (2 shared connections)
- [The Five Protocol Seams](The_Five_Protocol_Seams.md) (2 shared connections)
- [Hybrid Retrieval & RRF (ADR 0003)](Hybrid_Retrieval_%26_RRF_%28ADR_0003%29.md) (2 shared connections)
- [Four Test Tiers](Four_Test_Tiers.md) (1 shared connections)
- [ADRs — Protocol & LangChain Decisions](ADRs_%E2%80%94_Protocol_%26_LangChain_Decisions.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/chunking-and-embeddings.md`
- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/architecture/testing.md`
- `docs/engineering/technologies/fastapi.md`
- `docs/engineering/technologies/ollama.md`
- `docs/engineering/technologies/postgresql-pgvector.md`

## Audit Trail

- EXTRACTED: 35 (64%)
- INFERRED: 20 (36%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*