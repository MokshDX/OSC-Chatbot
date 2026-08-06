# Observability Entry & Trace Rendering

> 13 nodes · cohesion 0.23

## Key Concepts

- **observability/__init__.py** (21 connections) — `src/osc_assistant/observability/__init__.py`
- **render.py** (10 connections) — `src/osc_assistant/observability/render.py`
- **render_waterfall()** (10 connections) — `src/osc_assistant/observability/render.py`
- **render_summary()** (7 connections) — `src/osc_assistant/observability/render.py`
- **_details()** (5 connections) — `src/osc_assistant/observability/render.py`
- **test_the_waterfall_renders_every_span_and_marks_failures()** (4 connections) — `tests/test_observability.py`
- **_label()** (3 connections) — `src/osc_assistant/observability/render.py`
- **_short()** (2 connections) — `src/osc_assistant/observability/render.py`
- **Observability: tracing, persistence, and the rendering of traces. Three modules…** (1 connections) — `src/osc_assistant/observability/__init__.py`
- **Rendering a trace for a human. Separate from `trace` because collection and…** (1 connections) — `src/osc_assistant/observability/render.py`
- **Draw the trace as an indented waterfall. Bars are positioned by `offset_ms` and…** (1 connections) — `src/osc_assistant/observability/render.py`
- **One line: id, name, duration, span count, outcome.** (1 connections) — `src/osc_assistant/observability/render.py`
- **The first few attributes, plus any error. Truncated on purpose: a waterfall is…** (1 connections) — `src/osc_assistant/observability/render.py`

## Relationships

- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (8 shared connections)
- [Trace Configuration & CLI Trace](Trace_Configuration_%26_CLI_Trace.md) (6 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (3 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (3 shared connections)
- [Trace Sink & JSONL Parsing](Trace_Sink_%26_JSONL_Parsing.md) (2 shared connections)
- [Observability Installation & Isolation](Observability_Installation_%26_Isolation.md) (2 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (2 shared connections)
- [Persistent Trace Store](Persistent_Trace_Store.md) (1 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (1 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (1 shared connections)
- [Trace Store Tests](Trace_Store_Tests.md) (1 shared connections)
- [Trace Listing CLI](Trace_Listing_CLI.md) (1 shared connections)

## Source Files

- `src/osc_assistant/observability/__init__.py`
- `src/osc_assistant/observability/render.py`
- `tests/test_observability.py`

## Audit Trail

- EXTRACTED: 61 (91%)
- INFERRED: 6 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*