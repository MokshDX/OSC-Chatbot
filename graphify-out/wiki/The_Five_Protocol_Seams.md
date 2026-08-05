# The Five Protocol Seams

> 20 nodes

## Key Concepts

- **The Five Protocol Seams** (19 connections) — `docs/engineering/architecture/provider-architecture.md`
- **LangChain** (10 connections) — `docs/engineering/technologies/langchain.md`
- **What LangChain Was Refused** (5 connections) — `docs/engineering/technologies/langchain.md`
- **integrations/ May Import The Core; The Core May Never Import integrations/** (4 connections) — `docs/engineering/architecture/overview.md`
- **Protocols Rather Than Abstract Base Classes** (4 connections) — `docs/engineering/architecture/provider-architecture.md`
- **mypy --strict As Load-Bearing Architecture** (4 connections) — `docs/engineering/technologies/python-tooling.md`
- **Module Map** (3 connections) — `docs/engineering/architecture/overview.md`
- **Business Logic Imports protocols And types Only** (3 connections) — `docs/engineering/architecture/overview.md`
- **Two-Tier Provider Strategy** (3 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Adopt Where Undifferentiated, Keep OSC's Code Where OSC's Design Is Better** (3 connections) — `docs/engineering/decisions/0002-langchain-scope.md`
- **The Open Chunker Comparison (Milestone A)** (3 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **Protocols Are Enforced Only Statically** (2 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- **langchain_bridge Provider Adapter** (2 connections) — `docs/engineering/technologies/langchain.md`
- **OSC Exposed As A LangChain BaseRetriever** (2 connections) — `docs/engineering/technologies/langchain.md`
- **ChatModel Protocol** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **EmbeddingModel Protocol** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Reranker Protocol** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **StoreInspector Optional Protocol** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **PEP 544 — Structural Subtyping** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Name The Class By Import Path, Not init_chat_model** (1 connections) — `docs/engineering/technologies/langchain.md`

## Relationships

- [ADRs — Protocol & LangChain Decisions](ADRs_%E2%80%94_Protocol_%26_LangChain_Decisions.md) (9 shared connections)
- [Evaluation Metrics & CI Gate](Evaluation_Metrics_%26_CI_Gate.md) (5 shared connections)
- [Chunking Strategies & Ingestion Rules](Chunking_Strategies_%26_Ingestion_Rules.md) (4 shared connections)
- [Golden Set & Config Layering](Golden_Set_%26_Config_Layering.md) (2 shared connections)
- [Embedding & Chunk-Size Decisions](Embedding_%26_Chunk-Size_Decisions.md) (2 shared connections)
- [Hybrid Retrieval & RRF (ADR 0003)](Hybrid_Retrieval_%26_RRF_%28ADR_0003%29.md) (2 shared connections)
- [Four Test Tiers](Four_Test_Tiers.md) (2 shared connections)
- [ADR 0007 — Corpus Root Is docs/company/; The FAQ Is Split...](ADR_0007_%E2%80%94_Corpus_Root_Is_docs-company-%3B_The_FAQ_Is_Split.md) (1 shared connections)
- [Observability & API Weak Points](Observability_%26_API_Weak_Points.md) (1 shared connections)
- [Persistent Tracing Design (ADR 0004)](Persistent_Tracing_Design_%28ADR_0004%29.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/overview.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/decisions/0001-provider-abstraction.md`
- `docs/engineering/decisions/0002-langchain-scope.md`
- `docs/engineering/decisions/0006-chunking-strategy.md`
- `docs/engineering/technologies/langchain.md`
- `docs/engineering/technologies/python-tooling.md`

## Audit Trail

- EXTRACTED: 56 (77%)
- INFERRED: 17 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*