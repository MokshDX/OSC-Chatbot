# FastAPI

---

## What it is

An async Python web framework built on Starlette (ASGI) and Pydantic. Request and
response models are ordinary type annotations; validation and OpenAPI documentation are
generated from them.

https://fastapi.tiangolo.com/ · https://www.starlette.io/ · ASGI: https://asgi.readthedocs.io/

---

## Why OSC uses it

**The pipeline is async end to end.** Provider HTTP calls, `asyncpg`, and the streaming
answer path are all coroutines. A WSGI framework would need a thread pool at every one
of those boundaries.

**Streaming is first-class.** The chat UI streams tokens over Server-Sent Events.
Starlette's `StreamingResponse` over an async generator is the natural shape for that,
and SSE — rather than WebSockets — because the traffic is one-directional and SSE
survives proxies, reconnects on its own, and needs no protocol upgrade.

**Pydantic is already a dependency.** Settings use `pydantic-settings`; golden sets use
Pydantic validation. Using it for HTTP schemas too means one validation library, one
mental model, and the project's rule — *validation belongs at the trust boundary* — is
implemented by the same tool everywhere it applies.

**OpenAPI comes free**, which matters for a service other teams will call.

---

## Where it is used

```
api/
├── app.py       routes, lifespan, error handling
├── schemas.py   Pydantic request/response models — the trust boundary
├── sse.py       Server-Sent Events framing
├── banner.py    the human-readable startup summary (stderr)
└── static/index.html   the bundled chat UI
```

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Liveness |
| `GET /api/status` | What is indexed |
| `POST /api/search` | Retrieval only |
| `POST /api/chat` | Answer, buffered or streamed |
| `GET /api/traces`, `/api/traces/{id}` | Recent traces — **development only** |

Note what is absent: **there is no write endpoint.** Ingestion is a CLI command, so the
service exposes no unauthenticated way to modify the corpus. That is deliberate, and it
is the only reason the current lack of authentication is merely bad rather than
catastrophic.

---

## How it integrates

**Lifespan owns the container.** `Container` is built at startup and
`Container.shutdown()` runs at shutdown, releasing every component that was actually
constructed. `cached_property` storing into the instance `__dict__` means its presence
there is exactly the record of what was built — so shutdown never constructs a component
just to close it.

**Errors are translated once.** An `AssistantError` handler maps the hierarchy to
structured responses. This is why *"never let a vendor exception escape a provider
adapter"* is a rule: an untranslated `asyncpg` error bypassed this handler entirely, and
the most common operational failure was also the worst reported.

**Startup speaks to two audiences.** A human summary on **stderr** — URLs, active
components, warnings about an empty index, mixed embedding models, or a non-development
environment with no auth — while structured JSON continues to **stdout** untouched. So
`./osc serve > run.log` still yields a clean parseable log, and the terminal still shows
where the service is listening.

**Every SSE exit emits a terminal event.** The stream handler once caught only
`AssistantError`, so an unexpected exception closed the connection with no terminal
event and left the UI spinning forever. Now every exit path emits one; unexpected
exceptions get a stable client message with the detail in the log.
`test_server_lifecycle.py` holds that regression.

---

## Alternatives considered

| Option | Why not |
|---|---|
| **Flask / Django** | WSGI. Async is bolted on, and this pipeline is async everywhere |
| **Starlette alone** | FastAPI *is* Starlette plus Pydantic integration and OpenAPI. Dropping it means hand-writing validation that Pydantic already does |
| **Litestar** | Genuinely comparable. FastAPI won on ecosystem familiarity — a new engineer is more likely to have used it, and that is a real maintenance property |
| **gRPC** | Better for service-to-service, worse for a browser UI and for `curl` |
| **WebSockets instead of SSE** | Bidirectional protocol for one-directional traffic. SSE reconnects natively and passes through proxies unchanged |

---

## Trade-offs accepted

**`response_model=None` on `/chat`.** The endpoint returns either JSON or a stream
depending on a request flag, which drops the JSON branch from the OpenAPI schema.
Splitting into `/chat` and `/chat/stream` is the fix, and it is an API break the bundled
UI would have to follow — **deferred deliberately rather than overlooked**.

**No authentication, rate limiting, or concurrency bound.** A request can hold a
connection for the full 120 s provider timeout, and nothing caps requests per user. The
service *says so* at every startup when `environment != development`, but the constraint
lives in prose rather than in the code path. The smallest fix — refuse to start when
`environment != "development"` and no auth is configured — is about ten lines and is a
named milestone.

**The bundled UI is minimal.** One static page. Deliberately: a richer client is
explicitly late in the implementation order, because the value is in the index and the
retrieval, not the chrome.

---

## Future evolution

1. **OIDC authentication**, with the resolved principal attached to every request and
   carried into retrieval so ACL filtering has somewhere to plug in.
2. **A production startup guard** — the ten lines above.
3. **Rate limiting per authenticated principal**, with a test that a burst is rejected.
4. **Split `/chat`**, once the UI can follow.
5. **Conversation persistence.** The API is stateless today; history is client-supplied,
   and the bundled UI does not send it — so follow-up turns are independent questions.

---

## Related

- [../architecture/observability.md](../architecture/observability.md) — the stdout/stderr split
- [python-tooling.md](python-tooling.md) — Pydantic, Typer, and the rest
