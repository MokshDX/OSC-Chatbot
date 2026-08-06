# The Logging System & Span Bridge

> 11 nodes · cohesion 0.25

## Key Concepts

- **The Logging System** (7 connections) — `docs/engineering/architecture/logging.md`
- **The Span Bridge** (6 connections) — `docs/engineering/architecture/logging.md`
- **Observability Layer — trace, store, render** (6 connections) — `PROJECT_STATUS.md`
- **Bounded Append-Only JSONL Trace Store** (5 connections) — `PROJECT_STATUS.md`
- **Logging and Tracing Answer Different Questions** (3 connections) — `docs/engineering/architecture/logging.md`
- **Writing Is Off the Calling Thread** (2 connections) — `docs/engineering/architecture/logging.md`
- **trace_id Stamped on Every Log Record** (2 connections) — `docs/engineering/architecture/logging.md`
- **Rejected — Replace the Trace Store With Logs** (2 connections) — `docs/engineering/decisions/0009-persistent-logging.md`
- **Instrument the Pipeline, Not the Adapter** (2 connections) — `PROJECT_STATUS.md`
- **TRACE Level (5)** (1 connections) — `docs/engineering/architecture/logging.md`
- **Rejected — Hand-Written Log Lines in Every Pipeline** (1 connections) — `docs/engineering/decisions/0009-persistent-logging.md`

## Relationships

- [Audit Stream, Redaction & osc logs](Audit_Stream%2C_Redaction_%26_osc_logs.md) (4 shared connections)
- [ADR 0009 Structure](ADR_0009_Structure.md) (2 shared connections)
- [Ponytail Discipline & Evaluation Framework](Ponytail_Discipline_%26_Evaluation_Framework.md) (2 shared connections)
- [Module Map & Dependency Rules](Module_Map_%26_Dependency_Rules.md) (1 shared connections)

## Source Files

- `PROJECT_STATUS.md`
- `docs/engineering/architecture/logging.md`
- `docs/engineering/decisions/0009-persistent-logging.md`

## Audit Trail

- EXTRACTED: 37 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*