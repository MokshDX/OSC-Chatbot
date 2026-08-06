# Settings

> God node · 36 connections · `src/osc_assistant/settings.py`

**Community:** [Doctor Health Checks](Doctor_Health_Checks.md)

## Connections by Relation

### calls
- _settings() `EXTRACTED`
- _settings() `EXTRACTED`
- _settings() `EXTRACTED`
- test_observability_defaults_are_on() `EXTRACTED`
- test_traces_are_exposed_only_in_development() `EXTRACTED`

### contains
- settings.py `EXTRACTED`

### imports
- diagnose.py `EXTRACTED`
- app.py `EXTRACTED`
- evaluate.py `EXTRACTED`
- container.py `EXTRACTED`
- runner.py `EXTRACTED`
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
- _execute() `EXTRACTED`
- describe_startup() `EXTRACTED`
- _check_llm() `EXTRACTED`
- configuration_snapshot() `EXTRACTED`
- log_resolved_settings() `EXTRACTED`
- _check_store() `EXTRACTED`
- _check_chunker() `EXTRACTED`
- _check_reranker() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`

### uses
- [ComponentConfig](ComponentConfig.md) `INFERRED`
- [Container](Container.md) `INFERRED`
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- _ClosableEmbedding `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*