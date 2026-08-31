# Chunking & Embedding Architecture

> 26 nodes

## Key Concepts

- **load_settings()** (15 connections) — `src/osc_assistant/settings.py`
- **test_settings.py** (14 connections) — `tests/test_settings.py`
- **Path** (10 connections)
- **_profile()** (8 connections) — `tests/test_settings.py`
- **_isolate_environment()** (5 connections) — `tests/test_settings.py`
- **test_the_environment_beats_the_profile()** (5 connections) — `tests/test_settings.py`
- **test_a_nested_override_replaces_only_the_named_field()** (5 connections) — `tests/test_settings.py`
- **test_a_profile_that_is_not_a_mapping_is_rejected()** (5 connections) — `tests/test_settings.py`
- **test_an_unknown_key_in_a_typed_block_is_rejected()** (5 connections) — `tests/test_settings.py`
- **test_a_yaml_profile_supplies_values()** (4 connections) — `tests/test_settings.py`
- **test_an_empty_profile_is_tolerated()** (4 connections) — `tests/test_settings.py`
- **test_init_arguments_beat_the_environment()** (3 connections) — `tests/test_settings.py`
- **test_a_missing_profile_is_tolerated()** (3 connections) — `tests/test_settings.py`
- **test_observability_defaults_are_on()** (3 connections) — `tests/test_settings.py`
- **test_traces_are_exposed_only_in_development()** (3 connections) — `tests/test_settings.py`
- **fixture** (1 connections)
- **MonkeyPatch** (1 connections)
- **Configuration precedence tests. `settings.py` carries the only hand-written…** (1 connections) — `tests/test_settings.py`
- **Strip inherited OSC_ variables and point at an empty profile. Without this the…** (1 connections) — `tests/test_settings.py`
- **The layer order exists so a deployment can override a checked-in file.** (1 connections) — `tests/test_settings.py`
- **The behaviour operators actually rely on, and the easiest to break. Overriding…** (1 connections) — `tests/test_settings.py`
- **The built-in defaults are a working configuration; absence is not an error.** (1 connections) — `tests/test_settings.py`
- **Failing loudly beats silently ignoring the file an operator just edited.** (1 connections) — `tests/test_settings.py`
- **A typo in a tuning knob must not be silently discarded.** (1 connections) — `tests/test_settings.py`
- **The environment check is not overridable by the setting, on purpose. A profile…** (1 connections) — `tests/test_settings.py`
- *... and 1 more nodes in this community*

## Relationships

- [Session Store Internals](Session_Store_Internals.md) (3 shared connections)
- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (3 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (2 shared connections)
- [Settings Validators](Settings_Validators.md) (1 shared connections)

## Source Files

- `src/osc_assistant/settings.py`
- `tests/test_settings.py`

## Audit Trail

- EXTRACTED: 103 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*