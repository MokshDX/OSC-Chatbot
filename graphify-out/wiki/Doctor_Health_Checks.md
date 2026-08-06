# Doctor Health Checks

> 18 nodes · cohesion 0.24

## Key Concepts

- **diagnose.py** (53 connections) — `src/osc_assistant/cli/diagnose.py`
- **Settings** (36 connections) — `src/osc_assistant/settings.py`
- **_run_checks()** (12 connections) — `src/osc_assistant/cli/diagnose.py`
- **Check** (10 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_llm()** (7 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_chunker()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_langchain()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_reranker()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_store()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_corpus()** (4 connections) — `src/osc_assistant/cli/diagnose.py`
- **Path** (4 connections)
- **.traces_are_exposed()** (2 connections) — `src/osc_assistant/settings.py`
- **.marker()** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Diagnostics and inspection: understanding the system without reading its…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Report the LangChain versions in play. Both are core dependencies.** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **One diagnostic result. `status` is deliberately three-valued. A warning is a…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Root configuration object. Nested values are addressable from the environment…** (1 connections) — `src/osc_assistant/settings.py`
- **Whether the HTTP trace endpoints should be registered. Two conditions, not one.…** (1 connections) — `src/osc_assistant/settings.py`

## Relationships

- [Diagnostic CLI Commands](Diagnostic_CLI_Commands.md) (14 shared connections)
- [Container Lifecycle & E2E](Container_Lifecycle_%26_E2E.md) (9 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (7 shared connections)
- [Trace Listing CLI](Trace_Listing_CLI.md) (6 shared connections)
- [Settings Sources & Tests](Settings_Sources_%26_Tests.md) (5 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (4 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (4 shared connections)
- [Inspection Payloads & Redaction](Inspection_Payloads_%26_Redaction.md) (3 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (3 shared connections)
- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (3 shared connections)
- [Startup Banner & Lifecycle](Startup_Banner_%26_Lifecycle.md) (3 shared connections)
- [CLI Core Commands](CLI_Core_Commands.md) (2 shared connections)

## Source Files

- `src/osc_assistant/cli/diagnose.py`
- `src/osc_assistant/settings.py`

## Audit Trail

- EXTRACTED: 149 (97%)
- INFERRED: 5 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*