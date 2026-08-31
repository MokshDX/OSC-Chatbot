# CLI Failure Reporting Tests

> 8 nodes

## Key Concepts

- **_stub_environment()** (5 connections) — `tests/test_cli.py`
- **MonkeyPatch** (3 connections)
- **test_an_operator_error_is_a_message_not_a_traceback()** (3 connections) — `tests/test_cli.py`
- **test_a_failure_inside_a_stage_prints_the_trace()** (3 connections) — `tests/test_cli.py`
- **fixture** (1 connections)
- **Point the CLI at in-process doubles through configuration alone. Which is the…** (1 connections) — `tests/test_cli.py`
- **`AssistantError` names a problem the operator must fix; frames bury it.** (1 connections) — `tests/test_cli.py`
- **The trace names the stage that raised and what every earlier stage did.** (1 connections) — `tests/test_cli.py`

## Relationships

- [Evaluation Methodology & Sources](Evaluation_Methodology_%26_Sources.md) (3 shared connections)
- [Doctor Command Tests](Doctor_Command_Tests.md) (1 shared connections)

## Source Files

- `tests/test_cli.py`

## Audit Trail

- EXTRACTED: 18 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*