# Corpus Boundary & Golden Set Curation

> 28 nodes · cohesion 0.08

## Key Concepts

- **ADR 0005 — An In-Repo Evaluation Harness, Not A Third-Party One** (10 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **ADR 0007 — Corpus Root Is docs/company/; The FAQ Is Split By Topic** (9 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- **The Knowledge Corpus (docs/company/)** (7 connections) — `docs/engineering/architecture/knowledge-corpus.md`
- **Relevance Scored At Document Level** (5 connections) — `docs/engineering/architecture/evaluation.md`
- **Golden Set (86 cases)** (5 connections) — `docs/engineering/architecture/evaluation.md`
- **documents Extra (pypdf, python-docx, openpyxl)** (4 connections) — `docs/engineering/technologies/python-tooling.md`
- **Dependency Posture: Small Core, Vendor SDKs As Extras** (4 connections) — `docs/engineering/technologies/README.md`
- **Uniform Access Control, Directory As The Boundary** (3 connections) — `docs/engineering/architecture/knowledge-corpus.md`
- **Corpus Boundary Enforced At Index Time** (3 connections) — `docs/engineering/architecture/knowledge-corpus.md`
- **workspace_id On Every Table** (3 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Parsers Extract And Never Rewrite** (2 connections) — `docs/engineering/architecture/chunking-and-embeddings.md`
- **An Absent Metric Is Not A Zero Metric** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **workspace_id From Day One** (2 connections) — `docs/engineering/architecture/overview.md`
- **langchain-core And langchain-text-splitters Are Core Dependencies** (2 connections) — `docs/engineering/decisions/0002-langchain-scope.md`
- **The fact_match 1.0 Defect Found By Building It** (2 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **Rejected: RAGAS** (2 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **Rejected: An Ingest-Time Exclusion List** (2 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- **Rejected: Keep The FAQ As One File** (2 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- **openpyxl Added For .xlsx Scenario Workbooks** (2 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- **Abstention Cases In The Golden Set** (1 connections) — `docs/engineering/architecture/evaluation.md`
- **Golden-Set Path Guard Against The Index** (1 connections) — `docs/engineering/architecture/evaluation.md`
- **A Golden Set Is A Maintained Asset** (1 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **Rejected: A pytest Suite With Quality Assertions** (1 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **The Harness Drives The Real Pipelines** (1 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **The Corpus Root Is Named In Two Places** (1 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- *... and 3 more nodes in this community*

## Relationships

- [Chunking & Embedding Architecture](Chunking_%26_Embedding_Architecture.md) (5 shared connections)
- [Evaluation Harness & CI Gate](Evaluation_Harness_%26_CI_Gate.md) (5 shared connections)
- [Module Map & Dependency Rules](Module_Map_%26_Dependency_Rules.md) (3 shared connections)
- [Graphify Graph Findings](Graphify_Graph_Findings.md) (2 shared connections)
- [Architecture Overview & Weak Points](Architecture_Overview_%26_Weak_Points.md) (2 shared connections)
- [Retrieval Architecture & Metrics](Retrieval_Architecture_%26_Metrics.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/chunking-and-embeddings.md`
- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/knowledge-corpus.md`
- `docs/engineering/architecture/overview.md`
- `docs/engineering/decisions/0002-langchain-scope.md`
- `docs/engineering/decisions/0005-evaluation-framework.md`
- `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- `docs/engineering/technologies/README.md`
- `docs/engineering/technologies/postgresql-pgvector.md`
- `docs/engineering/technologies/python-tooling.md`

## Audit Trail

- EXTRACTED: 50 (62%)
- INFERRED: 30 (38%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*