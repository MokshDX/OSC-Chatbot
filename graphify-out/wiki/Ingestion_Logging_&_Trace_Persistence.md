# Ingestion Logging & Trace Persistence

> 15 nodes · cohesion 0.15

## Key Concepts

- **trace.py** (23 connections) — `src/osc_assistant/observability/trace.py`
- **ingestion/pipeline.py** (16 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **get_logger()** (16 connections) — `src/osc_assistant/logging.py`
- **store.py** (11 connections) — `src/osc_assistant/observability/store.py`
- **.set_text()** (4 connections) — `src/osc_assistant/observability/trace.py`
- **_log_span()** (3 connections) — `src/osc_assistant/observability/trace.py`
- **TraceConfig** (3 connections) — `src/osc_assistant/observability/trace.py`
- **_truncate()** (2 connections) — `src/osc_assistant/observability/trace.py`
- **Logger** (1 connections)
- **The ingestion pipeline: documents in, embedded chunks in the store. Idempotent…** (1 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **Traces that outlive the process that produced them. The in-memory recorder in…** (1 connections) — `src/osc_assistant/observability/store.py`
- **Execution tracing: how a request actually spent its time. Structured logs…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Attach human text (a query, an answer, a chunk excerpt). Kept separate from…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Emit one completed span as a TRACE record. Guarded by `isEnabledFor` before…** (1 connections) — `src/osc_assistant/observability/trace.py`
- **Process-wide tracing behaviour, set once from settings at startup. Module-level…** (1 connections) — `src/osc_assistant/observability/trace.py`

## Relationships

- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (12 shared connections)
- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (8 shared connections)
- [Logging Subsystem Core](Logging_Subsystem_Core.md) (4 shared connections)
- [Whitespace Normalisation & Error Base](Whitespace_Normalisation_%26_Error_Base.md) (3 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (3 shared connections)
- [Observability Entry & Trace Rendering](Observability_Entry_%26_Trace_Rendering.md) (3 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (2 shared connections)
- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (2 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (2 shared connections)
- [Trace Sink & JSONL Parsing](Trace_Sink_%26_JSONL_Parsing.md) (2 shared connections)
- [Trace Configuration & CLI Trace](Trace_Configuration_%26_CLI_Trace.md) (2 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (1 shared connections)

## Source Files

- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/logging.py`
- `src/osc_assistant/observability/store.py`
- `src/osc_assistant/observability/trace.py`

## Audit Trail

- EXTRACTED: 85 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*