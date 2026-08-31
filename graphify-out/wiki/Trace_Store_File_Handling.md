# Trace Store File Handling

> 12 nodes

## Key Concepts

- **TraceStore** (18 connections) — `src/osc_assistant/observability/store.py`
- **.append()** (5 connections) — `src/osc_assistant/observability/store.py`
- **.recent()** (5 connections) — `src/osc_assistant/observability/store.py`
- **Path** (3 connections)
- **.__init__()** (2 connections) — `src/osc_assistant/observability/store.py`
- **.path()** (2 connections) — `src/osc_assistant/observability/store.py`
- **.rotated_path()** (2 connections) — `src/osc_assistant/observability/store.py`
- **._rotate_if_needed()** (2 connections) — `src/osc_assistant/observability/store.py`
- **.clear()** (1 connections) — `src/osc_assistant/observability/store.py`
- **A size-bounded, append-only log of completed traces. Two files: the one being…** (1 connections) — `src/osc_assistant/observability/store.py`
- **Record one completed trace. Never raises. A read-only filesystem, a full disk…** (1 connections) — `src/osc_assistant/observability/store.py`
- **Completed traces, most recent first.** (1 connections) — `src/osc_assistant/observability/store.py`

## Relationships

- [Doctor Health Checks](Doctor_Health_Checks.md) (9 shared connections)
- [Answerer & Abstention Policy](Answerer_%26_Abstention_Policy.md) (4 shared connections)

## Source Files

- `src/osc_assistant/observability/store.py`

## Audit Trail

- EXTRACTED: 41 (95%)
- INFERRED: 2 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*