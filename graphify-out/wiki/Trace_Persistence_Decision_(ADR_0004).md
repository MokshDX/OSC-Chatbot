# Trace Persistence Decision (ADR 0004)

> 7 nodes · cohesion 0.29

## Key Concepts

- **ADR 0004 — Persist Traces To A Bounded JSONL File** (5 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **Every Case Records Its Trace Id** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **Rejected: A traces Table In PostgreSQL** (2 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **One Database Is One Failure Domain** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Auto-Explain On Failure** (1 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **Bounded Means Lossy — Not An Audit Log** (1 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **OpenTelemetry Exporter Deferred, Span Stays OTel-Shaped** (1 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`

## Relationships

- [Evaluation Harness & CI Gate](Evaluation_Harness_%26_CI_Gate.md) (1 shared connections)
- [Retrieval Architecture & Metrics](Retrieval_Architecture_%26_Metrics.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/decisions/0004-persistent-tracing.md`
- `docs/engineering/technologies/postgresql-pgvector.md`

## Audit Trail

- EXTRACTED: 10 (71%)
- INFERRED: 4 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*