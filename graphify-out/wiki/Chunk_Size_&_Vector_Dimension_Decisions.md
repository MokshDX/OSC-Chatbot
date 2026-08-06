# Chunk Size & Vector Dimension Decisions

> 16 nodes · cohesion 0.14

## Key Concepts

- **Ollama** (9 connections) — `docs/engineering/technologies/ollama.md`
- **Chunk Size As The Highest-Leverage Knob** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Vector Dimension Fixed In The DDL / DimensionMismatchError** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **nomic-embed-text (768 dimensions)** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Lazy cached_property Container Construction** (3 connections) — `docs/engineering/architecture/provider-architecture.md`
- **4096-Token Context Caps The Corpus Per Answer** (3 connections) — `docs/engineering/technologies/ollama.md`
- **nomic-embed-text** (3 connections) — `docs/engineering/technologies/ollama.md`
- **qwen3:8b** (3 connections) — `docs/engineering/technologies/ollama.md`
- **fact_match** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **Container Injects Vector Width And Embedding Model Id** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Registry And Composition Root Wiring** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Lifespan Owns The Container** (2 connections) — `docs/engineering/technologies/fastapi.md`
- **The Numeric-Fidelity Gap** (2 connections) — `docs/engineering/technologies/ollama.md`
- **Conditional HNSW Index (dimension <= 2000)** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Embedding Model Chosen Independently Of The Chat Model** (1 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Reached Through The openai_compatible Adapter** (1 connections) — `docs/engineering/technologies/ollama.md`

## Relationships

- [Evaluation Harness & CI Gate](Evaluation_Harness_%26_CI_Gate.md) (3 shared connections)
- [Chunking & Embedding Architecture](Chunking_%26_Embedding_Architecture.md) (2 shared connections)
- [Module Map & Dependency Rules](Module_Map_%26_Dependency_Rules.md) (2 shared connections)
- [Architecture Overview & Weak Points](Architecture_Overview_%26_Weak_Points.md) (2 shared connections)
- [Retrieval Architecture & Metrics](Retrieval_Architecture_%26_Metrics.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/chunking-and-embeddings.md`
- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/technologies/fastapi.md`
- `docs/engineering/technologies/ollama.md`
- `docs/engineering/technologies/postgresql-pgvector.md`

## Audit Trail

- EXTRACTED: 31 (70%)
- INFERRED: 13 (30%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*