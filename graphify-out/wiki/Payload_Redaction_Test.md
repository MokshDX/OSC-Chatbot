# Payload Redaction Test

> 2 nodes

## Key Concepts

- **test_credentials_are_redacted_even_with_payload_capture_on()** (4 connections) — `tests/test_logging.py`
- **`capture_payloads` opens up corpus text. It must not open up secrets.** (1 connections) — `tests/test_logging.py`

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