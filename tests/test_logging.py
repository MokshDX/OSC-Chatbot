"""Persistent logging tests.

Logging is the system that gets read when something has already gone wrong, which
makes two failure modes worse than a missing feature: a log that silently stopped
recording, and a log that recorded something it should not have. Most of what is
here tests one of those two.

Records are written on a background thread, so every test that reads a file calls
`shutdown_logging()` first. That is the flush, and it is deterministic — polling
for the file to grow would make the suite timing-dependent on a machine under load.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from osc_assistant.cli._shared import log_command
from osc_assistant.logging import (
    AUDIT_LOG,
    OPERATIONAL_LOG,
    REDACTED,
    TRACE,
    audit,
    configure_logging,
    get_logger,
    log_directory,
    shutdown_logging,
)
from osc_assistant.observability import configure_observability, span, trace
from osc_assistant.settings import load_settings


@pytest.fixture(autouse=True)
def _restore_logging():
    """Leave the root logger as it was found.

    The handler stack and the listener thread are process-global. A test that
    reconfigured them and did not clean up would silently change the behaviour of
    every test that ran after it, in file order.
    """
    yield
    shutdown_logging()
    logging.getLogger().handlers.clear()


def _records(path: Path) -> list[dict]:
    """Every JSON record in a log file, flushed and parsed."""
    shutdown_logging()
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


# ------------------------------------------------------------------- creation


def test_a_log_file_is_created_and_records_land_in_it(tmp_path: Path):
    configure_logging("INFO", directory=tmp_path, console=False)
    get_logger("t").info("thing.happened", extra={"count": 3})

    records = _records(tmp_path / OPERATIONAL_LOG)

    assert len(records) == 1
    assert records[0]["event"] == "thing.happened"
    assert records[0]["count"] == 3
    assert records[0]["level"] == "INFO"
    assert records[0]["logger"] == "t"
    assert records[0]["timestamp"]


def test_file_logging_is_off_when_no_directory_is_configured(tmp_path: Path):
    configure_logging("INFO", directory=None, console=False)
    get_logger("t").info("thing.happened")
    shutdown_logging()

    assert log_directory() is None
    assert not (tmp_path / OPERATIONAL_LOG).exists()


@pytest.mark.parametrize("value", ["", "null", "NONE", "  "])
def test_the_environment_can_disable_file_logging(value: str, monkeypatch):
    """A container configures through the environment, not through YAML.

    An environment variable is always a string, so without the validator
    `OSC_LOGGING__DIRECTORY=null` becomes a *relative directory named `null`* and an
    empty value becomes the working directory — both silently creating log files
    instead of disabling them. Both were observed in a repository checkout.
    """
    monkeypatch.setenv("OSC_LOGGING__DIRECTORY", value)

    assert load_settings().logging.directory is None


def test_a_real_directory_is_still_honoured_from_the_environment(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("OSC_LOGGING__DIRECTORY", str(tmp_path / "logs"))

    assert load_settings().logging.directory == tmp_path / "logs"


def test_the_directory_is_created_if_it_does_not_exist(tmp_path: Path):
    nested = tmp_path / "deep" / "logs"
    configure_logging("INFO", directory=nested, console=False)
    get_logger("t").info("thing.happened")

    assert _records(nested / OPERATIONAL_LOG)


# ------------------------------------------------------------------- rotation


def test_the_log_rotates_at_the_configured_size(tmp_path: Path):
    configure_logging("INFO", directory=tmp_path, console=False, max_bytes=2048, backup_count=3)
    log = get_logger("t")
    for index in range(200):
        log.info("filler", extra={"index": index, "padding": "x" * 200})
    shutdown_logging()

    assert (tmp_path / OPERATIONAL_LOG).exists()
    assert (tmp_path / f"{OPERATIONAL_LOG}.1").exists(), "rotation never fired"


def test_retention_deletes_the_oldest_rather_than_keeping_it(tmp_path: Path):
    """The property that makes disk bounded rather than merely monitored."""
    configure_logging("INFO", directory=tmp_path, console=False, max_bytes=1024, backup_count=2)
    log = get_logger("t")
    for index in range(500):
        log.info("filler", extra={"index": index, "padding": "x" * 200})
    shutdown_logging()

    rotated = sorted(tmp_path.glob(f"{OPERATIONAL_LOG}.*"))
    # backup_count=2 means .1 and .2 exist and .3 never does, however much is written.
    assert len(rotated) == 2
    assert not (tmp_path / f"{OPERATIONAL_LOG}.3").exists()


def test_disk_stays_under_the_configured_ceiling(tmp_path: Path):
    max_bytes, backups = 2048, 2
    configure_logging(
        "INFO", directory=tmp_path, console=False, max_bytes=max_bytes, backup_count=backups
    )
    log = get_logger("t")
    for index in range(1000):
        log.info("filler", extra={"index": index, "padding": "x" * 200})
    shutdown_logging()

    total = sum(p.stat().st_size for p in tmp_path.glob(f"{OPERATIONAL_LOG}*"))
    # One rotation's worth of slack: a record is never split across files, so the
    # active file can exceed max_bytes by the size of the record that triggered it.
    assert total <= max_bytes * (backups + 1) * 2


# -------------------------------------------------------------------- levels


def test_records_below_the_configured_level_are_not_written(tmp_path: Path):
    configure_logging("INFO", directory=tmp_path, console=False)
    log = get_logger("t")
    log.debug("invisible")
    log.info("visible")

    events = [record["event"] for record in _records(tmp_path / OPERATIONAL_LOG)]
    assert events == ["visible"]


def test_trace_is_a_real_level_below_debug(tmp_path: Path):
    configure_logging("TRACE", directory=tmp_path, console=False)
    get_logger("t").log(TRACE, "very.detailed")

    records = _records(tmp_path / OPERATIONAL_LOG)
    assert TRACE < logging.DEBUG
    assert records[0]["level"] == "TRACE"


def test_the_console_can_be_quieter_than_the_file(tmp_path: Path, capsys):
    """An interactive command prints its answer; the file still records everything.

    Quietening the terminal must not throw away the log — that is the opposite of
    what a persistent log is for, and it is the easy mistake to make when one level
    controls both destinations.
    """
    configure_logging("DEBUG", directory=tmp_path, console=True, console_level="WARNING")
    log = get_logger("t")
    log.debug("only.on.disk")
    log.warning("both.places")

    # `_records` flushes the background writer; the console handler runs on that
    # same thread, so capsys must be read *after* the flush or it sees nothing.
    events = [record["event"] for record in _records(tmp_path / OPERATIONAL_LOG)]
    captured = capsys.readouterr().out

    assert events == ["only.on.disk", "both.places"]
    assert "only.on.disk" not in captured
    assert "both.places" in captured


# --------------------------------------------------------- tracing integration


def test_every_record_inside_a_trace_carries_its_trace_id(tmp_path: Path):
    """The seam between the two observability systems.

    Without this field, logs and traces are two piles of facts about the same
    request with nothing joining them.
    """
    configure_observability(enabled=True, log_traces=False, persist=False)
    configure_logging("INFO", directory=tmp_path, console=False)

    with trace("operation") as current:
        get_logger("t").info("inside")
        expected = current.trace_id
    get_logger("t").info("outside")

    records = {record["event"]: record for record in _records(tmp_path / OPERATIONAL_LOG)}

    assert records["inside"]["trace_id"] == expected
    assert "trace_id" not in records["outside"]


def test_an_explicit_trace_id_on_the_call_site_is_not_overwritten(tmp_path: Path):
    configure_observability(enabled=True, log_traces=False, persist=False)
    configure_logging("INFO", directory=tmp_path, console=False)

    with trace("operation"):
        get_logger("t").info("correlated", extra={"trace_id": "supplied-by-caller"})

    assert _records(tmp_path / OPERATIONAL_LOG)[0]["trace_id"] == "supplied-by-caller"


def test_each_pipeline_stage_logs_once_at_trace_level(tmp_path: Path):
    """The span bridge: pipeline coverage with no call site in any pipeline."""
    configure_observability(enabled=True, log_traces=False, persist=False, log_spans=True)
    configure_logging("TRACE", directory=tmp_path, console=False)

    with trace("answer"), span("retrieve", strategy="hybrid"), span("embed_query"):
        pass

    spans = [r for r in _records(tmp_path / OPERATIONAL_LOG) if r["event"] == "span.complete"]

    # `trace()` opens a root span of its own, so the operation itself is logged
    # alongside its stages — which is what makes the log readable top-down.
    assert {record["span"] for record in spans} == {"answer", "retrieve", "embed_query"}
    retrieve = next(record for record in spans if record["span"] == "retrieve")
    # Span attributes are flattened onto the record, so the log carries the same
    # facts the trace does rather than a name and a duration.
    assert retrieve["strategy"] == "hybrid"
    assert retrieve["duration_ms"] >= 0
    assert retrieve["trace_id"]


def test_span_logging_costs_nothing_when_the_level_excludes_it(tmp_path: Path):
    configure_observability(enabled=True, log_traces=False, persist=False, log_spans=True)
    configure_logging("INFO", directory=tmp_path, console=False)

    with trace("answer"), span("retrieve"):
        pass

    events = [record["event"] for record in _records(tmp_path / OPERATIONAL_LOG)]
    assert "span.complete" not in events


def test_span_logging_can_be_disabled_outright(tmp_path: Path):
    configure_observability(enabled=True, log_traces=False, persist=False, log_spans=False)
    configure_logging("TRACE", directory=tmp_path, console=False)

    with trace("answer"), span("retrieve"):
        pass

    events = [record["event"] for record in _records(tmp_path / OPERATIONAL_LOG)]
    assert "span.complete" not in events


def test_a_failing_stage_still_logs_its_span_with_the_error(tmp_path: Path):
    configure_observability(enabled=True, log_traces=False, persist=False, log_spans=True)
    configure_logging("TRACE", directory=tmp_path, console=False)

    with pytest.raises(RuntimeError), trace("answer"), span("retrieve"):
        raise RuntimeError("store unreachable")

    spans = [r for r in _records(tmp_path / OPERATIONAL_LOG) if r["event"] == "span.complete"]
    assert spans[0]["error"] == "RuntimeError: store unreachable"


# ----------------------------------------------------------------- invocation


def test_the_command_that_ran_is_named_in_the_log(tmp_path: Path, monkeypatch):
    """Every command initialises identically; without this they are indistinguishable."""
    monkeypatch.setattr("sys.argv", ["osc", "ask", "how much annual leave?", "--explain"])
    configure_logging("INFO", directory=tmp_path, console=False)
    log_command(capture_payloads=False)

    record = _records(tmp_path / OPERATIONAL_LOG)[0]
    assert record["command"] == "ask"
    assert record["flags"] == ["--explain"]


def test_positional_arguments_are_payload_and_stay_out_by_default(tmp_path: Path, monkeypatch):
    """`osc ask "<a real question>"` puts user text on the command line."""
    monkeypatch.setattr("sys.argv", ["osc", "ask", "how much annual leave?"])
    configure_logging("INFO", directory=tmp_path, console=False)
    log_command(capture_payloads=False)

    record = _records(tmp_path / OPERATIONAL_LOG)[0]
    assert "argv" not in record
    assert "annual leave" not in json.dumps(record)


def test_payload_capture_records_the_whole_invocation(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["osc", "ask", "how much annual leave?"])
    configure_logging("INFO", directory=tmp_path, console=False, capture_payloads=True)
    log_command(capture_payloads=True)

    assert _records(tmp_path / OPERATIONAL_LOG)[0]["argv"] == ["ask", "how much annual leave?"]


# ------------------------------------------------------------------ redaction


@pytest.mark.parametrize(
    "field",
    ["api_key", "API_KEY", "auth_token", "password", "dsn", "client_secret", "authorization"],
)
def test_credential_fields_are_redacted(tmp_path: Path, field: str):
    configure_logging("INFO", directory=tmp_path, console=False)
    get_logger("t").info("connect", extra={field: "super-secret-value"})

    record = _records(tmp_path / OPERATIONAL_LOG)[0]
    assert record[field] == REDACTED
    assert "super-secret-value" not in json.dumps(record)


def test_credentials_are_redacted_even_with_payload_capture_on(tmp_path: Path):
    """`capture_payloads` opens up corpus text. It must not open up secrets."""
    configure_logging("INFO", directory=tmp_path, console=False, capture_payloads=True)
    get_logger("t").info("connect", extra={"api_key": "sk-live-123", "question": "what?"})

    record = _records(tmp_path / OPERATIONAL_LOG)[0]
    assert record["api_key"] == REDACTED
    assert record["question"] == "what?"


def test_corpus_text_is_reduced_to_a_length_by_default(tmp_path: Path):
    configure_logging("INFO", directory=tmp_path, console=False)
    get_logger("t").info(
        "generation.complete", extra={"question": "how many leave days?", "citations": 2}
    )

    record = _records(tmp_path / OPERATIONAL_LOG)[0]
    assert record["question"] == "<20 chars>"
    # Everything that is not text survives: a redacted log must still be useful.
    assert record["citations"] == 2


def test_payload_capture_restores_the_text(tmp_path: Path):
    configure_logging("INFO", directory=tmp_path, console=False, capture_payloads=True)
    get_logger("t").info("generation.complete", extra={"question": "how many leave days?"})

    assert _records(tmp_path / OPERATIONAL_LOG)[0]["question"] == "how many leave days?"


def test_redaction_applies_to_the_console_as_well_as_the_file(tmp_path: Path, capsys):
    """A secret suppressed on disk and printed to stdout is a secret that leaked."""
    configure_logging("INFO", directory=tmp_path, console=True)
    get_logger("t").info("connect", extra={"api_key": "sk-live-123"})
    shutdown_logging()

    assert "sk-live-123" not in capsys.readouterr().out


# ---------------------------------------------------------------- audit stream


def test_audit_records_go_to_their_own_file(tmp_path: Path):
    configure_logging("INFO", directory=tmp_path, console=False)
    audit("answer", model="qwen3:8b", citations=2)
    get_logger("t").info("operational.event")
    shutdown_logging()

    audit_events = [r["event"] for r in _records(tmp_path / AUDIT_LOG)]
    operational = [r["event"] for r in _records(tmp_path / OPERATIONAL_LOG)]

    assert audit_events == ["answer"]
    # Not duplicated into the operational stream: two copies under two retention
    # policies is the exact confusion two streams exist to avoid.
    assert "answer" not in operational
    assert operational == ["operational.event"]


def test_audit_survives_a_coarser_operational_level(tmp_path: Path):
    """Quietening a noisy deployment must not stop recording what was answered."""
    configure_logging("ERROR", directory=tmp_path, console=False)
    audit("answer", model="qwen3:8b")

    assert [r["event"] for r in _records(tmp_path / AUDIT_LOG)] == ["answer"]


def test_audit_can_be_disabled(tmp_path: Path):
    configure_logging("INFO", directory=tmp_path, console=False, audit=False)
    audit("answer", model="qwen3:8b")
    shutdown_logging()

    assert not (tmp_path / AUDIT_LOG).exists()


def test_the_audit_stream_has_its_own_retention(tmp_path: Path):
    configure_logging(
        "INFO",
        directory=tmp_path,
        console=False,
        max_bytes=1024,
        backup_count=1,
        audit_max_bytes=1024,
        audit_backup_count=3,
    )
    for index in range(400):
        audit("answer", index=index, padding="x" * 200)
        get_logger("t").info("filler", index=index) if False else None
    shutdown_logging()

    assert len(sorted(tmp_path.glob(f"{AUDIT_LOG}.*"))) == 3


# ------------------------------------------------------------- failure cases


def test_an_unwritable_log_directory_does_not_stop_the_process(tmp_path: Path, capsys):
    """An operational problem, not a reason to refuse to start.

    Console logging still works and the failure is reported through it.
    """
    blocker = tmp_path / "logs"
    blocker.write_text("I am a file, not a directory", encoding="utf-8")

    configure_logging("INFO", directory=blocker, console=True)
    get_logger("t").info("still.running")
    shutdown_logging()

    assert log_directory() is None
    assert "still.running" in capsys.readouterr().out


def test_an_unserialisable_value_does_not_lose_the_record(tmp_path: Path):
    """`default=str` on the encoder: a weird value degrades, it does not drop."""

    class Opaque:
        def __repr__(self) -> str:
            return "<opaque>"

    configure_logging("INFO", directory=tmp_path, console=False)
    get_logger("t").info("odd", extra={"value": Opaque()})

    assert _records(tmp_path / OPERATIONAL_LOG)[0]["value"] == "<opaque>"


def test_an_exception_is_recorded_with_its_traceback(tmp_path: Path):
    configure_logging("INFO", directory=tmp_path, console=False)
    try:
        raise ValueError("boom")
    except ValueError:
        get_logger("t").exception("operation.failed")

    record = _records(tmp_path / OPERATIONAL_LOG)[0]
    assert record["level"] == "ERROR"
    assert "ValueError: boom" in record["exception"]


def test_shutdown_is_idempotent_and_leaks_no_listener(tmp_path: Path):
    configure_logging("INFO", directory=tmp_path, console=False)
    get_logger("t").info("one")
    shutdown_logging()
    shutdown_logging()  # must not raise

    assert [r["event"] for r in _records(tmp_path / OPERATIONAL_LOG)] == ["one"]


def test_reconfiguring_does_not_duplicate_records(tmp_path: Path):
    """Each `configure_logging` replaces the stack rather than adding to it."""
    configure_logging("INFO", directory=tmp_path, console=False)
    configure_logging("INFO", directory=tmp_path, console=False)
    get_logger("t").info("once")

    assert len(_records(tmp_path / OPERATIONAL_LOG)) == 1


def test_records_are_appended_across_reconfiguration(tmp_path: Path):
    """Persistence: a restarted process adds to the log rather than truncating it."""
    configure_logging("INFO", directory=tmp_path, console=False)
    get_logger("t").info("first.run")
    shutdown_logging()

    configure_logging("INFO", directory=tmp_path, console=False)
    get_logger("t").info("second.run")

    events = [r["event"] for r in _records(tmp_path / OPERATIONAL_LOG)]
    assert events == ["first.run", "second.run"]


@pytest.mark.parametrize("field", ["input_tokens", "output_tokens", "max_tokens", "token_count"])
def test_token_counts_are_not_mistaken_for_credentials(tmp_path: Path, field: str):
    """Regression: `input_tokens` contains "token" and is a cost measurement.

    The substring heuristic is deliberately broad, so it produces false positives on
    exactly the fields most worth keeping. Redacting these silently destroyed every
    token and spend analysis in the log — found by reading a real audit record, not
    by a test, which is why there is now a test.
    """
    configure_logging("INFO", directory=tmp_path, console=False)
    get_logger("t").info("generation.complete", extra={field: 1234})

    assert _records(tmp_path / OPERATIONAL_LOG)[0][field] == 1234


def test_third_party_debug_output_is_pinned_out_of_our_stream(tmp_path: Path):
    """Raising our level to TRACE must not turn on every vendor SDK's firehose.

    Those emit unstructured prose into a JSONL file and can carry request bodies.
    A live TRACE run caught the openai client doing exactly that.
    """
    configure_logging("TRACE", directory=tmp_path, console=False)
    logging.getLogger("openai").debug("Request options: {...}")
    logging.getLogger("httpx").debug("Sending HTTP Request: POST /embeddings")
    get_logger("osc_assistant.retrieval").log(TRACE, "ours.survives")

    events = [record["event"] for record in _records(tmp_path / OPERATIONAL_LOG)]
    assert events == ["ours.survives"]
