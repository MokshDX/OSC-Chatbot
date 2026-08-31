# Handler Reconfiguration Test

> 2 nodes

## Key Concepts

- **test_reconfiguring_does_not_duplicate_records()** (4 connections) — `tests/test_logging.py`
- **Each `configure_logging` replaces the stack rather than adding to it.** (1 connections) — `tests/test_logging.py`

## Relationships

- [In-Memory Session Store](In-Memory_Session_Store.md) (3 shared connections)

## Source Files

- `tests/test_logging.py`

## Audit Trail

- EXTRACTED: 5 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*