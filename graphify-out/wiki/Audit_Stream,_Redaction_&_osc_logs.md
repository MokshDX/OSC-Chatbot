# Audit Stream, Redaction & osc logs

> 20 nodes · cohesion 0.11

## Key Concepts

- **The Audit Stream** (4 connections) — `docs/engineering/architecture/logging.md`
- **Disk Bounded by Construction** (4 connections) — `docs/engineering/architecture/logging.md`
- **Diagnosis Workflow — doctor, traces, trace, search, chunk** (4 connections) — `README.md`
- **Corpus Text Reduced to a Length** (3 connections) — `docs/engineering/architecture/logging.md`
- **Redaction Filter and NEVER_REDACT** (3 connections) — `docs/engineering/architecture/logging.md`
- **The Failure Modes of a Logging System Are Silent** (3 connections) — `docs/engineering/decisions/0009-persistent-logging.md`
- **OSC Internal Knowledge Assistant** (3 connections) — `PROJECT_STATUS.md`
- **Idempotent Ingestion by Content Hash** (3 connections) — `README.md`
- **The ./osc Operator CLI** (3 connections) — `README.md`
- **./osc logs Is a Discovery Command, Not a Viewer** (2 connections) — `docs/engineering/architecture/logging.md`
- **QueueHandler.prepare() Strips exc_info** (2 connections) — `docs/engineering/decisions/0009-persistent-logging.md`
- **Size-Based Rotation, Not Time-Based** (2 connections) — `docs/engineering/decisions/0009-persistent-logging.md`
- **Relevance Scored at Document Level** (2 connections) — `PROJECT_STATUS.md`
- **fact_match Reported 1.0 for Work Never Done** (2 connections) — `PROJECT_STATUS.md`
- **Operator Errors Are Messages; Bugs Are Tracebacks** (2 connections) — `PROJECT_STATUS.md`
- **Text Extraction Is a Plain Dict of Functions** (2 connections) — `PROJECT_STATUS.md`
- **Unreadable Files Are Present, Not Deleted** (2 connections) — `PROJECT_STATUS.md`
- **observability.capture_text** (2 connections) — `README.md`
- **--reindex When the Chunker Changes** (2 connections) — `README.md`
- **Production Start-Up Guard** (1 connections) — `PROJECT_STATUS.md`

## Relationships

- [The Logging System & Span Bridge](The_Logging_System_%26_Span_Bridge.md) (4 shared connections)
- [Ponytail Discipline & Evaluation Framework](Ponytail_Discipline_%26_Evaluation_Framework.md) (3 shared connections)
- [Logging Documentation & ADR 0009](Logging_Documentation_%26_ADR_0009.md) (1 shared connections)
- [Experiment Profiles & Embedding Caveats](Experiment_Profiles_%26_Embedding_Caveats.md) (1 shared connections)
- [ADR 0009 Structure](ADR_0009_Structure.md) (1 shared connections)
- [Module Map & Dependency Rules](Module_Map_%26_Dependency_Rules.md) (1 shared connections)

## Source Files

- `PROJECT_STATUS.md`
- `README.md`
- `docs/engineering/architecture/logging.md`
- `docs/engineering/decisions/0009-persistent-logging.md`

## Audit Trail

- EXTRACTED: 39 (76%)
- INFERRED: 12 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*