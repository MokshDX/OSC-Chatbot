# CLI Shared Plumbing

> 13 nodes

## Key Concepts

- **_shared.py** (15 connections) — `src/osc_assistant/cli/_shared.py`
- **run()** (3 connections) — `src/osc_assistant/cli/_shared.py`
- **T** (2 connections)
- **table()** (2 connections) — `src/osc_assistant/cli/_shared.py`
- **fail()** (2 connections) — `src/osc_assistant/cli/_shared.py`
- **print_trace()** (2 connections) — `src/osc_assistant/cli/_shared.py`
- **traced_command()** (2 connections) — `src/osc_assistant/cli/_shared.py`
- **Any** (1 connections)
- **Plumbing shared by the CLI command modules. Kept separate so `core` and…** (1 connections) — `src/osc_assistant/cli/_shared.py`
- **A table styled consistently across every command.** (1 connections) — `src/osc_assistant/cli/_shared.py`
- **Report an operator-facing error and exit non-zero.** (1 connections) — `src/osc_assistant/cli/_shared.py`
- **Render the trace the command just produced, if one was asked for.** (1 connections) — `src/osc_assistant/cli/_shared.py`
- **Report a failed command usefully instead of as a stack trace. Two things happen…** (1 connections) — `src/osc_assistant/cli/_shared.py`

## Relationships

- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (2 shared connections)
- [CLI Settings Bootstrap](CLI_Settings_Bootstrap.md) (2 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (1 shared connections)
- [Core CLI Commands](Core_CLI_Commands.md) (1 shared connections)
- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (1 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (1 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (1 shared connections)
- [In-Memory Session Store](In-Memory_Session_Store.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/_shared.py`

## Audit Trail

- EXTRACTED: 34 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*