# Cross-Encoder Reranker

> 19 nodes

## Key Concepts

- **app.py** (47 connections) — `src/osc_assistant/api/app.py`
- **create_app()** (19 connections) — `src/osc_assistant/api/app.py`
- **banner.py** (11 connections) — `src/osc_assistant/api/banner.py`
- **startup_notes()** (10 connections) — `src/osc_assistant/api/banner.py`
- **describe_startup()** (7 connections) — `src/osc_assistant/api/banner.py`
- **_register_ui()** (5 connections) — `src/osc_assistant/api/app.py`
- **log_resolved_settings()** (5 connections) — `src/osc_assistant/settings.py`
- **FastAPI** (4 connections)
- **_register_error_handlers()** (4 connections) — `src/osc_assistant/api/app.py`
- **ErrorBody** (4 connections) — `src/osc_assistant/api/schemas.py`
- **api/__init__.py** (3 connections) — `src/osc_assistant/api/__init__.py`
- **describe_shutdown()** (3 connections) — `src/osc_assistant/api/banner.py`
- **FastAPI application. Thin by design: it validates input, calls one pipeline…** (1 connections) — `src/osc_assistant/api/app.py`
- **Build the ASGI application. Accepting settings makes the app constructible in…** (1 connections) — `src/osc_assistant/api/app.py`
- **Serve the bundled chat client at the site root. Registered outside the `/api`…** (1 connections) — `src/osc_assistant/api/app.py`
- **Human-facing startup and shutdown reporting for the service. The structured…** (1 connections) — `src/osc_assistant/api/banner.py`
- **Print where the service is listening and what it is running. Failures are…** (1 connections) — `src/osc_assistant/api/banner.py`
- **Conditions worth telling a developer about before their first request. Returned…** (1 connections) — `src/osc_assistant/api/banner.py`
- **Record what the configuration layers actually resolved to. Called from the…** (1 connections) — `src/osc_assistant/settings.py`

## Relationships

- [Persistent Trace Store Tests](Persistent_Trace_Store_Tests.md) (10 shared connections)
- [Evaluation Framework Rationale](Evaluation_Framework_Rationale.md) (7 shared connections)
- [Fusion & Provider Packages](Fusion_%26_Provider_Packages.md) (6 shared connections)
- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (6 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (5 shared connections)
- [RRF Fusion & Citation Parsing](RRF_Fusion_%26_Citation_Parsing.md) (5 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (4 shared connections)
- [Chat & Session Route Handlers](Chat_%26_Session_Route_Handlers.md) (4 shared connections)
- [Trace HTTP Endpoints](Trace_HTTP_Endpoints.md) (4 shared connections)
- [Chunking & Embedding Architecture](Chunking_%26_Embedding_Architecture.md) (2 shared connections)
- [API Layer Tests](API_Layer_Tests.md) (2 shared connections)
- [SSE Encoding](SSE_Encoding.md) (1 shared connections)

## Source Files

- `src/osc_assistant/api/__init__.py`
- `src/osc_assistant/api/app.py`
- `src/osc_assistant/api/banner.py`
- `src/osc_assistant/api/schemas.py`
- `src/osc_assistant/settings.py`

## Audit Trail

- EXTRACTED: 123 (95%)
- INFERRED: 6 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*