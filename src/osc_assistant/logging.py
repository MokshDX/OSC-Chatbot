"""Structured logging: what the system did, recorded durably.

Tracing and logging answer different questions and both are needed. A **trace**
explains *one execution* — where the time went, how the data changed between
stages, which stage raised. A **log** records *everything that happened*, across
every execution, in the order it happened, and survives to be grepped next week.
`observability/` owns the first; this module owns the second.

## What is here

Records are single-line JSON on stdout **and** appended to a rotating file, so the
same event serves a terminal, a log shipper and `tail -f` without being formatted
three ways.

    log = get_logger(__name__)
    log.info("retrieval.complete", extra={"chunk_ids": ids, "latency_ms": 41})

Five levels, TRACE through ERROR. TRACE (5) sits below DEBUG and is where the
per-span firehose lives — see `observability.trace`. Emit it with
`log.log(TRACE, ...)` rather than a monkeypatched `log.trace()`, because adding a
method to `logging.Logger` is a global mutation that `mypy --strict` cannot see
through and every other library would inherit.

## Three properties that are load-bearing

**Writing is off the calling thread.** Every handler sits behind a
`QueueHandler`/`QueueListener` pair, so a log call costs an enqueue and the disk
I/O happens on a background thread. Logging that blocks a request on `fsync` is
logging that gets removed the first time it shows up in a latency profile.

**Every record carries its trace id.** A filter reads the active trace from the
tracer's context var and stamps it on the record. That single field is what turns
two independent systems into one: find a slow request in the logs, then expand it
with `./osc trace <id>`.

**Disk is bounded by construction.** Size-based rotation with a backup count, so
the ceiling is `max_bytes * (backup_count + 1)` and the oldest file is deleted
rather than retained. A time-based policy would give predictable windows and no
ceiling, which is the wrong guarantee for a service that can get busy.

## The audit stream is separate, deliberately

`audit.log` carries one record per answered question — what was asked, what was
retrieved, what was answered, what it cost. It is separate from `osc.log` because
the two have different lifetimes and different readers: operational logs roll off
in hours under TRACE, and "which passages did we show this user in March" needs to
outlive that. Keeping them in one stream would mean choosing one retention policy
for both, and the debug firehose would win.
"""

from __future__ import annotations

import atexit
import json
import logging
import logging.handlers
import queue
import sys
from contextlib import suppress
from pathlib import Path
from typing import Any

TRACE = 5
"""Below DEBUG. Per-span pipeline detail; off unless explicitly enabled."""

logging.addLevelName(TRACE, "TRACE")

DEFAULT_LOG_DIR = Path(".osc/logs")
OPERATIONAL_LOG = "osc.log"
AUDIT_LOG = "audit.log"

AUDIT_LOGGER = "osc.audit"
"""Its own logger name so the audit handler can select on it and nothing else."""

# Attributes present on every LogRecord; anything else was supplied by the caller
# via `extra` and is therefore structured context worth emitting.
_STANDARD_ATTRS = frozenset(logging.LogRecord("", 0, "", 0, "", None, None).__dict__) | {
    "message",
    "asctime",
    "taskName",
}

REDACTED = "[redacted]"

SECRET_KEY_HINTS = ("key", "token", "secret", "password", "dsn", "credential", "authorization")
"""Substrings that mark a field as a credential. Matched case-insensitively.

Deliberately matched on the *field name* rather than on the value: a heuristic that
inspects values for things that look like secrets both misses novel formats and
mangles legitimate content. A field called `api_key` is a credential regardless of
what it holds.
"""

NEVER_REDACT = frozenset(
    {
        "input_tokens",
        "output_tokens",
        "cached_input_tokens",
        "total_tokens",
        "max_tokens",
        "token_count",
        "tokens",
        "chunk_ids",
        "cited_chunk_ids",
        "retrieved_chunk_ids",
        "keys",
    }
)
"""Fields that contain a hint substring and are not credentials.

Checked before `SECRET_KEY_HINTS`, because the substring heuristic is deliberately
broad and therefore produces false positives on exactly the fields most worth
keeping. `input_tokens` contains "token" and is a **cost measurement**; redacting it
silently destroys every token and spend analysis in the log — which is what this
list exists to prevent, and what a live run caught.
"""

PAYLOAD_KEYS = frozenset(
    {"question", "answer", "query", "original_query", "text", "content", "prompt", "reply"}
)
"""Fields carrying corpus or user text, suppressed unless payload logging is on.

Replaced with a character count rather than dropped, so a record still shows that
there *was* a question of roughly this size — which is most of what a latency
investigation needs, and none of what a privacy review objects to.
"""


class JsonFormatter(logging.Formatter):
    """Renders records as single-line JSON."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in _STANDARD_ATTRS:
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


class TraceContextFilter(logging.Filter):
    """Stamps the active trace id onto every record.

    This is the seam between the two observability systems. Without it, logs and
    traces are two piles of facts about the same request with nothing joining them;
    with it, any log line can be expanded into a full stage-by-stage waterfall.

    Imported lazily inside `filter` because `observability` imports this module for
    its own logger, and a module-level import here would close the cycle.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if getattr(record, "trace_id", None):
            return True  # An explicit trace_id on the call site wins.
        try:
            from .observability.trace import current_trace_id

            active = current_trace_id()
        except Exception:  # pragma: no cover - defensive; tracing must never break logging
            active = ""
        if active:
            record.trace_id = active
        return True


class RedactionFilter(logging.Filter):
    """Removes credentials, and reduces corpus text to a length unless allowed.

    A filter rather than a formatter concern, because it must apply identically to
    every destination: a secret suppressed on stdout and written to disk is a
    secret that leaked.
    """

    def __init__(self, capture_payloads: bool = False) -> None:
        super().__init__()
        self._capture_payloads = capture_payloads

    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in list(record.__dict__.items()):
            if key in _STANDARD_ATTRS:
                continue
            lowered = key.lower()
            if lowered in NEVER_REDACT:
                continue
            if any(hint in lowered for hint in SECRET_KEY_HINTS):
                record.__dict__[key] = REDACTED
            elif not self._capture_payloads and key in PAYLOAD_KEYS and isinstance(value, str):
                record.__dict__[key] = f"<{len(value)} chars>"
        return True


class _NonDestructiveQueueHandler(logging.handlers.QueueHandler):
    """A `QueueHandler` that does not discard the exception it was given.

    The stdlib `prepare()` formats the record and then clears `exc_info`,
    `exc_text` and `args`, because a queue may cross a *process* boundary and a
    traceback object cannot be pickled. That is the right default and the wrong one
    here: this queue is consumed by a thread in the same process, so the record can
    be passed through intact — and the downstream `JsonFormatter` needs `exc_info`
    to emit the `exception` field at all.

    Without this override, `log.exception(...)` records the event and silently
    loses the traceback, which is the single worst thing a logging system can do
    quietly. A test asserts the traceback survives.
    """

    def prepare(self, record: logging.LogRecord) -> logging.LogRecord:
        return record


class _AuditOnly(logging.Filter):
    """Routes only audit records to the audit file."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.name == AUDIT_LOGGER or record.name.startswith(AUDIT_LOGGER + ".")


class _ExcludeAudit(logging.Filter):
    """Keeps audit records out of the operational stream.

    They would otherwise appear twice on disk under two retention policies, which
    is the specific confusion two streams exist to avoid.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        return not (record.name == AUDIT_LOGGER or record.name.startswith(AUDIT_LOGGER + "."))


_listener: logging.handlers.QueueListener | None = None
_log_directory: Path | None = None


def configure_logging(
    level: str = "INFO",
    fmt: str = "json",
    *,
    console: bool = True,
    console_level: str | None = None,
    directory: Path | str | None = None,
    max_bytes: int = 10_000_000,
    backup_count: int = 5,
    audit: bool = True,
    audit_max_bytes: int = 10_000_000,
    audit_backup_count: int = 20,
    capture_payloads: bool = False,
) -> None:
    """Install the logging stack. Safe to call more than once.

    Parameters are primitives rather than a settings object for the same reason
    `configure_observability` takes primitives: this module must stay importable by
    `settings` without a cycle, and a test must be able to configure it in one line
    without constructing the world.

    `directory=None` disables file logging entirely — which is what the test suite
    uses, and what a containerised deployment that ships stdout to a collector
    wants. Console output is unchanged from before this module grew: JSON on
    stdout, so `./osc serve > run.log` still yields a clean parseable log.

    `console_level` raises the bar for the terminal *only*. This is what lets an
    interactive CLI command stay quiet while the file still records everything at
    `level`: the operator sees their answer, and the full record is on disk
    afterwards. Without it, quietening the terminal would also throw away the log,
    which is the opposite of what a persistent log is for.
    """
    global _listener, _log_directory

    shutdown_logging()

    formatter: logging.Formatter = (
        JsonFormatter()
        if fmt == "json"
        else logging.Formatter("%(asctime)s %(levelname)-8s %(name)s  %(message)s")
    )

    file_level = logging.getLevelName(level.upper())
    terminal_level = (
        logging.getLevelName(console_level.upper()) if console_level else file_level
    )

    handlers: list[logging.Handler] = []
    if console:
        stream = logging.StreamHandler(sys.stdout)
        stream.setFormatter(formatter)
        stream.addFilter(_ExcludeAudit())
        stream.setLevel(terminal_level)
        handlers.append(stream)

    _log_directory = None
    if directory is not None:
        path = Path(directory)
        try:
            path.mkdir(parents=True, exist_ok=True)
            operational = logging.handlers.RotatingFileHandler(
                path / OPERATIONAL_LOG,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
                delay=True,
            )
            operational.setFormatter(JsonFormatter())
            operational.addFilter(_ExcludeAudit())
            operational.setLevel(file_level)
            handlers.append(operational)

            if audit:
                audit_handler = logging.handlers.RotatingFileHandler(
                    path / AUDIT_LOG,
                    maxBytes=audit_max_bytes,
                    backupCount=audit_backup_count,
                    encoding="utf-8",
                    delay=True,
                )
                audit_handler.setFormatter(JsonFormatter())
                audit_handler.addFilter(_AuditOnly())
                # Audit records are INFO and must survive a coarser root level:
                # raising the root to WARNING to quieten a noisy deployment must
                # not silently stop recording what was answered.
                audit_handler.setLevel(logging.INFO)
                handlers.append(audit_handler)
            _log_directory = path
        # Broad by intent: an unwritable log directory is an operational problem,
        # not a reason for the process to refuse to start. Console logging still
        # works, and the failure is reported through it.
        except OSError as exc:
            logging.getLogger(__name__).warning(
                "logging.file_unavailable",
                extra={"directory": str(path), "error": str(exc)},
            )

    root = logging.getLogger()
    root.handlers.clear()

    if handlers:
        # Unbounded queue: dropping a log line to bound memory trades a diagnostic
        # for a resource guarantee that the rotating file already provides.
        record_queue: queue.SimpleQueue[Any] = queue.SimpleQueue()
        entry = _NonDestructiveQueueHandler(record_queue)
        entry.addFilter(TraceContextFilter())
        entry.addFilter(RedactionFilter(capture_payloads))
        root.addHandler(entry)

        _listener = logging.handlers.QueueListener(
            record_queue, *handlers, respect_handler_level=True
        )
        _listener.start()

    # The root gates before any handler sees a record, so it has to sit at the
    # most verbose of the two. Per-handler levels do the actual separating.
    root.setLevel(min(file_level, terminal_level))

    # Audit must reach its handler even when the root level is coarser, and must
    # not be suppressed by a caller raising the root to WARNING.
    audit_logger = logging.getLogger(AUDIT_LOGGER)
    audit_logger.setLevel(logging.INFO)

    # Third-party libraries are pinned to WARNING regardless of our level.
    #
    # Without this, raising the level to TRACE to watch our own pipeline also turns
    # on every vendor SDK's debug stream — and those emit unstructured prose into a
    # JSONL file ("Sending HTTP Request: POST ..."), carry request bodies that may
    # contain corpus text, and drown the records worth reading. A live TRACE run
    # caught the openai client doing exactly that.
    #
    # A denylist rather than scoping our level to the `osc_assistant` logger, because
    # `get_logger(name)` is documented to work for any name and the tests rely on it.
    for noisy in (
        "httpx",
        "httpcore",
        "asyncio",
        "openai",
        "anthropic",
        "urllib3",
        "asyncpg",
        "langchain",
        "langchain_core",
        "sentence_transformers",
        "google",
        "google_genai",
        "filelock",
        "multipart",
    ):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def shutdown_logging() -> None:
    """Flush and stop the background writer. Idempotent.

    Registered with `atexit` and called at the start of every reconfiguration.
    Without it a reconfigured process leaks a listener thread per call, and a
    short-lived CLI command can exit with records still queued.
    """
    global _listener
    if _listener is not None:
        # Suppressed: shutdown runs on the failure path and at interpreter exit,
        # where a handler that cannot close must not mask the original error.
        with suppress(Exception):
            _listener.stop()
        for handler in _listener.handlers:
            with suppress(Exception):
                handler.close()
        _listener = None


atexit.register(shutdown_logging)


def log_directory() -> Path | None:
    """Where logs are being written, or None when file logging is off."""
    return _log_directory


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def audit(event: str, **fields: Any) -> None:
    """Record one auditable operation.

    Separate from `get_logger(...).info(...)` so that what belongs in the audit
    trail is a deliberate decision at the call site rather than a property of which
    logger happened to be in scope. Routed to `audit.log` and excluded from the
    operational stream.
    """
    logging.getLogger(AUDIT_LOGGER).info(event, extra=fields)
