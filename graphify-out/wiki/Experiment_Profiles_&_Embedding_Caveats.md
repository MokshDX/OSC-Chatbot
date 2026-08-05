# Experiment Profiles & Embedding Caveats

> 12 nodes

## Key Concepts

- **local-only Experiment Profile** (4 connections) — `config/experiments/local-only.yaml`
- **The Five Protocol Seams** (3 connections) — `PROJECT_STATUS.md`
- **384-Dimension Database Separation** (2 connections) — `config/experiments/local-only.yaml`
- **Output Rules — stdout/stderr split and error hierarchy** (2 connections) — `AGENTS.md`
- **Vendor Agnosticism** (2 connections) — `PROJECT_STATUS.md`
- **StoreInspector — optional inspection protocol** (2 connections) — `PROJECT_STATUS.md`
- **Container — composition root and lifecycle** (2 connections) — `PROJECT_STATUS.md`
- **Registry wiring — providers as plug-in additions** (2 connections) — `PROJECT_STATUS.md`
- **Operator errors are messages; bugs are tracebacks** (2 connections) — `PROJECT_STATUS.md`
- **3072-Dimension Embedding Caveat** (1 connections) — `config/experiments/hosted-anthropic.yaml`
- **BGE Asymmetric Query Prefix** (1 connections) — `config/experiments/local-only.yaml`
- **cross_encoder Reranker (ms-marco-MiniLM-L-6-v2)** (1 connections) — `config/experiments/local-only.yaml`

## Relationships

- [Session Startup Checklist](Session_Startup_Checklist.md) (1 shared connections)
- [Operational Tooling (./osc CLI)](Operational_Tooling_%28.-osc_CLI%29.md) (1 shared connections)

## Source Files

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `config/experiments/hosted-anthropic.yaml`
- `config/experiments/local-only.yaml`

## Audit Trail

- EXTRACTED: 14 (58%)
- INFERRED: 10 (42%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*