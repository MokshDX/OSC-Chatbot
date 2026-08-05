# Settings Loading & YAML Profiles

> 34 nodes

## Key Concepts

- **load_settings()** (17 connections) — `src/osc_assistant/settings.py`
- **test_settings.py** (14 connections) — `tests/test_settings.py`
- **Path** (10 connections)
- **_profile()** (8 connections) — `tests/test_settings.py`
- **_YamlProfileSource** (7 connections) — `src/osc_assistant/settings.py`
- **_isolate_environment()** (5 connections) — `tests/test_settings.py`
- **test_the_environment_beats_the_profile()** (5 connections) — `tests/test_settings.py`
- **test_a_nested_override_replaces_only_the_named_field()** (5 connections) — `tests/test_settings.py`
- **test_a_profile_that_is_not_a_mapping_is_rejected()** (5 connections) — `tests/test_settings.py`
- **test_an_unknown_key_in_a_typed_block_is_rejected()** (5 connections) — `tests/test_settings.py`
- **.settings_customise_sources()** (4 connections) — `src/osc_assistant/settings.py`
- **test_a_yaml_profile_supplies_values()** (4 connections) — `tests/test_settings.py`
- **test_an_empty_profile_is_tolerated()** (4 connections) — `tests/test_settings.py`
- **Any** (3 connections)
- **test_init_arguments_beat_the_environment()** (3 connections) — `tests/test_settings.py`
- **test_a_missing_profile_is_tolerated()** (3 connections) — `tests/test_settings.py`
- **test_observability_defaults_are_on()** (3 connections) — `tests/test_settings.py`
- **test_traces_are_exposed_only_in_development()** (3 connections) — `tests/test_settings.py`
- **BaseSettings** (2 connections)
- **PydanticBaseSettingsSource** (2 connections)
- **.get_field_value()** (2 connections) — `src/osc_assistant/settings.py`
- **.__call__()** (2 connections) — `src/osc_assistant/settings.py`
- **Lowest-precedence source reading a YAML profile. The profile path comes from…** (1 connections) — `src/osc_assistant/settings.py`
- **Build settings, applying `overrides` at the highest precedence.** (1 connections) — `src/osc_assistant/settings.py`
- **fixture** (1 connections)
- *... and 9 more nodes in this community*

## Relationships

- [Settings Schema](Settings_Schema.md) (9 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (1 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (1 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (1 shared connections)

## Source Files

- `src/osc_assistant/settings.py`
- `tests/test_settings.py`

## Audit Trail

- EXTRACTED: 127 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*