# Technologies

Every page here answers the same seven questions, so they can be read in any order and
compared against each other:

1. **What it is** — with authoritative references
2. **Why OSC uses it**
3. **Where it is used** — the actual modules
4. **How it integrates**
5. **Alternatives considered**
6. **Trade-offs accepted** — the costs, stated
7. **Future evolution**

| Page | Covers |
|---|---|
| [postgresql-pgvector.md](postgresql-pgvector.md) | The single datastore: chunk text, embeddings, lexical index, metadata. HNSW, `tsvector`, SQL-side RRF fusion |
| [ollama.md](ollama.md) | The local model runtime. `qwen3:8b`, `nomic-embed-text`, and the honest costs of a local stack |
| [langchain.md](langchain.md) | What was adopted, what was refused, and the rule that decided — including the reversal of an earlier rejection |
| [fastapi.md](fastapi.md) | The HTTP layer, SSE streaming, lifespan-owned container, the stdout/stderr split |
| [python-tooling.md](python-tooling.md) | Pydantic, Typer, Rich, ruff, `mypy --strict`, pytest, hatchling — and why the strict typecheck is load-bearing architecture |
| [graphify-and-ponytail.md](graphify-and-ponytail.md) | The two development-time tools. Neither ships; both shape the codebase |

## The dependency posture, in one paragraph

The core runtime is deliberately small — `pydantic`, `pydantic-settings`, `fastapi`,
`uvicorn`, `asyncpg`, `httpx`, `pyyaml`, `typer`, `rich`, `langchain-core`,
`langchain-text-splitters`. Everything vendor-specific is an **extra**, so a deployment
installs only the SDKs for the providers it actually configures. The two LangChain
packages are core rather than extras because both are pure Python with no vendor SDK
behind them and both must be importable for the registries to be complete.

## Before adding a dependency

Read the ladder in [graphify-and-ponytail.md](graphify-and-ponytail.md#what-it-is-1),
then answer three questions in the pull request:

1. What does it do that the standard library or an already-installed dependency does
   not?
2. Is it maintained, and by whom?
3. Is it core, or is it an extra? (Default: extra.)

`logging.py` is a JSON formatter on stdlib `logging` rather than a logging framework —
thirty lines against a dependency that is forever. That is the standard to argue
against.
