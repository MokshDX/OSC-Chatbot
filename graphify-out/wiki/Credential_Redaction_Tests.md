# Credential Redaction Tests

> 4 nodes

## Key Concepts

- **test_token_counts_are_not_mistaken_for_credentials()** (5 connections) — `tests/test_logging.py`
- **test_credential_fields_are_redacted()** (4 connections) — `tests/test_logging.py`
- **parametrize** (2 connections)
- **Regression: `input_tokens` contains "token" and is a cost measurement. The…** (1 connections) — `tests/test_logging.py`

## Relationships

- [In-Memory Session Store](In-Memory_Session_Store.md) (6 shared connections)

## Source Files

- `tests/test_logging.py`

## Audit Trail

- EXTRACTED: 12 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*