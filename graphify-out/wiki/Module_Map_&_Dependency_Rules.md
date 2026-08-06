# Module Map & Dependency Rules

> 30 nodes · cohesion 0.09

## Key Concepts

- **The Five Protocol Seams** (22 connections) — `PROJECT_STATUS.md`
- **LangChain** (9 connections) — `docs/engineering/technologies/langchain.md`
- **ADR 0001 — Five Protocols As The Swappability Seams** (8 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- **ADR 0002 — Adopt LangChain For Undifferentiated Work Only** (7 connections) — `docs/engineering/decisions/0002-langchain-scope.md`
- **integrations/ May Import The Core; The Core May Never Import integrations/** (4 connections) — `docs/engineering/architecture/overview.md`
- **What LangChain Was Refused** (4 connections) — `docs/engineering/technologies/langchain.md`
- **mypy --strict As Load-Bearing Architecture** (4 connections) — `docs/engineering/technologies/python-tooling.md`
- **Scoped LangChain Adoption** (4 connections) — `PROJECT_STATUS.md`
- **Two-Tier Provider Strategy** (4 connections) — `PROJECT_STATUS.md`
- **Business Logic Imports protocols And types Only** (3 connections) — `docs/engineering/architecture/overview.md`
- **Module Map** (3 connections) — `docs/engineering/architecture/overview.md`
- **Protocols Rather Than Abstract Base Classes** (3 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Adopt Where Undifferentiated, Keep OSC's Code Where OSC's Design Is Better** (3 connections) — `docs/engineering/decisions/0002-langchain-scope.md`
- **The Open Chunker Comparison (Milestone A)** (3 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **Layered Configuration (env > .env > YAML profile)** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Protocols Are Enforced Only Statically** (2 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- **langchain_bridge Provider Adapter** (2 connections) — `docs/engineering/technologies/langchain.md`
- **OSC Exposed As A LangChain BaseRetriever** (2 connections) — `docs/engineering/technologies/langchain.md`
- **Four-Layer Settings Precedence** (2 connections) — `docs/engineering/technologies/python-tooling.md`
- **Tracing Is OSC's Own, Shaped Like OpenTelemetry** (2 connections) — `README.md`
- **ChatModel Protocol** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **EmbeddingModel Protocol** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **PEP 544 — Structural Subtyping** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Reranker Protocol** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Rejected: Abstract Base Classes And Framework Abstractions** (1 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- *... and 5 more nodes in this community*

## Relationships

- [Evaluation Harness & CI Gate](Evaluation_Harness_%26_CI_Gate.md) (5 shared connections)
- [Chunking & Embedding Architecture](Chunking_%26_Embedding_Architecture.md) (5 shared connections)
- [Architecture Overview & Weak Points](Architecture_Overview_%26_Weak_Points.md) (4 shared connections)
- [Corpus Boundary & Golden Set Curation](Corpus_Boundary_%26_Golden_Set_Curation.md) (3 shared connections)
- [Retrieval Architecture & Metrics](Retrieval_Architecture_%26_Metrics.md) (2 shared connections)
- [Chunk Size & Vector Dimension Decisions](Chunk_Size_%26_Vector_Dimension_Decisions.md) (2 shared connections)
- [Experiment Profiles & Embedding Caveats](Experiment_Profiles_%26_Embedding_Caveats.md) (2 shared connections)
- [Session Startup & Deduplication (ADR 0008)](Session_Startup_%26_Deduplication_%28ADR_0008%29.md) (1 shared connections)
- [Audit Stream, Redaction & osc logs](Audit_Stream%2C_Redaction_%26_osc_logs.md) (1 shared connections)
- [Graphify Graph Findings](Graphify_Graph_Findings.md) (1 shared connections)
- [The Logging System & Span Bridge](The_Logging_System_%26_Span_Bridge.md) (1 shared connections)

## Source Files

- `PROJECT_STATUS.md`
- `README.md`
- `docs/engineering/architecture/overview.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/decisions/0001-provider-abstraction.md`
- `docs/engineering/decisions/0002-langchain-scope.md`
- `docs/engineering/decisions/0006-chunking-strategy.md`
- `docs/engineering/technologies/langchain.md`
- `docs/engineering/technologies/python-tooling.md`

## Audit Trail

- EXTRACTED: 80 (78%)
- INFERRED: 23 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*