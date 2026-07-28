# Settings Loading & YAML Profiles

> 15 nodes · cohesion 0.18

## Key Concepts

- **Settings** (14 connections) — `src/osc_assistant/settings.py`
- **load_settings()** (9 connections) — `src/osc_assistant/settings.py`
- **_YamlProfileSource** (7 connections) — `src/osc_assistant/settings.py`
- **osc_assistant/__init__.py** (6 connections) — `src/osc_assistant/__init__.py`
- **.settings_customise_sources()** (4 connections) — `src/osc_assistant/settings.py`
- **Any** (3 connections)
- **BaseSettings** (2 connections)
- **PydanticBaseSettingsSource** (2 connections)
- **.__init__()** (2 connections) — `src/osc_assistant/container.py`
- **.__call__()** (2 connections) — `src/osc_assistant/settings.py`
- **.get_field_value()** (2 connections) — `src/osc_assistant/settings.py`
- **OSC internal knowledge assistant. A provider-agnostic retrieval-augmented…** (1 connections) — `src/osc_assistant/__init__.py`
- **Lowest-precedence source reading a YAML profile. The profile path comes from…** (1 connections) — `src/osc_assistant/settings.py`
- **Build settings, applying `overrides` at the highest precedence.** (1 connections) — `src/osc_assistant/settings.py`
- **Root configuration object. Nested values are addressable from the environment…** (1 connections) — `src/osc_assistant/settings.py`

## Relationships

- [Settings Schema](Settings_Schema.md) (5 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (4 shared connections)
- [Composition Root](Composition_Root.md) (3 shared connections)
- [Command Line Interface](Command_Line_Interface.md) (3 shared connections)
- [Structured Logging](Structured_Logging.md) (2 shared connections)
- [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md) (2 shared connections)

## Source Files

- `src/osc_assistant/__init__.py`
- `src/osc_assistant/container.py`
- `src/osc_assistant/settings.py`

## Audit Trail

- EXTRACTED: 54 (95%)
- INFERRED: 3 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*