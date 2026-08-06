# Experiment Profiles & Embedding Caveats

> 12 nodes · cohesion 0.17

## Key Concepts

- **Vendor Agnosticism** (5 connections) — `PROJECT_STATUS.md`
- **local-only Experiment Profile** (4 connections) — `config/experiments/local-only.yaml`
- **Experiment Profiles** (3 connections) — `README.md`
- **384-Dimension Database Separation** (2 connections) — `config/experiments/local-only.yaml`
- **The cli.command Record** (2 connections) — `docs/engineering/architecture/logging.md`
- **Instrument the Pipeline, Not the Adapter** (2 connections) — `docs/engineering/architecture/observability.md`
- **Container — Composition Root and Lifecycle** (2 connections) — `PROJECT_STATUS.md`
- **Registry Wiring — Providers as Additions** (2 connections) — `PROJECT_STATUS.md`
- **Layered Configuration** (2 connections) — `README.md`
- **3072-Dimension Embedding Caveat** (1 connections) — `config/experiments/hosted-anthropic.yaml`
- **BGE Asymmetric Query Prefix** (1 connections) — `config/experiments/local-only.yaml`
- **cross_encoder Reranker (ms-marco-MiniLM-L-6-v2)** (1 connections) — `config/experiments/local-only.yaml`

## Relationships

- [Module Map & Dependency Rules](Module_Map_%26_Dependency_Rules.md) (2 shared connections)
- [Audit Stream, Redaction & osc logs](Audit_Stream%2C_Redaction_%26_osc_logs.md) (1 shared connections)
- [Engineering Handbook Rules](Engineering_Handbook_Rules.md) (1 shared connections)
- [Evaluation Harness & CI Gate](Evaluation_Harness_%26_CI_Gate.md) (1 shared connections)

## Source Files

- `PROJECT_STATUS.md`
- `README.md`
- `config/experiments/hosted-anthropic.yaml`
- `config/experiments/local-only.yaml`
- `docs/engineering/architecture/logging.md`
- `docs/engineering/architecture/observability.md`

## Audit Trail

- EXTRACTED: 18 (67%)
- INFERRED: 9 (33%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*