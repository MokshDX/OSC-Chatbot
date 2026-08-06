# Architecture Overview & Weak Points

> 20 nodes · cohesion 0.11

## Key Concepts

- **Pydantic At Every Trust Boundary, And Nowhere Else** (13 connections) — `docs/engineering/technologies/python-tooling.md`
- **FastAPI** (9 connections) — `docs/engineering/technologies/fastapi.md`
- **The Seven-Question Technology Page Format** (7 connections) — `docs/engineering/technologies/README.md`
- **No Authentication, Rate Limiting Or Concurrency Bound** (4 connections) — `docs/engineering/technologies/fastapi.md`
- **Where The Architecture Is Weakest** (3 connections) — `docs/engineering/architecture/overview.md`
- **Never Let A Vendor Exception Escape An Adapter** (3 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Frozen Dataclasses For Domain Types** (2 connections) — `docs/engineering/architecture/overview.md`
- **Operator Errors Are Messages; Bugs Are Tracebacks** (2 connections) — `docs/engineering/architecture/overview.md`
- **Query Rewriting (off by default)** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **There Is No Write Endpoint** (2 connections) — `docs/engineering/technologies/fastapi.md`
- **asyncpg Errors Translated To VectorStoreError** (2 connections) — `docs/engineering/technologies/postgresql-pgvector.md`
- **response_model=None On /chat** (1 connections) — `docs/engineering/technologies/fastapi.md`
- **Server-Sent Events Rather Than WebSockets** (1 connections) — `docs/engineering/technologies/fastapi.md`
- **Every SSE Exit Path Emits A Terminal Event** (1 connections) — `docs/engineering/technologies/fastapi.md`
- **Flat Command Surface With Three --help Panels** (1 connections) — `docs/engineering/technologies/python-tooling.md`
- **hatchling Build Backend** (1 connections) — `docs/engineering/technologies/python-tooling.md`
- **The ./osc Wrapper Script** (1 connections) — `docs/engineering/technologies/python-tooling.md`
- **pytest With asyncio_mode = auto** (1 connections) — `docs/engineering/technologies/python-tooling.md`
- **ruff** (1 connections) — `docs/engineering/technologies/python-tooling.md`
- **Typer And Rich CLI** (1 connections) — `docs/engineering/technologies/python-tooling.md`

## Relationships

- [Module Map & Dependency Rules](Module_Map_%26_Dependency_Rules.md) (4 shared connections)
- [Evaluation Harness & CI Gate](Evaluation_Harness_%26_CI_Gate.md) (3 shared connections)
- [Retrieval Architecture & Metrics](Retrieval_Architecture_%26_Metrics.md) (3 shared connections)
- [Chunk Size & Vector Dimension Decisions](Chunk_Size_%26_Vector_Dimension_Decisions.md) (2 shared connections)
- [Corpus Boundary & Golden Set Curation](Corpus_Boundary_%26_Golden_Set_Curation.md) (2 shared connections)
- [Graphify Graph Findings](Graphify_Graph_Findings.md) (1 shared connections)
- [Ponytail Discipline & Evaluation Framework](Ponytail_Discipline_%26_Evaluation_Framework.md) (1 shared connections)

## Source Files

- `docs/engineering/architecture/overview.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/technologies/README.md`
- `docs/engineering/technologies/fastapi.md`
- `docs/engineering/technologies/postgresql-pgvector.md`
- `docs/engineering/technologies/python-tooling.md`

## Audit Trail

- EXTRACTED: 48 (83%)
- INFERRED: 8 (14%)
- AMBIGUOUS: 2 (3%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*