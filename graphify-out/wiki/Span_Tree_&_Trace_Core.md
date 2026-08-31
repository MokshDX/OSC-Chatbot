# Span Tree & Trace Core

> 35 nodes

## Key Concepts

- **InMemorySessionStore** (46 connections) — `src/osc_assistant/conversation.py`
- **test_conversation.py** (32 connections) — `tests/test_conversation.py`
- **conversation.py** (19 connections) — `src/osc_assistant/conversation.py`
- **SessionSettings** (18 connections) — `src/osc_assistant/settings.py`
- **test_history_is_trimmed_from_the_oldest_end()** (4 connections) — `tests/test_conversation.py`
- **test_activity_postpones_expiry()** (4 connections) — `tests/test_conversation.py`
- **test_reading_history_postpones_expiry_so_a_turn_cannot_outlive_itself()** (4 connections) — `tests/test_conversation.py`
- **test_the_protocol_is_satisfied_structurally()** (3 connections) — `tests/test_conversation.py`
- **test_history_is_a_copy_so_a_caller_cannot_mutate_the_session()** (3 connections) — `tests/test_conversation.py`
- **test_destroying_an_unknown_session_reports_that_there_was_nothing()** (3 connections) — `tests/test_conversation.py`
- **test_a_reopened_session_id_is_never_reissued()** (3 connections) — `tests/test_conversation.py`
- **test_an_unknown_session_names_the_three_ordinary_causes()** (3 connections) — `tests/test_conversation.py`
- **test_a_trimmed_session_still_reports_its_true_length()** (3 connections) — `tests/test_conversation.py`
- **test_the_least_recently_used_session_is_evicted_at_capacity()** (3 connections) — `tests/test_conversation.py`
- **test_an_idle_session_expires()** (3 connections) — `tests/test_conversation.py`
- **.__init__()** (2 connections) — `src/osc_assistant/conversation.py`
- **.live_sessions()** (2 connections) — `src/osc_assistant/conversation.py`
- **test_a_new_session_starts_empty()** (2 connections) — `tests/test_conversation.py`
- **test_a_recorded_turn_becomes_user_then_assistant_messages()** (2 connections) — `tests/test_conversation.py`
- **test_sessions_cannot_see_each_other()** (2 connections) — `tests/test_conversation.py`
- **test_closing_a_session_destroys_its_memory()** (2 connections) — `tests/test_conversation.py`
- **test_live_session_count_tracks_creation_and_closure()** (2 connections) — `tests/test_conversation.py`
- **Session-scoped conversational memory. Until this module existed, every question…** (1 connections) — `src/osc_assistant/conversation.py`
- **Process-local conversation memory, bounded three ways. The bounds are the…** (1 connections) — `src/osc_assistant/conversation.py`
- **How many sessions are currently held. For `doctor` and for tests.** (1 connections) — `src/osc_assistant/conversation.py`
- *... and 10 more nodes in this community*

## Relationships

- [Generation & Abstention Metrics](Generation_%26_Abstention_Metrics.md) (22 shared connections)
- [Observability Subsystem](Observability_Subsystem.md) (10 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (6 shared connections)
- [Document Loaders](Document_Loaders.md) (5 shared connections)
- [StoreInspector Protocol](StoreInspector_Protocol.md) (4 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (3 shared connections)
- [SessionStore Seam](SessionStore_Seam.md) (3 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (2 shared connections)
- [PgVector SQL & Inspection](PgVector_SQL_%26_Inspection.md) (2 shared connections)
- [Evaluation Runner Tests](Evaluation_Runner_Tests.md) (1 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (1 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (1 shared connections)

## Source Files

- `src/osc_assistant/conversation.py`
- `src/osc_assistant/settings.py`
- `tests/test_conversation.py`

## Audit Trail

- EXTRACTED: 171 (96%)
- INFERRED: 7 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*