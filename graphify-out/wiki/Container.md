# Container

> God node · 60 connections · `src/osc_assistant/container.py`

**Community:** [Container Lifecycle](Container_Lifecycle.md)

## Connections by Relation

### calls
- create_app() `EXTRACTED`
- _run_checks() `EXTRACTED`
- _execute() `EXTRACTED`
- test_a_populated_index_produces_no_note() `EXTRACTED`
- indexed() `EXTRACTED`
- test_shutdown_releases_every_component_that_was_built() `EXTRACTED`
- test_a_component_that_fails_to_close_does_not_break_shutdown() `EXTRACTED`
- test_a_non_development_environment_is_called_out() `EXTRACTED`
- test_an_empty_index_is_reported_at_startup() `EXTRACTED`
- test_embedding_vectors_are_unaffected_by_the_close_probe() `EXTRACTED`
- test_shutdown_does_not_construct_what_was_never_used() `EXTRACTED`

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
- .shutdown() `EXTRACTED`
- .vector_store() `EXTRACTED`
- .__aenter__() `EXTRACTED`
- .chunker() `EXTRACTED`
- .fast_llm() `EXTRACTED`
- .retrieval() `EXTRACTED`
- .__aexit__() `EXTRACTED`
- .answerer() `EXTRACTED`
- .embeddings() `EXTRACTED`
- .ingestion() `EXTRACTED`
- .__init__() `EXTRACTED`
- .llm() `EXTRACTED`
- .reranker() `EXTRACTED`
- .startup() `EXTRACTED`

### rationale_for
- Builds and owns the application's components. `EXTRACTED`

### references
- startup_notes() `EXTRACTED`
- describe_startup() `EXTRACTED`
- _check_llm() `EXTRACTED`
- _assert_golden_set_is_resolvable() `EXTRACTED`
- _check_store() `EXTRACTED`
- _check_chunker() `EXTRACTED`
- _check_reranker() `EXTRACTED`
- test_re_running_an_unchanged_corpus_makes_no_embedding_calls() `EXTRACTED`
- _inspector() `EXTRACTED`
- test_reindex_forces_work_the_hash_says_is_unnecessary() `EXTRACTED`
- test_a_binary_format_is_answerable() `EXTRACTED`
- test_a_corpus_of_six_formats_indexes() `EXTRACTED`
- test_a_grounded_answer_cites_the_source_it_came_from() `EXTRACTED`
- test_a_question_the_corpus_cannot_answer_is_declined() `EXTRACTED`
- test_hybrid_retrieval_ranks_the_right_document_first() `EXTRACTED`
- test_the_run_is_fully_traced() `EXTRACTED`
- test_the_streamed_and_buffered_paths_agree_on_abstention() `EXTRACTED`

### uses
- [ComponentConfig](ComponentConfig.md) `INFERRED`
- [Settings](Settings.md) `INFERRED`
- ChatModel `INFERRED`
- EmbeddingModel `INFERRED`
- VectorStore `INFERRED`
- Chunker `INFERRED`
- Reranker `INFERRED`
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- _ClosableEmbedding `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*