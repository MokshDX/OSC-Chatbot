# Log Retention Tests

> 4 nodes

## Key Concepts

- **test_retention_deletes_the_oldest_rather_than_keeping_it()** (3 connections) — `tests/test_logging.py`
- **test_an_unwritable_log_directory_does_not_stop_the_process()** (3 connections) — `tests/test_logging.py`
- **The property that makes disk bounded rather than merely monitored.** (1 connections) — `tests/test_logging.py`
- **An operational problem, not a reason to refuse to start. Console logging still…** (1 connections) — `tests/test_logging.py`

## Relationships

- [In-Memory Session Store](In-Memory_Session_Store.md) (4 shared connections)

## Source Files

- `tests/test_logging.py`

## Audit Trail

- EXTRACTED: 8 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*