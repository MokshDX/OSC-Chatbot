# LangChain Chat Bridge

> 30 nodes

## Key Concepts

- **ADR 0011 — The Schema Corpus Is the Authoritative Knowledge Source** (9 connections) — `docs/engineering/decisions/0011-schema-first-knowledge-corpus.md`
- **ADR 0012 — markdown Becomes the Default Chunker, on a Measurement** (9 connections) — `docs/engineering/decisions/0012-markdown-chunking-measured.md`
- **Schema Golden Set Suite** (9 connections) — `evaluation/suites/schema.yaml`
- **Conversational Golden Set Suite** (8 connections) — `evaluation/suites/conversational.yaml`
- **ADR Process and Rules** (7 connections) — `docs/engineering/decisions/README.md`
- **Committed Baselines Directory** (7 connections) — `evaluation/baselines/README.md`
- **FAQ Golden Set Suite (preserved, not production)** (7 connections) — `evaluation/suites/faq.yaml`
- **Golden Set** (6 connections) — `docs/engineering/architecture/evaluation.md`
- **Document-Level Relevance Scoring** (6 connections) — `docs/engineering/architecture/evaluation.md`
- **ADR 0014 — Regression Tolerances Are Derived, Not Typed** (6 connections) — `docs/engineering/decisions/0014-derived-regression-tolerances.md`
- **ADR 0008 — Deduplicate by Source, Not by Content** (5 connections) — `docs/engineering/decisions/0008-content-level-deduplication.md`
- **The FAQ Baselines Are Historical** (5 connections) — `evaluation/baselines/README.md`
- **The OSCP Schema Corpus** (4 connections) — `docs/engineering/decisions/0011-schema-first-knowledge-corpus.md`
- **Evaluation CI Gate** (3 connections) — `docs/engineering/architecture/evaluation.md`
- **Byte-Identical Scenario Document Duplicate** (3 connections) — `docs/engineering/decisions/0008-content-level-deduplication.md`
- **Cold Control Run and follow_up_lift** (3 connections) — `evaluation/suites/conversational.yaml`
- **Rejected: Keep The FAQ As One File** (2 connections) — `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- **Abstention Cases in the Golden Set** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **Golden-Set Path Guard** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **LLM-as-Judge Faithfulness** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **Deterministic Metrics Gate CI** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **--reindex After a Chunker Change** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **Two Corpora, One Database, Partitioned by workspace_id** (2 connections) — `docs/engineering/decisions/0011-schema-first-knowledge-corpus.md`
- **The Gate Explains Itself** (2 connections) — `docs/engineering/decisions/0014-derived-regression-tolerances.md`
- **Conversational Turn Flags** (2 connections) — `evaluation/suites/conversational.yaml`
- *... and 5 more nodes in this community*

## Relationships

- [Conversational Evaluation Tests](Conversational_Evaluation_Tests.md) (7 shared connections)
- [Anthropic Adapter](Anthropic_Adapter.md) (5 shared connections)
- [Corpus Boundary Rules](Corpus_Boundary_Rules.md) (4 shared connections)
- [Server Lifecycle Tests](Server_Lifecycle_Tests.md) (2 shared connections)
- [Ingestion Tests](Ingestion_Tests.md) (2 shared connections)
- [LangChain Splitters](LangChain_Splitters.md) (1 shared connections)
- [Retrieval Metric Functions](Retrieval_Metric_Functions.md) (1 shared connections)
- [Embeddings & Vector Width](Embeddings_%26_Vector_Width.md) (1 shared connections)
- [Idempotency & Metric Honesty](Idempotency_%26_Metric_Honesty.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/overview.md`
- `docs/engineering/decisions/0007-knowledge-corpus-layout.md`
- `docs/engineering/decisions/0008-content-level-deduplication.md`
- `docs/engineering/decisions/0011-schema-first-knowledge-corpus.md`
- `docs/engineering/decisions/0012-markdown-chunking-measured.md`
- `docs/engineering/decisions/0013-ephemeral-session-memory.md`
- `docs/engineering/decisions/0014-derived-regression-tolerances.md`
- `docs/engineering/decisions/README.md`
- `evaluation/baselines/README.md`
- `evaluation/suites/conversational.yaml`
- `evaluation/suites/faq.yaml`
- `evaluation/suites/schema.yaml`

## Audit Trail

- EXTRACTED: 104 (87%)
- INFERRED: 16 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*