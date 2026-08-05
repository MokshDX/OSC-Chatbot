# ADR 0004 — Persist traces to a bounded JSONL file

**Status:** Accepted · **Date:** Phase 3

---

## Context

Phase 2 added execution tracing: every significant stage of ingestion and question
answering is a timed span, and one request produces one trace. Traces were held in an
in-memory ring buffer.

That works for the server. The process is long-lived, so `/api/traces` answers *"what
did that request just do?"* with no storage at all.

**It does not work for the CLI**, where the process exits the moment the answer is
printed. A developer who did not think to pass `--explain` had no way back to the trace,
and `./osc trace` could only read from a running server. The situation in which a trace
is most wanted — something went wrong and you did not anticipate it — was precisely the
situation in which there was none.

Re-running is not a workaround. **A generation is not deterministic**: re-running
produces *a* trace, not *the* trace, and the answer under investigation is usually the
odd one out.

## Decision

**A bounded, append-only JSONL log** (`observability/store.py`), written to
`observability.trace_dir` (default `.osc/`), rotated at `max_trace_file_bytes` with two
files kept.

Plus **auto-explain on failure**: a failed command prints its trace before the error,
which needs no persistence at all.

Three properties are deliberate:

- **Rotation, not rewriting.** Appending is O(1); a log that rewrites itself to stay
  bounded is a log that gets slower as it fills.
- **Writing never raises.** Instrumentation that can break the thing it observes is a
  liability precisely because it is trusted.
- **It reuses the payload the HTTP endpoint already serves**, so one parser and one
  renderer cover both sources.

`Span` stays OTel-shaped, so an exporter remains an addition rather than a rewrite.

## Alternatives considered

| Option | Rejected because |
|---|---|
| **Re-run with `--explain`** | A generation is not deterministic — it produces *a* trace, not *the* trace. It also costs a full model call, and cannot explain a failure that already happened in CI |
| **A `traces` table in PostgreSQL** | Puts write load on the primary datastore for a debugging feature, and makes tracing unavailable in exactly the situation where it is most wanted: **when the database is what is broken** |
| **OpenTelemetry + a collector** | The right destination once traces leave the host, and the wrong answer for reading a trace in a terminal on a laptop. Requires a service to be running before you can debug why nothing is running |
| **A daemon or a Unix socket** | A background process whose job is to let you read a trace is worse than the problem it solves |
| **Structured logs only** | The information is all there and the *shape* is not. A waterfall showing that rerank took 80% of the request is a different artefact from twelve log lines containing the same durations |

## Consequences

**What it buys.**

- `./osc traces` (with `--failed`, `--name`, `--slower-than`) and `./osc trace [id]`
  work for one-shot commands, across process boundaries, and in CI.
- No service, no schema, no migration, no new dependency.
- The evaluation harness gets it for free: every case records a `trace_id`, so a bad
  score in a run that finished an hour ago is still expandable into a waterfall. That
  was not the original motivation and is now one of the main uses.
- `test_trace_store.py` covers cross-process readability, rotation, malformed lines and
  unwritable directories.

**What it costs.**

- **Traces are process-local.** The log lives on one host. It answers "what happened
  recently, here", not "what happened last Tuesday across the fleet". That needs the
  exporter.
- **Bounded means lossy.** Past `max_trace_file_bytes` × 2, old traces are gone. Fine
  for a debugging aid; not an audit log, and must never be mistaken for one.
- **Trace reads are whole-file.** `_read_backwards` reads both files to serve twenty
  summaries. Bounded at 5 MB and fine there; marked in the source with a `ponytail:`
  comment naming seek-from-end as the upgrade if the limit rises.
- **Traces may contain corpus text.** Questions, rewritten queries and answers are
  recorded by default. Mitigated by `capture_text: false` — which retains every timing,
  count and stage while reducing text to a length — and by refusing the HTTP trace
  endpoints outside `environment: development`, a check **deliberately not overridable
  by configuration** because no endpoint on this service is authenticated yet.
- **A file on disk in a container is ephemeral.** Deployment will need a volume or the
  exporter.

**Next step.** An OTel exporter behind a configuration flag, with the local log retained
as the default. `Span` is already shaped for it; this is an addition, not a migration.
