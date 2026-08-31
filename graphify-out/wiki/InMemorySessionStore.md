# InMemorySessionStore

> God node · 46 connections · `src/osc_assistant/conversation.py`

**Community:** [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md)

## Connections by Relation

### calls
- evaluator() `EXTRACTED`
- test_a_failed_turn_still_releases_its_session() `EXTRACTED`
- test_a_failing_provider_costs_one_turn_not_the_whole_run() `EXTRACTED`
- test_an_abstention_is_still_recorded_as_a_turn() `EXTRACTED`
- test_a_stream_that_fails_partway_records_no_turn() `EXTRACTED`
- .sessions() `EXTRACTED`
- test_activity_postpones_expiry() `EXTRACTED`
- test_history_is_trimmed_from_the_oldest_end() `EXTRACTED`
- test_reading_history_postpones_expiry_so_a_turn_cannot_outlive_itself() `EXTRACTED`
- test_a_reopened_session_id_is_never_reissued() `EXTRACTED`
- test_a_trimmed_session_still_reports_its_true_length() `EXTRACTED`
- test_an_idle_session_expires() `EXTRACTED`
- test_an_unknown_session_names_the_three_ordinary_causes() `EXTRACTED`
- test_destroying_an_unknown_session_reports_that_there_was_nothing() `EXTRACTED`
- test_history_is_a_copy_so_a_caller_cannot_mutate_the_session() `EXTRACTED`
- test_the_least_recently_used_session_is_evicted_at_capacity() `EXTRACTED`
- test_the_protocol_is_satisfied_structurally() `EXTRACTED`
- test_a_new_session_starts_empty() `EXTRACTED`
- test_a_recorded_turn_becomes_user_then_assistant_messages() `EXTRACTED`
- test_closing_a_session_destroys_its_memory() `EXTRACTED`

### contains
- conversation.py `EXTRACTED`

### imports
- container.py `EXTRACTED`

### method
- ._require() `EXTRACTED`
- .create() `EXTRACTED`
- .record() `EXTRACTED`
- ._expire_idle() `EXTRACTED`
- .history() `EXTRACTED`
- .describe() `EXTRACTED`
- .destroy() `EXTRACTED`
- ._evict_over_capacity() `EXTRACTED`
- .__init__() `EXTRACTED`
- .live_sessions() `EXTRACTED`

### rationale_for
- Process-local conversation memory, bounded three ways. The bounds are the… `EXTRACTED`

### references
- conversation() `EXTRACTED`
- test_a_first_turn_is_answered_with_no_history() `EXTRACTED`
- test_a_follow_up_turn_carries_the_previous_exchange_into_generation() `EXTRACTED`
- test_a_new_session_after_a_close_starts_with_clean_context() `EXTRACTED`
- test_a_streamed_follow_up_sees_the_previous_streamed_turn() `EXTRACTED`
- test_the_session_context_span_distinguishes_a_follow_up_from_a_first_turn() `EXTRACTED`
- test_two_sessions_answered_in_parallel_do_not_mix_context() `EXTRACTED`
- test_a_closed_session_refuses_further_turns() `EXTRACTED`
- test_a_streamed_turn_is_recorded_once_the_answer_completes() `EXTRACTED`

### uses
- [Container](Container.md) `INFERRED`
- SessionSettings `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*