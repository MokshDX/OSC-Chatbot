# Settings

> God node · 37 connections · `src/osc_assistant/settings.py`

**Community:** [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md)

## Connections by Relation

### calls
- _settings() `EXTRACTED`
- _settings() `EXTRACTED`
- _settings() `EXTRACTED`
- _settings() `EXTRACTED`
- _settings() `EXTRACTED`
- test_the_configured_corpus_root_cannot_reach_the_engineering_knowledge_base() `INFERRED`
- test_observability_defaults_are_on() `EXTRACTED`
- test_traces_are_exposed_only_in_development() `EXTRACTED`

### contains
- settings.py `EXTRACTED`

### imports
- app.py `EXTRACTED`
- diagnose.py `EXTRACTED`
- evaluate.py `EXTRACTED`
- container.py `EXTRACTED`
- banner.py `EXTRACTED`
- osc_assistant/__init__.py `EXTRACTED`

### inherits
- BaseSettings `EXTRACTED`

### method
- .settings_customise_sources() `EXTRACTED`
- .traces_are_exposed() `EXTRACTED`

### rationale_for
- Root configuration object. Nested values are addressable from the environment… `EXTRACTED`

### references
- create_app() `EXTRACTED`
- load_settings() `EXTRACTED`
- _run_checks() `EXTRACTED`
- startup_notes() `EXTRACTED`
- _run_suite() `EXTRACTED`
- _execute() `EXTRACTED`
- _execute_conversational() `EXTRACTED`
- describe_startup() `EXTRACTED`
- _check_store() `EXTRACTED`
- _check_chunker() `EXTRACTED`
- _check_reranker() `EXTRACTED`
- _check_llm() `EXTRACTED`
- log_resolved_settings() `EXTRACTED`
- .__init__() `EXTRACTED`

### uses
- [Container](Container.md) `INFERRED`
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- _ClosableEmbedding `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*