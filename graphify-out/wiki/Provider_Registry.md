# Provider Registry

> 15 nodes · cohesion 0.16

## Key Concepts

- **Registry** (14 connections) — `src/osc_assistant/registry.py`
- **UnknownComponentError** (8 connections) — `src/osc_assistant/errors.py`
- **.create()** (5 connections) — `src/osc_assistant/registry.py`
- **.register()** (4 connections) — `src/osc_assistant/registry.py`
- **test_built_in_providers_are_registered()** (4 connections) — `tests/test_registry.py`
- **.names()** (2 connections) — `src/osc_assistant/registry.py`
- **T** (2 connections)
- **Factory** (1 connections)
- **A component was requested by a name that is not registered.** (1 connections) — `src/osc_assistant/errors.py`
- **Maps a provider name to a factory for one kind of component.** (1 connections) — `src/osc_assistant/registry.py`
- **Decorator registering a factory under `name`. Re-registering a name replaces…** (1 connections) — `src/osc_assistant/registry.py`
- **.__contains__()** (1 connections) — `src/osc_assistant/registry.py`
- **.__init__()** (1 connections) — `src/osc_assistant/registry.py`
- **parametrize** (1 connections)
- **Importing the package must make every built-in provider selectable.** (1 connections) — `tests/test_registry.py`

## Relationships

- [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md) (7 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (3 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (2 shared connections)
- [Dimension Guard & Match Source](Dimension_Guard_%26_Match_Source.md) (1 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/registry.py`
- `tests/test_registry.py`

## Audit Trail

- EXTRACTED: 44 (94%)
- INFERRED: 3 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*