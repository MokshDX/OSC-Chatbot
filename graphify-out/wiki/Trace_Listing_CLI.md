# Trace Listing CLI

> 9 nodes · cohesion 0.25

## Key Concepts

- **StoreInspector** (21 connections) — `src/osc_assistant/protocols.py`
- **traces()** (10 connections) — `src/osc_assistant/cli/diagnose.py`
- **_traces_from()** (7 connections) — `src/osc_assistant/cli/diagnose.py`
- **fail()** (7 connections) — `src/osc_assistant/cli/_shared.py`
- **_fetch_traces()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **_inspector()** (4 connections) — `src/osc_assistant/cli/diagnose.py`
- **List recent execution traces, most recent first. Read from the persisted trace…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Report an operator-facing error and exit non-zero.** (1 connections) — `src/osc_assistant/cli/_shared.py`
- **Read-only introspection of what a store currently holds. Kept **separate from…** (1 connections) — `src/osc_assistant/protocols.py`

## Relationships

- [Diagnostic CLI Commands](Diagnostic_CLI_Commands.md) (7 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (6 shared connections)
- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (3 shared connections)
- [VectorStore Errors & Inspection](VectorStore_Errors_%26_Inspection.md) (3 shared connections)
- [Trace Sink & JSONL Parsing](Trace_Sink_%26_JSONL_Parsing.md) (2 shared connections)
- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (2 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (2 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (2 shared connections)
- [Container Lifecycle & E2E](Container_Lifecycle_%26_E2E.md) (1 shared connections)
- [Observability Entry & Trace Rendering](Observability_Entry_%26_Trace_Rendering.md) (1 shared connections)
- [Trace Configuration & CLI Trace](Trace_Configuration_%26_CLI_Trace.md) (1 shared connections)
- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/_shared.py`
- `src/osc_assistant/cli/diagnose.py`
- `src/osc_assistant/protocols.py`

## Audit Trail

- EXTRACTED: 49 (86%)
- INFERRED: 8 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*