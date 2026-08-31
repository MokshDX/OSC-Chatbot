# Core CLI Commands

> 24 nodes

## Key Concepts

- **core.py** (12 connections) — `src/osc_assistant/cli/core.py`
- **ingest()** (10 connections) — `src/osc_assistant/cli/core.py`
- **ask()** (9 connections) — `src/osc_assistant/cli/core.py`
- **search()** (9 connections) — `src/osc_assistant/cli/core.py`
- **serve()** (7 connections) — `src/osc_assistant/cli/core.py`
- **cli/__init__.py** (4 connections) — `src/osc_assistant/cli/__init__.py`
- **command** (4 connections)
- **ProfileOption** (4 connections)
- **help** (4 connections)
- **Argument** (3 connections)
- **ExplainOption** (3 connections)
- **VerboseOption** (3 connections)
- **Option** (2 connections)
- **JsonOption** (2 connections)
- **_print_answer()** (2 connections) — `src/osc_assistant/cli/core.py`
- **Answer** (2 connections)
- **_answer_payload()** (2 connections) — `src/osc_assistant/cli/core.py`
- **Command line interface. Split across three modules by what a command is *for*,…** (1 connections) — `src/osc_assistant/cli/__init__.py`
- **Path** (1 connections)
- **The commands that do work: serve, ingest, ask, search. Ingestion and ad-hoc…** (1 connections) — `src/osc_assistant/cli/core.py`
- **Run the HTTP service and chat UI.** (1 connections) — `src/osc_assistant/cli/core.py`
- **Index a directory of documents.** (1 connections) — `src/osc_assistant/cli/core.py`
- **Ask a question and print the grounded answer.** (1 connections) — `src/osc_assistant/cli/core.py`
- **Run retrieval only, without generating an answer. The first place to look when…** (1 connections) — `src/osc_assistant/cli/core.py`

## Relationships

- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (1 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (1 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (1 shared connections)
- [CLI Shared Plumbing](CLI_Shared_Plumbing.md) (1 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (1 shared connections)
- [RRF Fusion & Citation Parsing](RRF_Fusion_%26_Citation_Parsing.md) (1 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/__init__.py`
- `src/osc_assistant/cli/core.py`

## Audit Trail

- EXTRACTED: 88 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*