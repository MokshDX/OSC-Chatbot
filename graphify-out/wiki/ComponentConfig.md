# ComponentConfig

> God node · 64 connections · `src/osc_assistant/registry.py`

**Community:** [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md)

## Connections by Relation

### calls
- _settings() `EXTRACTED`
- _settings() `EXTRACTED`
- test_shutdown_releases_every_component_that_was_built() `EXTRACTED`
- test_a_component_that_fails_to_close_does_not_break_shutdown() `EXTRACTED`
- test_shutdown_does_not_construct_what_was_never_used() `EXTRACTED`
- .vector_store() `EXTRACTED`
- test_langchain_chunkers_are_registered_and_satisfy_the_protocol() `EXTRACTED`
- test_re_registration_overrides() `EXTRACTED`
- .chunker() `EXTRACTED`
- test_options_are_passed_through_untouched() `EXTRACTED`
- test_registered_factory_is_used() `EXTRACTED`
- test_unknown_config_key_is_rejected() `EXTRACTED`
- test_unknown_provider_lists_the_alternatives() `EXTRACTED`

### contains
- registry.py `EXTRACTED`

### imports
- llm/langchain_bridge.py `EXTRACTED`
- settings.py `EXTRACTED`
- container.py `EXTRACTED`
- memory.py `EXTRACTED`
- pgvector.py `EXTRACTED`
- llm/openai_compatible.py `EXTRACTED`
- llm/gemini.py `EXTRACTED`
- anthropic_provider.py `EXTRACTED`
- langchain_splitters.py `EXTRACTED`
- recursive.py `EXTRACTED`
- embeddings/langchain_bridge.py `EXTRACTED`
- embeddings/gemini.py `EXTRACTED`
- embeddings/openai_compatible.py `EXTRACTED`
- cross_encoder.py `EXTRACTED`
- noop.py `EXTRACTED`
- local.py `EXTRACTED`
- voyage.py `EXTRACTED`

### inherits
- BaseModel `EXTRACTED`

### rationale_for
- Selects and configures one swappable component. `options` is intentionally… `EXTRACTED`

### references
- _build_langchain_recursive() `EXTRACTED`
- _build_markdown() `EXTRACTED`
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
- _build() `EXTRACTED`
- _build() `EXTRACTED`
- .create() `EXTRACTED`

### uses
- [Container](Container.md) `INFERRED`
- [Settings](Settings.md) `INFERRED`
- _FakeEmbeddings `INFERRED`
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- RetrievalSettings `INFERRED`
- _ClosableEmbedding `INFERRED`
- GenerationSettings `INFERRED`
- UnknownComponentError `INFERRED`
- ChunkingSettings `INFERRED`
- _YamlProfileSource `INFERRED`
- ObservabilitySettings `INFERRED`
- DatabaseSettings `INFERRED`
- LoggingSettings `INFERRED`
- ServerSettings `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*