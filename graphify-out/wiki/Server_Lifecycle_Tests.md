# Server Lifecycle Tests

> 28 nodes

## Key Concepts

- **ADR 0005 — An In-Repo Evaluation Harness, Not A Third-Party One** (10 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **ADR 0006 — Keep recursive As The Default Until Measured** (8 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **ADR 0007 — Corpus Root Is docs/company/; The FAQ Is Split By Topic** (7 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- **ADR 0001 — Five Protocols As The Swappability Seams** (5 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- **ADR 0002 — Adopt LangChain For Undifferentiated Work Only** (4 connections) — `docs/engineering/decisions/0002-langchain-scope.md`
- **Dependency Posture: Small Core, Vendor SDKs As Extras** (4 connections) — `docs/engineering/technologies/README.md`
- **documents Extra (pypdf, python-docx, openpyxl)** (4 connections) — `docs/engineering/technologies/python-tooling.md`
- **langchain-core And langchain-text-splitters Are Core Dependencies** (2 connections) — `docs/engineering/decisions/0002-langchain-scope.md`
- **Rejected: RAGAS** (2 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **A Retrieval Change Ships With A Measured Improvement** (2 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **The Open Chunker Comparison (Milestone A)** (2 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **openpyxl Added For .xlsx Scenario Workbooks** (2 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- **Shared Chunk Id Helper And Idempotent Ingestion** (2 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **--reindex Required After A Chunker Change** (2 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **Rejected: Abstract Base Classes And Framework Abstractions** (1 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- **Provider-Specific Tuning Lives In Untyped options** (1 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- **Rejected: A pytest Suite With Quality Assertions** (1 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **The Harness Drives The Real Pipelines** (1 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **The fact_match 1.0 Defect Found By Building It** (1 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **A Golden Set Is A Maintained Asset** (1 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **fixed Retained As An Evaluation Control** (1 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **Character-Based Rather Than Token-Based Sizing** (1 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **Semantic Chunking Deferred** (1 connections) — `docs/engineering/decisions/0006-chunking-strategy.md`
- **Rejected: An Ingest-Time Exclusion List** (1 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- **Rejected: Split At Question Level (89 Files)** (1 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- *... and 3 more nodes in this community*

## Relationships

- [Ingestion Tests](Ingestion_Tests.md) (3 shared connections)
- [LangChain Splitters](LangChain_Splitters.md) (2 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (2 shared connections)
- [Conversational Evaluation Tests](Conversational_Evaluation_Tests.md) (2 shared connections)
- [Corpus Boundary Rules](Corpus_Boundary_Rules.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/chunking-and-embeddings.md`
- `docs/engineering/decisions/0001-provider-abstraction.md`
- `docs/engineering/decisions/0002-langchain-scope.md`
- `docs/engineering/decisions/0005-evaluation-framework.md`
- `docs/engineering/decisions/0006-chunking-strategy.md`
- `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- `docs/engineering/technologies/README.md`
- `docs/engineering/technologies/python-tooling.md`

## Audit Trail

- EXTRACTED: 53 (76%)
- INFERRED: 17 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*