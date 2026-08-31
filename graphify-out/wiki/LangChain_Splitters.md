# LangChain Splitters

> 22 nodes

## Key Concepts

- **Pydantic At Every Trust Boundary, And Nowhere Else** (12 connections) — `docs/engineering/technologies/python-tooling.md`
- **FastAPI** (9 connections) — `docs/engineering/technologies/fastapi.md`
- **Lazy cached_property Container Construction** (3 connections) — `docs/engineering/architecture/provider-architecture.md`
- **mypy --strict As Load-Bearing Architecture** (3 connections) — `docs/engineering/technologies/python-tooling.md`
- **Layered Configuration (env > .env > YAML profile)** (3 connections) — `README.md`
- **Protocols Rather Than Abstract Base Classes** (2 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Protocols Are Enforced Only Statically** (2 connections) — `docs/engineering/decisions/0001-provider-abstraction.md`
- **Lifespan Owns The Container** (2 connections) — `docs/engineering/technologies/fastapi.md`
- **There Is No Write Endpoint** (2 connections) — `docs/engineering/technologies/fastapi.md`
- **No Authentication, Rate Limiting Or Concurrency Bound** (2 connections) — `docs/engineering/technologies/fastapi.md`
- **Four-Layer Settings Precedence** (2 connections) — `docs/engineering/technologies/python-tooling.md`
- **PEP 544 — Structural Subtyping** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Registry And Composition Root Wiring** (1 connections) — `docs/engineering/architecture/provider-architecture.md`
- **Server-Sent Events Rather Than WebSockets** (1 connections) — `docs/engineering/technologies/fastapi.md`
- **Every SSE Exit Path Emits A Terminal Event** (1 connections) — `docs/engineering/technologies/fastapi.md`
- **response_model=None On /chat** (1 connections) — `docs/engineering/technologies/fastapi.md`
- **Typer And Rich CLI** (1 connections) — `docs/engineering/technologies/python-tooling.md`
- **Flat Command Surface With Three --help Panels** (1 connections) — `docs/engineering/technologies/python-tooling.md`
- **ruff** (1 connections) — `docs/engineering/technologies/python-tooling.md`
- **pytest With asyncio_mode = auto** (1 connections) — `docs/engineering/technologies/python-tooling.md`
- **hatchling Build Backend** (1 connections) — `docs/engineering/technologies/python-tooling.md`
- **The ./osc Wrapper Script** (1 connections) — `docs/engineering/technologies/python-tooling.md`

## Relationships

- [Server Lifecycle Tests](Server_Lifecycle_Tests.md) (2 shared connections)
- [Reasoning-Model Hygiene](Reasoning-Model_Hygiene.md) (2 shared connections)
- [Embeddings & Vector Width](Embeddings_%26_Vector_Width.md) (1 shared connections)
- [Retrieval Metric Functions](Retrieval_Metric_Functions.md) (1 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (1 shared connections)
- [CLI Tests](CLI_Tests.md) (1 shared connections)
- [Core Architecture Decisions](Core_Architecture_Decisions.md) (1 shared connections)

## Source Files

- `README.md`
- `docs/engineering/architecture/provider-architecture.md`
- `docs/engineering/decisions/0001-provider-abstraction.md`
- `docs/engineering/technologies/fastapi.md`
- `docs/engineering/technologies/python-tooling.md`

## Audit Trail

- EXTRACTED: 45 (85%)
- INFERRED: 8 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*