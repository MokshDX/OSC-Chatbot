# ADRs — Protocol & LangChain Decisions

> 27 nodes

## Key Concepts

- **OSC Engineering Knowledge Base** (24 connections) — `docs/engineering/README.md`
- **ADR 0005 — An In-Repo Evaluation Harness, Not A Third-Party One** (12 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **ADR 0001 — Five Protocols As The Swappability Seams** (11 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- **Architecture Decision Records** (11 connections) — `docs/engineering/decisions/README.md`
- **Ponytail** (10 connections) — `docs/engineering/technologies/graphify-and-ponytail.md`
- **ADR 0002 — Adopt LangChain For Undifferentiated Work Only** (9 connections) — `docs/engineering/decisions/0002-langchain-scope.md`
- **Dependency Posture: Small Core, Vendor SDKs As Extras** (5 connections) — `docs/engineering/technologies/README.md`
- **The Ponytail Ladder** (5 connections) — `docs/engineering/technologies/graphify-and-ponytail.md`
- **Structured Logging On stdlib logging** (4 connections) — `docs/engineering/architecture/observability.md`
- **documents Extra (pypdf, python-docx, openpyxl)** (4 connections) — `docs/engineering/technologies/python-tooling.md`
- **Parsers Extract And Never Rewrite** (3 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **LLM-As-Judge Faithfulness (opt-in)** (3 connections) — `docs/engineering/architecture/evaluation.md`
- **Three Rules For Keeping Documentation Accurate** (2 connections) — `docs/engineering/README.md`
- **Machine Output On stdout, Human Output On stderr** (2 connections) — `docs/engineering/architecture/observability.md`
- **langchain-core And langchain-text-splitters Are Core Dependencies** (2 connections) — `docs/engineering/decisions/0002-langchain-scope.md`
- **Rejected: RAGAS** (2 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **Rejected: A pytest Suite With Quality Assertions** (2 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **openpyxl Added For .xlsx Scenario Workbooks** (2 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- **ADRs Are Append-Only** (2 connections) — `docs/engineering/decisions/README.md`
- **Three Questions Before Adding A Dependency** (2 connections) — `docs/engineering/technologies/README.md`
- **Flat Command Surface With Three --help Panels** (2 connections) — `docs/engineering/technologies/python-tooling.md`
- **Zheng et al., Judging LLM-as-a-Judge (NeurIPS 2023)** (1 connections) — `docs/engineering/architecture/evaluation.md`
- **Rejected: Abstract Base Classes And Framework Abstractions** (1 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- **Provider-Specific Tuning Lives In Untyped options** (1 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- **The Harness Drives The Real Pipelines** (1 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- *... and 2 more nodes in this community*

## Relationships

- [The Five Protocol Seams](The_Five_Protocol_Seams.md) (9 shared connections)
- [Chunking Strategies & Ingestion Rules](Chunking_Strategies_%26_Ingestion_Rules.md) (7 shared connections)
- [Persistent Tracing Design (ADR 0004)](Persistent_Tracing_Design_%28ADR_0004%29.md) (7 shared connections)
- [Evaluation Metrics & CI Gate](Evaluation_Metrics_%26_CI_Gate.md) (6 shared connections)
- [ADR 0007 — Corpus Root Is docs/company/; The FAQ Is Split...](ADR_0007_%E2%80%94_Corpus_Root_Is_docs-company-%3B_The_FAQ_Is_Split.md) (5 shared connections)
- [Observability & API Weak Points](Observability_%26_API_Weak_Points.md) (5 shared connections)
- [Golden Set & Config Layering](Golden_Set_%26_Config_Layering.md) (4 shared connections)
- [Hybrid Retrieval & RRF (ADR 0003)](Hybrid_Retrieval_%26_RRF_%28ADR_0003%29.md) (3 shared connections)
- [Four Test Tiers](Four_Test_Tiers.md) (2 shared connections)
- [Embedding & Chunk-Size Decisions](Embedding_%26_Chunk-Size_Decisions.md) (1 shared connections)

## Source Files

- `docs/engineering/README.md`
- `docs/engineering/architecture/chunking-and-embeddings.md`
- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/observability.md`
- `docs/engineering/decisions/0001-provider-abstraction.md`
- `docs/engineering/decisions/0002-langchain-scope.md`
- `docs/engineering/decisions/0005-evaluation-framework.md`
- `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- `docs/engineering/decisions/README.md`
- `docs/engineering/technologies/README.md`
- `docs/engineering/technologies/graphify-and-ponytail.md`
- `docs/engineering/technologies/python-tooling.md`

## Audit Trail

- EXTRACTED: 101 (81%)
- INFERRED: 24 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*