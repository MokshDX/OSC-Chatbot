# Persistent Tracing Design (ADR 0004)

> 15 nodes

## Key Concepts

- **One Request, One Persistent Trace** (13 connections) — `docs/engineering/architecture/observability.md`
- **ADR 0004 — Persist Traces To A Bounded JSONL File** (10 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **store.py — Bounded Append-Only JSONL Log** (9 connections) — `docs/engineering/architecture/observability.md`
- **trace.py — Context-Var Span Tree** (5 connections) — `docs/engineering/architecture/observability.md`
- **render.py — Waterfall Renderer** (4 connections) — `docs/engineering/architecture/observability.md`
- **One Database Is One Failure Domain** (4 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **Every Case Records Its Trace Id** (3 connections) — `docs/engineering/architecture/evaluation.md`
- **HTTP Trace Endpoints Gated On development** (3 connections) — `docs/engineering/architecture/observability.md`
- **Traces Are Process-Local And Lossy** (3 connections) — `docs/engineering/architecture/observability.md`
- **Rejected: A traces Table In PostgreSQL** (3 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **set_text As The Redaction Seam** (2 connections) — `docs/engineering/architecture/observability.md`
- **OpenTelemetry Exporter Deferred, Span Stays OTel-Shaped** (2 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **The ponytail: Comment Convention** (2 connections) — `docs/engineering/technologies/graphify-and-ponytail.md`
- **Auto-Explain On Failure** (1 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`
- **Bounded Means Lossy — Not An Audit Log** (1 connections) — `docs/engineering/decisions/0004-persistent-tracing.md`

## Relationships

- [ADRs — Protocol & LangChain Decisions](ADRs_%E2%80%94_Protocol_%26_LangChain_Decisions.md) (7 shared connections)
- [Evaluation Metrics & CI Gate](Evaluation_Metrics_%26_CI_Gate.md) (3 shared connections)
- [Observability & API Weak Points](Observability_%26_API_Weak_Points.md) (2 shared connections)
- [The Five Protocol Seams](The_Five_Protocol_Seams.md) (1 shared connections)
- [Chunking Strategies & Ingestion Rules](Chunking_Strategies_%26_Ingestion_Rules.md) (1 shared connections)
- [Four Test Tiers](Four_Test_Tiers.md) (1 shared connections)
- [Golden Set & Config Layering](Golden_Set_%26_Config_Layering.md) (1 shared connections)
- [Hybrid Retrieval & RRF (ADR 0003)](Hybrid_Retrieval_%26_RRF_%28ADR_0003%29.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/observability.md`
- `docs/engineering/decisions/0004-persistent-tracing.md`
- `docs/engineering/technologies/graphify-and-ponytail.md`
- `docs/engineering/technologies/postgresql-pgvector.md`

## Audit Trail

- EXTRACTED: 47 (72%)
- INFERRED: 18 (28%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*