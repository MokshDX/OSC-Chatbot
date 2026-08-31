# CLI Settings Bootstrap

> 11 nodes

## Key Concepts

- **log_command()** (6 connections) — `src/osc_assistant/cli/_shared.py`
- **load()** (5 connections) — `src/osc_assistant/cli/_shared.py`
- **test_the_command_that_ran_is_named_in_the_log()** (5 connections) — `tests/test_logging.py`
- **test_positional_arguments_are_payload_and_stay_out_by_default()** (5 connections) — `tests/test_logging.py`
- **test_payload_capture_records_the_whole_invocation()** (4 connections) — `tests/test_logging.py`
- **Path** (1 connections)
- **Settings** (1 connections)
- **Resolve settings and initialise logging and tracing for one command.…** (1 connections) — `src/osc_assistant/cli/_shared.py`
- **Name the command that is about to run. Without it a day of history is a stream…** (1 connections) — `src/osc_assistant/cli/_shared.py`
- **Every command initialises identically; without this they are indistinguishable.** (1 connections) — `tests/test_logging.py`
- **`osc ask "<a real question>"` puts user text on the command line.** (1 connections) — `tests/test_logging.py`

## Relationships

- [In-Memory Session Store](In-Memory_Session_Store.md) (9 shared connections)
- [CLI Shared Plumbing](CLI_Shared_Plumbing.md) (2 shared connections)

## Source Files

- `src/osc_assistant/cli/_shared.py`
- `tests/test_logging.py`

## Audit Trail

- EXTRACTED: 31 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*