# Doctor Command Tests

> 10 nodes

## Key Concepts

- **Path** (7 connections)
- **test_doctor_makes_live_calls_by_default()** (3 connections) — `tests/test_cli.py`
- **test_doctor_reports_a_broken_component_and_exits_non_zero()** (3 connections) — `tests/test_cli.py`
- **test_doctor_warns_about_files_no_parser_can_read()** (3 connections) — `tests/test_cli.py`
- **test_doctor_passes_when_every_component_is_reachable()** (2 connections) — `tests/test_cli.py`
- **test_doctor_can_skip_the_live_calls()** (2 connections) — `tests/test_cli.py`
- **test_doctor_warns_about_an_empty_index()** (2 connections) — `tests/test_cli.py`
- **Construction alone passes with the model unpulled or the credential expired.** (1 connections) — `tests/test_cli.py`
- **A failing provider must be named on one line, not raised as a traceback.** (1 connections) — `tests/test_cli.py`
- **A directory of .pptx looks identical to an empty corpus in the sync report.** (1 connections) — `tests/test_cli.py`

## Relationships

- [Evaluation Methodology & Sources](Evaluation_Methodology_%26_Sources.md) (6 shared connections)
- [CLI Failure Reporting Tests](CLI_Failure_Reporting_Tests.md) (1 shared connections)

## Source Files

- `tests/test_cli.py`

## Audit Trail

- EXTRACTED: 25 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*