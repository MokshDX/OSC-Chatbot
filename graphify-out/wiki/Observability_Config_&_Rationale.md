# Observability Config & Rationale

> 7 nodes · cohesion 0.43

## Key Concepts

- **Observability Subsystem** (8 connections) — `docs/engineering/architecture/observability.md`
- **store.py (append-only JSONL trace log)** (4 connections) — `docs/engineering/architecture/observability.md`
- **observability: configuration block** (3 connections) — `config/default.yaml`
- **capture_text Privacy Seam** (2 connections) — `docs/engineering/architecture/observability.md`
- **render.py (waterfall renderer)** (2 connections) — `docs/engineering/architecture/observability.md`
- **trace.py (context-var span tree)** (2 connections) — `docs/engineering/architecture/observability.md`
- **Why a JSONL File (alternatives rejected)** (1 connections) — `docs/engineering/architecture/observability.md`

## Relationships

- [Default Configuration Profile](Default_Configuration_Profile.md) (1 shared connections)
- [Session Startup & Deduplication (ADR 0008)](Session_Startup_%26_Deduplication_%28ADR_0008%29.md) (1 shared connections)
- [Engineering Handbook Rules](Engineering_Handbook_Rules.md) (1 shared connections)
- [Ponytail Discipline & Evaluation Framework](Ponytail_Discipline_%26_Evaluation_Framework.md) (1 shared connections)

## Source Files

- `config/default.yaml`
- `docs/engineering/architecture/observability.md`

## Audit Trail

- EXTRACTED: 22 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*