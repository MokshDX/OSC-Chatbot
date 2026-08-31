# StoreInspector Protocol

> 20 nodes

## Key Concepts

- **Conversation** (19 connections) — `src/osc_assistant/conversation.py`
- **.answer()** (6 connections) — `src/osc_assistant/conversation.py`
- **.stream()** (6 connections) — `src/osc_assistant/conversation.py`
- **._load()** (6 connections) — `src/osc_assistant/conversation.py`
- **Message** (5 connections)
- **.record()** (5 connections) — `src/osc_assistant/conversation.py`
- **.history()** (4 connections) — `src/osc_assistant/conversation.py`
- **.history()** (3 connections) — `src/osc_assistant/conversation.py`
- **.__init__()** (3 connections) — `src/osc_assistant/conversation.py`
- **.conversation()** (2 connections) — `src/osc_assistant/container.py`
- **.destroy()** (2 connections) — `src/osc_assistant/conversation.py`
- **.close()** (2 connections) — `src/osc_assistant/conversation.py`
- **Answerer** (1 connections)
- **Answer** (1 connections)
- **The messages a new turn in this session should be answered against. Raises:…** (1 connections) — `src/osc_assistant/conversation.py`
- **A multi-turn question-answering session. The composition of a `SessionStore`…** (1 connections) — `src/osc_assistant/conversation.py`
- **The transcript so far, as the next turn would see it. For a client reconnecting…** (1 connections) — `src/osc_assistant/conversation.py`
- **Answer one turn in `session_id`, recording it in the session's history.** (1 connections) — `src/osc_assistant/conversation.py`
- **Stream one turn in `session_id`, recording it when the answer completes. The…** (1 connections) — `src/osc_assistant/conversation.py`
- **Fetch the history this turn will be answered against. Its own span because "the…** (1 connections) — `src/osc_assistant/conversation.py`

## Relationships

- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (4 shared connections)
- [Observability Subsystem](Observability_Subsystem.md) (3 shared connections)
- [Generation & Abstention Metrics](Generation_%26_Abstention_Metrics.md) (3 shared connections)
- [Document Loaders](Document_Loaders.md) (3 shared connections)
- [RRF Fusion & Citation Parsing](RRF_Fusion_%26_Citation_Parsing.md) (2 shared connections)
- [SessionStore Seam](SessionStore_Seam.md) (2 shared connections)
- [AccessLock & BulkImportExport Schemas](AccessLock_%26_BulkImportExport_Schemas.md) (2 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (1 shared connections)
- [Evaluation Runner Tests](Evaluation_Runner_Tests.md) (1 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/conversation.py`

## Audit Trail

- EXTRACTED: 67 (94%)
- INFERRED: 4 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*