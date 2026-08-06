# ADR 0009 — Persistent logging on the standard library, fed by the span stream

**Status:** Accepted · **Date:** Phase 5

---

## Context

OSC had structured logging — a JSON formatter on stdlib `logging`, 30 call sites
across 13 modules — and it wrote to **stdout only**. Nothing persisted. A CLI
command's log died with the process, exactly like its trace did before
[ADR 0004](0004-persistent-tracing.md), and for the same reason: nobody had needed
it until they did.

Four gaps followed from that:

- **No history.** "Did this fail overnight?" had no answer.
- **No correlation.** Traces carried a `trace_id`; log records did not, so the two
  systems described the same request with nothing joining them.
- **No coverage.** 30 call sites across a system with roughly a dozen pipeline
  stages, four providers in the default path and two entry points.
- **No level below DEBUG**, so there was nowhere to put per-stage detail that would
  be unbearable at DEBUG.

The constraint that shaped the answer: the pipelines, providers, chunkers,
evaluation harness and LangChain integration were explicitly out of scope for
modification. Coverage had to come from somewhere that was not new call sites in
those modules.

## Decision

**Grow `logging.py` into the logging system. Take rotation, retention, async
writing and levels from the standard library. Take coverage from the span stream.**

### The span bridge is the load-bearing decision

Every stage of OSC is already a `span()` carrying structured attributes. One hook
in `trace.py`'s span-exit path emits a TRACE record per stage:

```python
finally:
    entry.duration_ms = ...
    _log_span(entry, current.trace_id)
```

That gives `retrieve`, `embed_query`, `search`, `threshold`, `rerank`, `generate`,
`finalise`, `load_hashes`, `document`, `chunk`, `embed`, `store` and `prune` their
log lines **with no change to any of those modules**. It is also the honest reading
of the project's own rule — *instrument the pipeline, not the adapter* — extended
one step: instrument once, and let both observability systems read the same
instrumentation.

What the span stream cannot supply is *which command produced it*. Every command
initialises identically, so `load()` emits one `cli.command` record naming the
command and its flags. It reads `sys.argv` rather than the click context, because
typer invokes a command's callback outside the context `click.get_current_context`
reads; the positional tail is payload and is gated on `capture_payloads`.

### Everything else is stdlib

| Requirement | Mechanism |
|---|---|
| Persistence, rotation, retention | `RotatingFileHandler(maxBytes, backupCount)` |
| Non-blocking writes | `QueueHandler` + `QueueListener` |
| TRACE level | `addLevelName(5, "TRACE")`, emitted via `log.log(TRACE, ...)` |
| Trace correlation | a `logging.Filter` reading the tracer's context var |
| Redaction | a `logging.Filter` on the queue entry |

### Size-based rotation, not time-based

`max_bytes * (backup_count + 1)` is a **disk ceiling by construction**. A
`TimedRotatingFileHandler` gives predictable windows ("last 14 days") and no ceiling
at all — one busy day can produce an arbitrarily large file. For a service that can
get busy, bounded disk is the guarantee worth having.

### Two streams

`osc.log` (operational) and `audit.log` (one record per answered question, longer
retention, pinned at INFO so a coarser root level cannot silence it).

### TRACE is off by default

Span logging costs one `isEnabledFor` check at INFO. Operators opt in.

## Alternatives considered

**structlog / loguru.** Both are good. Neither earns a dependency here: the formatter
is 15 lines, the filters are 20, and rotation and async writing come from the
standard library either way. `logging.py`'s docstring has said "implemented on the
standard library to avoid a dependency for ~50 lines of formatter" since Phase 1;
the module has roughly quadrupled and the reasoning has not changed. A dependency
would also put a third-party API on the one code path that must keep working while
everything else is broken.

**Hand-written log lines in every pipeline.** The obvious way to get coverage, and it
would have meant editing retrieval, ingestion, generation, chunking and the
providers — all out of scope — *and* maintaining a second set of instrumentation
that drifts from the spans on the first change nobody makes twice.

**LangChain callbacks for provider-level logging.** Same objection as
[ADR 0002](0002-langchain-scope.md) raised for tracing: callbacks observe LangChain
runs, and most of this pipeline is not one.

**Log to the database.** Same objection as ADR 0004: it puts write load on the
primary datastore for a debugging feature, and makes logging unavailable in exactly
the situation where it is most wanted.

**Replace the trace store with logs.** Tempting — one persistence mechanism instead
of two. Rejected: a trace is a *tree* and a log is a *stream*, and reassembling a
waterfall from interleaved lines across concurrent requests is work the trace store
already avoids. They persist separately and are joined by `trace_id`.

**Time-based rotation, or both.** Covered above; "both" needs a custom handler
subclass for a guarantee size-based already provides.

## Consequences

**What it buys.**

- Logs survive the process. `./osc logs`, `tail -f`, `grep`, `jq`.
- Any log line expands into a full trace via `trace_id`.
- Full pipeline visibility at TRACE, at zero cost when unused, with no new call
  sites in any pipeline.
- An audit trail with its own retention.
- Bounded disk: ~60 MB operational, ~210 MB audit at defaults.

**What it costs.**

- **A background thread per process.** Stopped by `atexit` and by every
  reconfiguration; `shutdown_logging()` is idempotent and tested.
- **Records can be lost on a hard kill.** Queued records not yet written die with a
  `SIGKILL`. The trade for not blocking on `fsync`.
- **The queue is unbounded**, so a pathological burst grows memory rather than
  dropping records.
- **Redaction is a name heuristic**, so it is both over- and under-inclusive. The
  over-inclusive half bit immediately — see below.
- **Rotation is size-based**, so retention windows are not predictable.

**Two defects found by running it, both worth recording.**

*`QueueHandler.prepare()` strips `exc_info`* to make records picklable across a
process boundary. Our queue is consumed by a thread in the same process, so the
stripping bought nothing and silently deleted every traceback — the worst thing a
logging system can do quietly. Fixed with a `prepare()` override; a test asserts
tracebacks survive.

*The redaction heuristic redacted token counts.* `input_tokens` contains "token", so
every cost measurement in the log became `[redacted]`. Found by reading a real audit
record, not by a test. Fixed with a `NEVER_REDACT` allowlist checked first, and
pinned by a regression test.

Both are the same lesson: the failure modes of a logging system are silent, and the
only way to find them is to read the output of a real run.
