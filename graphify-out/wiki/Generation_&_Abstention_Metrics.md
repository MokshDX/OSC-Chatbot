# Generation & Abstention Metrics

> 25 nodes

## Key Concepts

- **conversation()** (19 connections) — `tests/test_conversation.py`
- **StubChatModel** (16 connections)
- **test_an_abstention_is_still_recorded_as_a_turn()** (10 connections) — `tests/test_conversation.py`
- **test_a_stream_that_fails_partway_records_no_turn()** (9 connections) — `tests/test_conversation.py`
- **test_a_first_turn_is_answered_with_no_history()** (5 connections) — `tests/test_conversation.py`
- **test_a_follow_up_turn_carries_the_previous_exchange_into_generation()** (5 connections) — `tests/test_conversation.py`
- **test_two_sessions_answered_in_parallel_do_not_mix_context()** (5 connections) — `tests/test_conversation.py`
- **test_a_new_session_after_a_close_starts_with_clean_context()** (5 connections) — `tests/test_conversation.py`
- **test_a_streamed_follow_up_sees_the_previous_streamed_turn()** (5 connections) — `tests/test_conversation.py`
- **test_the_session_context_span_distinguishes_a_follow_up_from_a_first_turn()** (5 connections) — `tests/test_conversation.py`
- **test_a_closed_session_refuses_further_turns()** (4 connections) — `tests/test_conversation.py`
- **test_a_streamed_turn_is_recorded_once_the_answer_completes()** (4 connections) — `tests/test_conversation.py`
- **MemoryVectorStore** (3 connections)
- **StubEmbeddingModel** (3 connections)
- **Document** (3 connections)
- **fixture** (1 connections)
- **A `Conversation` over the shared fixture corpus, with an inspectable model.…** (1 connections) — `tests/test_conversation.py`
- **Single-turn behaviour is unchanged by the existence of sessions.** (1 connections) — `tests/test_conversation.py`
- **The load-bearing assertion of this whole module. Checked against what the…** (1 connections) — `tests/test_conversation.py`
- **Context isolation under concurrency, which is how a service is actually used.** (1 connections) — `tests/test_conversation.py`
- **The full cleanup cycle: close destroys, and the replacement inherits nothing.** (1 connections) — `tests/test_conversation.py`
- **Otherwise a follow-up like "why not?" resolves against nothing. The abstention…** (1 connections) — `tests/test_conversation.py`
- **Memory must work identically in both modes, as the abstention policy does.** (1 connections) — `tests/test_conversation.py`
- **A failed turn is not a turn. Recording the deltas seen before the failure would…** (1 connections) — `tests/test_conversation.py`
- **Diagnosability: "answered as if it were a first question" must be visible. That…** (1 connections) — `tests/test_conversation.py`

## Relationships

- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (22 shared connections)
- [Document Loaders](Document_Loaders.md) (4 shared connections)
- [Answer & Citation Types](Answer_%26_Citation_Types.md) (4 shared connections)
- [StoreInspector Protocol](StoreInspector_Protocol.md) (3 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (3 shared connections)
- [API Layer Tests](API_Layer_Tests.md) (1 shared connections)

## Source Files

- `tests/test_conversation.py`

## Audit Trail

- EXTRACTED: 105 (95%)
- INFERRED: 6 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*