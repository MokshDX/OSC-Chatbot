"""Traces that outlive the process that produced them.

The in-memory recorder in `trace` is the right shape for the server: the process
is long-lived, so a ring buffer plus `/api/traces` answers "what did that request
just do?" with no storage at all. It is the wrong shape for the CLI, where the
process exits the moment the answer is printed — so a developer who did not think
to pass `--explain` has no way back to the trace.

**Why not just re-run with `--explain`.** Because a generation is not
deterministic. Re-running produces *a* trace, not *the* trace, and the answer being
investigated is usually the one that was odd. It also costs a full model call, and
it cannot explain a failure that already happened in CI or in a colleague's
terminal.

**Why a file rather than the database.** Storing traces in PostgreSQL is uniform
and queryable, and was rejected on two grounds: it puts write load on the primary
datastore for a debugging feature, and it makes tracing unavailable in exactly the
situation where it is most wanted — when the database is the thing that is broken.

**Why not OpenTelemetry yet.** It remains the right destination once traces leave
the host, and `Span` is deliberately OTel-shaped so that day is an exporter rather
than a rewrite. Running a collector to read a trace in a terminal is not.

So: an append-only JSONL file, one trace per line, in the same shape the HTTP
endpoint already serves — which means one renderer, one parser, and a format that
`grep` and `jq` already understand.

Bounded by rotation rather than by rewriting. Appending is O(1); keeping "the last
N traces" by rewriting the file would be O(n) on every request, which is a strange
cost to impose on the system in order to observe it.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Any

from ..logging import get_logger
from .trace import Span, Trace

log = get_logger(__name__)

DEFAULT_TRACE_DIR = Path(".osc")
TRACE_FILENAME = "traces.jsonl"
ROTATED_FILENAME = "traces.1.jsonl"


def trace_from_dict(payload: dict[str, Any]) -> Trace:
    """Rebuild a `Trace` from its serialised form.

    The inverse of `Trace.to_dict`, and the reason the file format and the HTTP
    response body are the same thing: a trace read from disk and a trace fetched
    from a running service are the same object by the time anything renders them.
    """
    return Trace(
        trace_id=payload["trace_id"],
        name=payload["name"],
        started_at=datetime.fromisoformat(payload["started_at"]),
        duration_ms=payload.get("duration_ms", 0.0),
        spans_dropped=payload.get("spans_dropped", 0),
        spans=[
            Span(
                name=span["name"],
                span_id=span["span_id"],
                parent_id=span["parent_id"],
                depth=span["depth"],
                offset_ms=span["offset_ms"],
                duration_ms=span["duration_ms"],
                attributes=span.get("attributes", {}),
                error=span.get("error"),
            )
            for span in payload.get("spans", [])
        ],
    )


class TraceStore:
    """A size-bounded, append-only log of completed traces.

    Two files: the one being written and the one before it. Two rather than one
    because rotation would otherwise discard every trace at the moment the limit is
    reached, which is reliably the moment someone is trying to read one.
    """

    def __init__(self, directory: Path = DEFAULT_TRACE_DIR, max_bytes: int = 5_000_000) -> None:
        self._directory = Path(directory)
        self._max_bytes = max_bytes

    @property
    def path(self) -> Path:
        return self._directory / TRACE_FILENAME

    @property
    def rotated_path(self) -> Path:
        return self._directory / ROTATED_FILENAME

    def append(self, trace: Trace) -> None:
        """Record one completed trace.

        Never raises. A read-only filesystem, a full disk or a permission problem
        must degrade to "no persisted traces", not to a failed request: this is
        instrumentation, and instrumentation that can break the thing it observes is
        a liability.
        """
        try:
            self._directory.mkdir(parents=True, exist_ok=True)
            self._rotate_if_needed()
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(trace.to_dict(), default=str) + "\n")
        except OSError as exc:
            log.debug("trace_store.write_failed", extra={"error": str(exc)})

    def recent(self, limit: int | None = None) -> list[Trace]:
        """Completed traces, most recent first."""
        found: list[Trace] = []
        for trace in self._read_backwards():
            found.append(trace)
            if limit is not None and len(found) >= limit:
                break
        return found

    def get(self, trace_id: str) -> Trace | None:
        """Look up by full id, or by a unique prefix — ids get pasted by hand."""
        for trace in self._read_backwards():
            if trace.trace_id == trace_id or trace.trace_id.startswith(trace_id):
                return trace
        return None

    def clear(self) -> None:
        for path in (self.path, self.rotated_path):
            path.unlink(missing_ok=True)

    def _rotate_if_needed(self) -> None:
        if not self.path.is_file() or self.path.stat().st_size < self._max_bytes:
            return
        # os.replace is atomic, so a reader concurrent with rotation sees one file
        # or the other and never a half-written one.
        os.replace(self.path, self.rotated_path)

    def _read_backwards(self) -> Iterator[Trace]:
        """Yield traces newest first, current file before rotated.

        Reads whole files rather than seeking from the end. The bound is a few
        megabytes and the caller is a developer running a command, so the simpler
        implementation wins.
        """
        # ponytail: whole-file read, bounded by max_bytes. Seek-from-end if the
        # rotation limit is ever raised past tens of megabytes.
        for path in (self.path, self.rotated_path):
            if not path.is_file():
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except OSError as exc:
                log.debug("trace_store.read_failed", extra={"error": str(exc)})
                continue
            for line in reversed(lines):
                trace = _parse_line(line)
                if trace is not None:
                    yield trace


def _parse_line(line: str) -> Trace | None:
    """Parse one record, skipping anything malformed.

    A truncated final line is expected rather than exceptional: the process writing
    it may have been killed mid-write. One bad record must not hide the good ones
    around it.
    """
    line = line.strip()
    if not line:
        return None
    try:
        return trace_from_dict(json.loads(line))
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None
