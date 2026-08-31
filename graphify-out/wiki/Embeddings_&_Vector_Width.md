# Embeddings & Vector Width

> 17 nodes

## Key Concepts

- **Ollama** (8 connections) — `docs/engineering/technologies/ollama.md`
- **top_k Has Not Been Re-Tuned Since The Chunker Changed** (5 connections) — `PROJECT_STATUS.md`
- **Retrieval Configuration Knobs** (4 connections) — `docs/engineering/architecture/retrieval.md`
- **4096-Token Context Caps The Corpus Per Answer** (3 connections) — `docs/engineering/technologies/ollama.md`
- **Chunk Size As The Highest-Leverage Knob** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **nomic-embed-text (768 dimensions)** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Vector Dimension Fixed In The DDL / DimensionMismatchError** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Container Injects Vector Width And Embedding Model Id** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **qwen3:8b** (2 connections) — `docs/engineering/technologies/ollama.md`
- **nomic-embed-text** (2 connections) — `docs/engineering/technologies/ollama.md`
- **Conditional HNSW Index (dimension <= 2000)** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Technical Debt Register** (2 connections) — `PROJECT_STATUS.md`
- **Reached Through The openai_compatible Adapter** (1 connections) — `docs/engineering/technologies/ollama.md`
- **The Numeric-Fidelity Gap** (1 connections) — `docs/engineering/technologies/ollama.md`
- **Citations Are Asserted, Not Verified** (1 connections) — `docs/engineering/technologies/ollama.md`
- **Duplicate Chunks Undetected (content_hash limitation)** (1 connections) — `PROJECT_STATUS.md`
- **Embedding Model Chosen Independently Of The Chat Model** (1 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`

## Relationships

- [Ingestion Tests](Ingestion_Tests.md) (2 shared connections)
- [Measured Chunker Decision & IR Metrics](Measured_Chunker_Decision_%26_IR_Metrics.md) (2 shared connections)
- [LangChain Splitters](LangChain_Splitters.md) (1 shared connections)
- [Reasoning-Model Hygiene](Reasoning-Model_Hygiene.md) (1 shared connections)
- [Conversational Evaluation Tests](Conversational_Evaluation_Tests.md) (1 shared connections)
- [Retrieval Metric Functions](Retrieval_Metric_Functions.md) (1 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (1 shared connections)
- [Anthropic Adapter](Anthropic_Adapter.md) (1 shared connections)

## Source Files

- `PROJECT_STATUS.md`
- `docs/engineering/architecture/chunking-and-embeddings.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/technologies/ollama.md`
- `docs/engineering/technologies/postgresql-pgvector.md`

## Audit Trail

- EXTRACTED: 35 (80%)
- INFERRED: 9 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*