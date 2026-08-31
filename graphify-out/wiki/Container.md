# Container

> God node · 64 connections · `src/osc_assistant/container.py`

**Community:** [RRF Fusion & Citation Parsing](RRF_Fusion_%26_Citation_Parsing.md)

## Connections by Relation

### calls
- create_app() `EXTRACTED`
- _run_checks() `EXTRACTED`
- test_a_populated_index_produces_no_note() `EXTRACTED`
- _execute() `EXTRACTED`
- _execute_conversational() `EXTRACTED`
- test_shutdown_releases_every_component_that_was_built() `EXTRACTED`
- indexed() `EXTRACTED`
- test_a_session_that_outlives_its_ttl_is_reported_not_silently_emptied() `EXTRACTED`
- test_an_empty_index_is_reported_at_startup() `EXTRACTED`
- test_a_non_development_environment_is_called_out() `EXTRACTED`
- test_shutdown_does_not_construct_what_was_never_used() `EXTRACTED`
- test_a_component_that_fails_to_close_does_not_break_shutdown() `EXTRACTED`
- test_embedding_vectors_are_unaffected_by_the_close_probe() `EXTRACTED`

### contains
- container.py `EXTRACTED`

### imports
- app.py `EXTRACTED`
- diagnose.py `EXTRACTED`
- evaluate.py `EXTRACTED`
- core.py `EXTRACTED`
- banner.py `EXTRACTED`
- osc_assistant/__init__.py `EXTRACTED`

### method
- .sessions() `EXTRACTED`
- .shutdown() `EXTRACTED`
- .__aenter__() `EXTRACTED`
- .fast_llm() `EXTRACTED`
- .vector_store() `EXTRACTED`
- .__aexit__() `EXTRACTED`
- .answerer() `EXTRACTED`
- .chunker() `EXTRACTED`
- .conversation() `EXTRACTED`
- .embeddings() `EXTRACTED`
- .ingestion() `EXTRACTED`
- .__init__() `EXTRACTED`
- .llm() `EXTRACTED`
- .reranker() `EXTRACTED`
- .retrieval() `EXTRACTED`
- .startup() `EXTRACTED`

### rationale_for
- Builds and owns the application's components. `EXTRACTED`

### references
- startup_notes() `EXTRACTED`
- conversation() `EXTRACTED`
- describe_startup() `EXTRACTED`
- _assert_resolvable() `EXTRACTED`
- _check_store() `EXTRACTED`
- _check_chunker() `EXTRACTED`
- _check_reranker() `EXTRACTED`
- _check_llm() `EXTRACTED`
- _purge() `EXTRACTED`
- test_a_session_carries_context_into_a_follow_up() `EXTRACTED`
- test_re_running_an_unchanged_corpus_makes_no_embedding_calls() `EXTRACTED`
- _inspector() `EXTRACTED`
- test_a_binary_format_is_answerable() `EXTRACTED`
- test_a_corpus_of_six_formats_indexes() `EXTRACTED`
- test_a_grounded_answer_cites_the_source_it_came_from() `EXTRACTED`
- test_a_question_the_corpus_cannot_answer_is_declined() `EXTRACTED`
- test_hybrid_retrieval_ranks_the_right_document_first() `EXTRACTED`
- test_reindex_forces_work_the_hash_says_is_unnecessary() `EXTRACTED`
- test_the_run_is_fully_traced() `EXTRACTED`
- test_the_streamed_and_buffered_paths_agree_on_abstention() `EXTRACTED`

### uses
- [InMemorySessionStore](InMemorySessionStore.md) `INFERRED`
- [Settings](Settings.md) `INFERRED`
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- _ClosableEmbedding `INFERRED`
- Conversation `INFERRED`
- SessionStore `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*