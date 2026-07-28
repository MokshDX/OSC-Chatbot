# ComponentConfig

> God node · 46 connections · `src/osc_assistant/registry.py`

**Community:** [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md)

## Connections by Relation

### calls
- _settings() `EXTRACTED`
- .vector_store() `EXTRACTED`
- test_re_registration_overrides() `EXTRACTED`
- .chunker() `EXTRACTED`
- test_options_are_passed_through_untouched() `EXTRACTED`
- test_registered_factory_is_used() `EXTRACTED`
- test_unknown_config_key_is_rejected() `EXTRACTED`
- test_unknown_provider_lists_the_alternatives() `EXTRACTED`

### contains
- registry.py `EXTRACTED`

### imports
- llm/gemini.py `EXTRACTED`
- anthropic_provider.py `EXTRACTED`
- llm/openai_compatible.py `EXTRACTED`
- container.py `EXTRACTED`
- pgvector.py `EXTRACTED`
- memory.py `EXTRACTED`
- recursive.py `EXTRACTED`
- settings.py `EXTRACTED`
- embeddings/gemini.py `EXTRACTED`
- embeddings/openai_compatible.py `EXTRACTED`
- cross_encoder.py `EXTRACTED`
- local.py `EXTRACTED`
- voyage.py `EXTRACTED`
- noop.py `EXTRACTED`

### inherits
- BaseModel `EXTRACTED`

### rationale_for
- Selects and configures one swappable component. `options` is intentionally… `EXTRACTED`

### references
- _build_recursive() `EXTRACTED`
- _build_fixed() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- .create() `EXTRACTED`

### uses
- Container `INFERRED`
- Settings `INFERRED`
- RetrievalSettings `INFERRED`
- UnknownComponentError `INFERRED`
- GenerationSettings `INFERRED`
- _YamlProfileSource `INFERRED`
- ChunkingSettings `INFERRED`
- DatabaseSettings `INFERRED`
- ServerSettings `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*