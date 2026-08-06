# FastAPI Application Assembly

> 18 nodes · cohesion 0.18

## Key Concepts

- **app.py** (52 connections) — `src/osc_assistant/api/app.py`
- **create_app()** (20 connections) — `src/osc_assistant/api/app.py`
- **log_resolved_settings()** (6 connections) — `src/osc_assistant/settings.py`
- **_register_ui()** (5 connections) — `src/osc_assistant/api/app.py`
- **FastAPI** (4 connections)
- **_register_error_handlers()** (4 connections) — `src/osc_assistant/api/app.py`
- **ErrorBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **encode_event()** (4 connections) — `src/osc_assistant/api/sse.py`
- **describe_shutdown()** (3 connections) — `src/osc_assistant/api/banner.py`
- **api/__init__.py** (3 connections) — `src/osc_assistant/api/__init__.py`
- **sse.py** (3 connections) — `src/osc_assistant/api/sse.py`
- **FastAPI application. Thin by design: it validates input, calls one pipeline…** (1 connections) — `src/osc_assistant/api/app.py`
- **Serve the bundled chat client at the site root. Registered outside the `/api`…** (1 connections) — `src/osc_assistant/api/app.py`
- **Build the ASGI application. Accepting settings makes the app constructible in…** (1 connections) — `src/osc_assistant/api/app.py`
- **Any** (1 connections)
- **Server-sent event encoding. SSE rather than WebSockets: the stream is one-…** (1 connections) — `src/osc_assistant/api/sse.py`
- **Encode one named SSE frame. The payload is serialised without literal newlines…** (1 connections) — `src/osc_assistant/api/sse.py`
- **Record what the configuration layers actually resolved to. Called from the…** (1 connections) — `src/osc_assistant/settings.py`

## Relationships

- [API Request & Response Schemas](API_Request_%26_Response_Schemas.md) (10 shared connections)
- [Chat & Health Endpoints](Chat_%26_Health_Endpoints.md) (7 shared connections)
- [Startup Banner & Lifecycle](Startup_Banner_%26_Lifecycle.md) (6 shared connections)
- [Trace & Status Endpoints](Trace_%26_Status_Endpoints.md) (5 shared connections)
- [Server Lifecycle Tests](Server_Lifecycle_Tests.md) (4 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (3 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (3 shared connections)
- [Logging Subsystem Core](Logging_Subsystem_Core.md) (3 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (3 shared connections)
- [Container Lifecycle & E2E](Container_Lifecycle_%26_E2E.md) (2 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (2 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (2 shared connections)

## Source Files

- `src/osc_assistant/api/__init__.py`
- `src/osc_assistant/api/app.py`
- `src/osc_assistant/api/banner.py`
- `src/osc_assistant/api/schemas.py`
- `src/osc_assistant/api/sse.py`
- `src/osc_assistant/settings.py`

## Audit Trail

- EXTRACTED: 112 (97%)
- INFERRED: 3 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*