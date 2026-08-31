# Gemini Adapter

> 22 nodes

## Key Concepts

- **Registry** (14 connections) — `src/osc_assistant/registry.py`
- **test_registry.py** (10 connections) — `tests/test_registry.py`
- **.create()** (5 connections) — `src/osc_assistant/registry.py`
- **.register()** (4 connections) — `src/osc_assistant/registry.py`
- **test_re_registration_overrides()** (4 connections) — `tests/test_registry.py`
- **test_built_in_providers_are_registered()** (4 connections) — `tests/test_registry.py`
- **test_registered_factory_is_used()** (3 connections) — `tests/test_registry.py`
- **test_unknown_provider_lists_the_alternatives()** (3 connections) — `tests/test_registry.py`
- **test_options_are_passed_through_untouched()** (3 connections) — `tests/test_registry.py`
- **test_unknown_config_key_is_rejected()** (3 connections) — `tests/test_registry.py`
- **T** (2 connections)
- **.names()** (2 connections) — `src/osc_assistant/registry.py`
- **.__init__()** (1 connections) — `src/osc_assistant/registry.py`
- **Factory** (1 connections)
- **.__contains__()** (1 connections) — `src/osc_assistant/registry.py`
- **Maps a provider name to a factory for one kind of component.** (1 connections) — `src/osc_assistant/registry.py`
- **Decorator registering a factory under `name`. Re-registering a name replaces…** (1 connections) — `src/osc_assistant/registry.py`
- **parametrize** (1 connections)
- **The registry is the mechanism that makes providers pluggable, so it is tested…** (1 connections) — `tests/test_registry.py`
- **Overriding a built-in must be possible without editing it.** (1 connections) — `tests/test_registry.py`
- **A typo in a profile must fail loudly rather than be silently ignored.** (1 connections) — `tests/test_registry.py`
- **Importing the package must make every built-in provider selectable.** (1 connections) — `tests/test_registry.py`

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (7 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (6 shared connections)

## Source Files

- `src/osc_assistant/registry.py`
- `tests/test_registry.py`

## Audit Trail

- EXTRACTED: 66 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*