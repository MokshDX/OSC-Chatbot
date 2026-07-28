# Component Config & Registry Tests

> 12 nodes · cohesion 0.23

## Key Concepts

- **ComponentConfig** (46 connections) — `src/osc_assistant/registry.py`
- **test_registry.py** (10 connections) — `tests/test_registry.py`
- **test_re_registration_overrides()** (4 connections) — `tests/test_registry.py`
- **test_options_are_passed_through_untouched()** (3 connections) — `tests/test_registry.py`
- **test_registered_factory_is_used()** (3 connections) — `tests/test_registry.py`
- **test_unknown_config_key_is_rejected()** (3 connections) — `tests/test_registry.py`
- **test_unknown_provider_lists_the_alternatives()** (3 connections) — `tests/test_registry.py`
- **BaseModel** (1 connections)
- **Selects and configures one swappable component. `options` is intentionally…** (1 connections) — `src/osc_assistant/registry.py`
- **The registry is the mechanism that makes providers pluggable, so it is tested…** (1 connections) — `tests/test_registry.py`
- **Overriding a built-in must be possible without editing it.** (1 connections) — `tests/test_registry.py`
- **A typo in a profile must fail loudly rather than be silently ignored.** (1 connections) — `tests/test_registry.py`

## Relationships

- [Provider Registry](Provider_Registry.md) (7 shared connections)
- [Settings Schema](Settings_Schema.md) (7 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (5 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (5 shared connections)
- [Chunker Registration](Chunker_Registration.md) (4 shared connections)
- [Embedding Model Interface](Embedding_Model_Interface.md) (3 shared connections)
- [Composition Root](Composition_Root.md) (2 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (2 shared connections)
- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (2 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (2 shared connections)
- [Dimension Guard & Match Source](Dimension_Guard_%26_Match_Source.md) (2 shared connections)
- [pgvector Setup & Codecs](pgvector_Setup_%26_Codecs.md) (2 shared connections)

## Source Files

- `src/osc_assistant/registry.py`
- `tests/test_registry.py`

## Audit Trail

- EXTRACTED: 68 (88%)
- INFERRED: 9 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*