# Ingestion Tests

> 28 nodes

## Key Concepts

- **Chunking And Embedding Pipeline** (10 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **markdown Chunking Strategy (default since ADR 0012)** (9 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Phase 6 Measured Baseline (schema corpus)** (5 connections) — `PROJECT_STATUS.md`
- **markdown Adopted As Default Chunker on Evidence (ADR 0012)** (5 connections) — `PROJECT_STATUS.md`
- **Measured Retrieval Baseline (schema suite)** (5 connections) — `docs/engineering/architecture/retrieval.md`
- **LangChain** (5 connections) — `docs/engineering/technologies/langchain.md`
- **langchain-text-splitters** (5 connections) — `docs/engineering/technologies/langchain.md`
- **Derived Regression Gates (evaluation/gate.py)** (4 connections) — `PROJECT_STATUS.md`
- **Baseline → Change → Measure → Keep/Reject Rule** (4 connections) — `PROJECT_STATUS.md`
- **Current Corpus Contents — 11 Documents / 80 Chunks** (4 connections) — `docs/engineering/architecture/knowledge-corpus.md`
- **recursive Chunking Strategy (former default, superseded by markdown)** (4 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **What LangChain Was Refused** (4 connections) — `docs/engineering/technologies/langchain.md`
- **Adopt Where Undifferentiated, Keep OSC's Code Where OSC's Design Is Better** (3 connections) — `docs/engineering/decisions/0002-langchain-scope.md`
- **Two Canonical Commands — make verify and make eval** (3 connections) — `PROJECT_STATUS.md`
- **langchain_bridge Provider Adapter** (3 connections) — `docs/engineering/technologies/langchain.md`
- **LangChain — Adopted and Rejected Scope** (2 connections) — `PROJECT_STATUS.md`
- **FAQ Split Into 17 Topic Files** (2 connections) — `docs/engineering/architecture/knowledge-corpus.md`
- **langchain_recursive Chunking Strategy** (2 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Adopt LangChain For Undifferentiated Work, Keep OSC's Own Code Where OSC's Design Is Better** (2 connections) — `docs/engineering/technologies/langchain.md`
- **Dependency Posture — Core Runtime Small, Vendor SDKs Are Extras** (2 connections) — `docs/engineering/technologies/langchain.md`
- **Chunker Protocol** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Testing Status (445 tests, make verify)** (1 connections) — `PROJECT_STATUS.md`
- **Corpus Authoring Conventions (H1 title, question headings, kebab-case)** (1 connections) — `docs/engineering/architecture/knowledge-corpus.md`
- **Why Documents Are Split At All** (1 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Chunk Denormalises Title And Source URI** (1 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- *... and 3 more nodes in this community*

## Relationships

- [Measured Chunker Decision & IR Metrics](Measured_Chunker_Decision_%26_IR_Metrics.md) (4 shared connections)
- [Server Lifecycle Tests](Server_Lifecycle_Tests.md) (3 shared connections)
- [Embeddings & Vector Width](Embeddings_%26_Vector_Width.md) (2 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (2 shared connections)
- [CLI Tests](CLI_Tests.md) (1 shared connections)
- [Conversational Evaluation Tests](Conversational_Evaluation_Tests.md) (1 shared connections)
- [Corpus Boundary Rules](Corpus_Boundary_Rules.md) (1 shared connections)
- [Reasoning-Model Hygiene](Reasoning-Model_Hygiene.md) (1 shared connections)
- [LLM-as-Judge Faithfulness](LLM-as-Judge_Faithfulness.md) (1 shared connections)
- [Anthropic Adapter](Anthropic_Adapter.md) (1 shared connections)

## Source Files

- `PROJECT_STATUS.md`
- `docs/engineering/architecture/chunking-and-embeddings.md`
- `docs/engineering/architecture/knowledge-corpus.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/decisions/0002-langchain-scope.md`
- `docs/engineering/technologies/langchain.md`

## Audit Trail

- EXTRACTED: 73 (80%)
- INFERRED: 16 (18%)
- AMBIGUOUS: 2 (2%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*