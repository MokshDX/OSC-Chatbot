# Observability Subsystem

> 15 nodes

## Key Concepts

- **UnknownSessionError** (6 connections) — `src/osc_assistant/conversation.py`
- **SessionState** (6 connections) — `src/osc_assistant/conversation.py`
- **._require()** (6 connections) — `src/osc_assistant/conversation.py`
- **.create()** (5 connections) — `src/osc_assistant/conversation.py`
- **.history()** (4 connections) — `src/osc_assistant/conversation.py`
- **._expire_idle()** (4 connections) — `src/osc_assistant/conversation.py`
- **.describe()** (3 connections) — `src/osc_assistant/conversation.py`
- **._evict_over_capacity()** (2 connections) — `src/osc_assistant/conversation.py`
- **.start()** (2 connections) — `src/osc_assistant/conversation.py`
- **AssistantError** (1 connections)
- **The session id is not known to this store. An operator problem rather than a…** (1 connections) — `src/osc_assistant/conversation.py`
- **One conversation's working set. `messages` alternates user and assistant and is…** (1 connections) — `src/osc_assistant/conversation.py`
- **The messages this session holds, and the start of an interaction. Reading…** (1 connections) — `src/osc_assistant/conversation.py`
- **Read a session's state without touching its activity clock. For diagnostics…** (1 connections) — `src/osc_assistant/conversation.py`
- **Drop sessions untouched for longer than the TTL. Swept on access rather than on…** (1 connections) — `src/osc_assistant/conversation.py`

## Relationships

- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (10 shared connections)
- [StoreInspector Protocol](StoreInspector_Protocol.md) (3 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (1 shared connections)

## Source Files

- `src/osc_assistant/conversation.py`

## Audit Trail

- EXTRACTED: 42 (95%)
- INFERRED: 2 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*