# Evaluation Metrics & CI Gate

> 23 nodes

## Key Concepts

- **Evaluation Harness** (27 connections) — `docs/engineering/architecture/evaluation.md`
- **OSC Architecture Overview** (15 connections) — `docs/engineering/architecture/overview.md`
- **Six-Stage Retrieval Pipeline** (13 connections) — `docs/engineering/architecture/retrieval.md`
- **Citation Strength Differs By Provider, Silently** (4 connections) — `docs/engineering/architecture/overview.md`
- **CI Gate via --fail-under** (3 connections) — `docs/engineering/architecture/evaluation.md`
- **Committed Baselines** (3 connections) — `docs/engineering/architecture/evaluation.md`
- **The Request Path (rewrite → search → threshold → rerank → generate → cite)** (3 connections) — `docs/engineering/architecture/overview.md`
- **Abstention Is A Code Path, Not A Prompt Instruction** (3 connections) — `docs/engineering/architecture/overview.md`
- **Frozen Prompts** (3 connections) — `docs/engineering/architecture/overview.md`
- **recall@k** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **groundedness** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **abstention_accuracy** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **Configuration Travels With The Numbers** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **An Absent Metric Is Not A Zero Metric** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **The Five-Step Debugging Workflow** (2 connections) — `docs/engineering/architecture/observability.md`
- **Measured Retrieval Baseline (recall@5 0.932)** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **A Test Asserts A Behaviour, Not An Implementation** (2 connections) — `docs/engineering/architecture/testing.md`
- **The fact_match 1.0 Defect Found By Building It** (2 connections) — `docs/engineering/decisions/0005-evaluation-framework.md`
- **Citations Are Asserted, Not Verified** (2 connections) — `docs/engineering/technologies/ollama.md`
- **precision@k** (1 connections) — `docs/engineering/architecture/evaluation.md`
- **mrr** (1 connections) — `docs/engineering/architecture/evaluation.md`
- **hit_rate@k** (1 connections) — `docs/engineering/architecture/evaluation.md`
- **citation_coverage / citation_precision** (1 connections) — `docs/engineering/architecture/evaluation.md`

## Relationships

- [ADRs — Protocol & LangChain Decisions](ADRs_%E2%80%94_Protocol_%26_LangChain_Decisions.md) (6 shared connections)
- [Chunking Strategies & Ingestion Rules](Chunking_Strategies_%26_Ingestion_Rules.md) (5 shared connections)
- [The Five Protocol Seams](The_Five_Protocol_Seams.md) (5 shared connections)
- [Embedding & Chunk-Size Decisions](Embedding_%26_Chunk-Size_Decisions.md) (4 shared connections)
- [Hybrid Retrieval & RRF (ADR 0003)](Hybrid_Retrieval_%26_RRF_%28ADR_0003%29.md) (4 shared connections)
- [Observability & API Weak Points](Observability_%26_API_Weak_Points.md) (4 shared connections)
- [Persistent Tracing Design (ADR 0004)](Persistent_Tracing_Design_%28ADR_0004%29.md) (3 shared connections)
- [Four Test Tiers](Four_Test_Tiers.md) (3 shared connections)
- [Golden Set & Config Layering](Golden_Set_%26_Config_Layering.md) (2 shared connections)
- [ADR 0007 — Corpus Root Is docs/company/; The FAQ Is Split...](ADR_0007_%E2%80%94_Corpus_Root_Is_docs-company-%3B_The_FAQ_Is_Split.md) (2 shared connections)

## Source Files

- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/observability.md`
- `docs/engineering/architecture/overview.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/architecture/testing.md`
- `docs/engineering/decisions/0005-evaluation-framework.md`
- `docs/engineering/technologies/ollama.md`

## Audit Trail

- EXTRACTED: 82 (84%)
- INFERRED: 16 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*