# Evaluation CLI Command

> 47 nodes

## Key Concepts

- **evaluate.py** (31 connections) — `src/osc_assistant/cli/evaluate.py`
- **eval()** (21 connections) — `src/osc_assistant/cli/evaluate.py`
- **_shared.py** (19 connections) — `src/osc_assistant/cli/_shared.py`
- **GoldenSet** (17 connections) — `src/osc_assistant/evaluation/dataset.py`
- **EvaluationReport** (15 connections) — `src/osc_assistant/evaluation/runner.py`
- **dataset.py** (13 connections) — `src/osc_assistant/evaluation/dataset.py`
- **EvaluationError** (11 connections) — `src/osc_assistant/errors.py`
- **_execute()** (10 connections) — `src/osc_assistant/cli/evaluate.py`
- **traced_command()** (9 connections) — `src/osc_assistant/cli/_shared.py`
- **table()** (7 connections) — `src/osc_assistant/cli/_shared.py`
- **_assert_golden_set_is_resolvable()** (7 connections) — `src/osc_assistant/cli/evaluate.py`
- **_print_comparison()** (7 connections) — `src/osc_assistant/cli/evaluate.py`
- **unresolvable_documents()** (7 connections) — `src/osc_assistant/evaluation/dataset.py`
- **configuration_snapshot()** (6 connections) — `src/osc_assistant/evaluation/runner.py`
- **.run()** (6 connections) — `src/osc_assistant/evaluation/runner.py`
- **Path** (5 connections)
- **_write()** (5 connections) — `src/osc_assistant/cli/evaluate.py`
- **_print_report()** (5 connections) — `src/osc_assistant/cli/evaluate.py`
- **_enforce_thresholds()** (5 connections) — `src/osc_assistant/cli/evaluate.py`
- **_default_output()** (4 connections) — `src/osc_assistant/cli/evaluate.py`
- **.to_dict()** (3 connections) — `src/osc_assistant/evaluation/runner.py`
- **Any** (3 connections)
- **.referenced_documents()** (2 connections) — `src/osc_assistant/evaluation/dataset.py`
- **Plumbing shared by the CLI command modules. Kept separate so `core` and…** (1 connections) — `src/osc_assistant/cli/_shared.py`
- **A table styled consistently across every command.** (1 connections) — `src/osc_assistant/cli/_shared.py`
- *... and 22 more nodes in this community*

## Relationships

- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (20 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (16 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (8 shared connections)
- [Golden Set Loading & Evaluation Tests](Golden_Set_Loading_%26_Evaluation_Tests.md) (7 shared connections)
- [Settings Schema](Settings_Schema.md) (6 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (5 shared connections)
- [Observability Composition & Rendering](Observability_Composition_%26_Rendering.md) (3 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (3 shared connections)
- [AssistantError Base & Loaders](AssistantError_Base_%26_Loaders.md) (2 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (2 shared connections)
- [Trace Fetching & Persistence](Trace_Fetching_%26_Persistence.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/_shared.py`
- `src/osc_assistant/cli/evaluate.py`
- `src/osc_assistant/errors.py`
- `src/osc_assistant/evaluation/dataset.py`
- `src/osc_assistant/evaluation/runner.py`

## Audit Trail

- EXTRACTED: 236 (98%)
- INFERRED: 6 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*