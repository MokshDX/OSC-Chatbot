# SessionStore Seam

> 10 nodes

## Key Concepts

- **SessionStore** (12 connections) — `src/osc_assistant/conversation.py`
- **.sessions()** (4 connections) — `src/osc_assistant/container.py`
- **.create()** (2 connections) — `src/osc_assistant/conversation.py`
- **.record()** (2 connections) — `src/osc_assistant/conversation.py`
- **.destroy()** (2 connections) — `src/osc_assistant/conversation.py`
- **Conversational memory. Not built through a registry, unlike the five swappable…** (1 connections) — `src/osc_assistant/container.py`
- **Where conversation state lives between turns. Async because the implementation…** (1 connections) — `src/osc_assistant/conversation.py`
- **Open a session and return its id.** (1 connections) — `src/osc_assistant/conversation.py`
- **Append one completed exchange. Raises: UnknownSessionError: No such session, or…** (1 connections) — `src/osc_assistant/conversation.py`
- **Destroy a session's memory. Returns whether there was one to destroy. Named…** (1 connections) — `src/osc_assistant/conversation.py`

## Relationships

- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (3 shared connections)
- [RRF Fusion & Citation Parsing](RRF_Fusion_%26_Citation_Parsing.md) (2 shared connections)
- [StoreInspector Protocol](StoreInspector_Protocol.md) (2 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (1 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (1 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/conversation.py`

## Audit Trail

- EXTRACTED: 25 (93%)
- INFERRED: 2 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*