# Cross-Process Trace Test

> 2 nodes

## Key Concepts

- **test_traces_are_readable_after_the_command_that_made_them_exited()** (2 connections) — `tests/test_cli.py`
- **Each `runner.invoke` is a separate command; the trace outlives it.** (1 connections) — `tests/test_cli.py`

## Relationships

- [Evaluation Methodology & Sources](Evaluation_Methodology_%26_Sources.md) (1 shared connections)

## Source Files

- `tests/test_cli.py`

## Audit Trail

- EXTRACTED: 3 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*