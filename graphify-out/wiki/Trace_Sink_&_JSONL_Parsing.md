# Trace Sink & JSONL Parsing

> 12 nodes · cohesion 0.18

## Key Concepts

- **trace_from_dict()** (12 connections) — `src/osc_assistant/observability/store.py`
- **active_trace_store()** (11 connections) — `src/osc_assistant/observability/__init__.py`
- **test_a_trace_survives_serialisation_intact()** (6 connections) — `tests/test_trace_store.py`
- **_parse_line()** (5 connections) — `src/osc_assistant/observability/store.py`
- **test_an_error_survives_the_round_trip()** (5 connections) — `tests/test_trace_store.py`
- **test_persistence_can_be_turned_off()** (4 connections) — `tests/test_trace_store.py`
- **The store traces are being written to, if persistence is enabled.** (1 connections) — `src/osc_assistant/observability/__init__.py`
- **Any** (1 connections)
- **Parse one record, skipping anything malformed. A truncated final line is…** (1 connections) — `src/osc_assistant/observability/store.py`
- **Rebuild a `Trace` from its serialised form. The inverse of `Trace.to_dict`, and…** (1 connections) — `src/osc_assistant/observability/store.py`
- **One format for the file and the HTTP body, so one parser serves both.** (1 connections) — `tests/test_trace_store.py`
- **Diagnosing a failure after the fact is the main reason to persist at all.** (1 connections) — `tests/test_trace_store.py`

## Relationships

- [Trace Store Tests](Trace_Store_Tests.md) (6 shared connections)
- [Persistent Trace Store](Persistent_Trace_Store.md) (3 shared connections)
- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (3 shared connections)
- [Trace Configuration & CLI Trace](Trace_Configuration_%26_CLI_Trace.md) (3 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (2 shared connections)
- [Trace Listing CLI](Trace_Listing_CLI.md) (2 shared connections)
- [Observability Entry & Trace Rendering](Observability_Entry_%26_Trace_Rendering.md) (2 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (2 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (1 shared connections)
- [Observability Installation & Isolation](Observability_Installation_%26_Isolation.md) (1 shared connections)

## Source Files

- `src/osc_assistant/observability/__init__.py`
- `src/osc_assistant/observability/store.py`
- `tests/test_trace_store.py`

## Audit Trail

- EXTRACTED: 44 (90%)
- INFERRED: 5 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*