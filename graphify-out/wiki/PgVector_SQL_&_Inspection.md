# PgVector SQL & Inspection

> 36 nodes

## Key Concepts

- **test_e2e.py** (28 connections) — `tests/test_e2e.py`
- **Path** (8 connections)
- **conversation()** (8 connections) — `tests/test_e2e.py`
- **indexed()** (7 connections) — `tests/test_e2e.py`
- **test_a_session_that_outlives_its_ttl_is_reported_not_silently_emptied()** (7 connections) — `tests/test_e2e.py`
- **_build_corpus()** (5 connections) — `tests/test_e2e.py`
- **corpus()** (5 connections) — `tests/test_e2e.py`
- **_purge()** (5 connections) — `tests/test_e2e.py`
- **_write_pdf()** (4 connections) — `tests/test_e2e.py`
- **test_re_running_an_unchanged_corpus_makes_no_embedding_calls()** (4 connections) — `tests/test_e2e.py`
- **test_a_session_carries_context_into_a_follow_up()** (4 connections) — `tests/test_e2e.py`
- **fixture** (3 connections)
- **test_reindex_forces_work_the_hash_says_is_unnecessary()** (3 connections) — `tests/test_e2e.py`
- **test_hybrid_retrieval_ranks_the_right_document_first()** (3 connections) — `tests/test_e2e.py`
- **test_a_grounded_answer_cites_the_source_it_came_from()** (3 connections) — `tests/test_e2e.py`
- **test_the_streamed_and_buffered_paths_agree_on_abstention()** (3 connections) — `tests/test_e2e.py`
- **test_closing_a_session_destroys_it_and_the_next_one_starts_clean()** (3 connections) — `tests/test_e2e.py`
- **test_two_live_sessions_do_not_share_memory()** (3 connections) — `tests/test_e2e.py`
- **test_a_conversational_turn_produces_one_trace_with_its_context_stage()** (3 connections) — `tests/test_e2e.py`
- **test_an_unanswerable_turn_inside_a_session_is_still_recorded()** (3 connections) — `tests/test_e2e.py`
- **End-to-end smoke test against the real stack. Everything else in this suite…** (1 connections) — `tests/test_e2e.py`
- **Write a minimal single-page PDF containing `lines` as extractable text. Hand-…** (1 connections) — `tests/test_e2e.py`
- **Write one document per parser family into `root`. Six formats, each carrying a…** (1 connections) — `tests/test_e2e.py`
- **A generated corpus, isolated per test and never read from `docs/`.** (1 connections) — `tests/test_e2e.py`
- **A container over a freshly synced corpus, cleaned up afterwards.** (1 connections) — `tests/test_e2e.py`
- *... and 11 more nodes in this community*

## Relationships

- [RRF Fusion & Citation Parsing](RRF_Fusion_%26_Citation_Parsing.md) (14 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (6 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (2 shared connections)
- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (2 shared connections)

## Source Files

- `tests/test_e2e.py`

## Audit Trail

- EXTRACTED: 128 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*