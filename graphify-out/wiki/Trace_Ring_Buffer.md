# Trace Ring Buffer

> 8 nodes

## Key Concepts

- **TraceRecorder** (9 connections) — `src/osc_assistant/observability/trace.py`
- **.record()** (2 connections) — `src/osc_assistant/observability/trace.py`
- **.recent()** (2 connections) — `src/osc_assistant/observability/trace.py`
- **.__init__()** (1 connections) — `src/osc_assistant/observability/trace.py`
- **.resize()** (1 connections) — `src/osc_assistant/observability/trace.py`
- **.clear()** (1 connections) — `src/osc_assistant/observability/trace.py`
- **.__len__()** (1 connections) — `src/osc_assistant/observability/trace.py`
- **A bounded ring of recent traces, for `osc-assistant trace` and `/api/traces`.…** (1 connections) — `src/osc_assistant/observability/trace.py`

## Relationships

- [Doctor Health Checks](Doctor_Health_Checks.md) (4 shared connections)

## Source Files

- `src/osc_assistant/observability/trace.py`

## Audit Trail

- EXTRACTED: 18 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*