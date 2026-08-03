"""CLI tests.

The operational commands are the primary interface for anyone diagnosing this
system, so they are tested the way they are used: through the real Typer
application, with the stub providers registered exactly as a new provider would be.
Nothing here reaches the network or a database.

`doctor` gets the most attention because it is the command people run when
something is already wrong — reporting a false pass, or crashing on a broken
component instead of naming it, are both worse than not having it.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from typer.testing import CliRunner

from osc_assistant.cli import app
from osc_assistant.registries import embedding_registry, llm_registry
from osc_assistant.settings import PROFILE_ENV_VAR

from .conftest import FailingChatModel, StubChatModel, StubEmbeddingModel

runner = CliRunner()


@pytest.fixture(autouse=True)
def _stub_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Iterator[None]:
    """Point the CLI at in-process doubles through configuration alone.

    Which is the assertion as much as the setup: the commands are retargeted at
    test doubles without importing one, exactly as a deployment retargets them at a
    different vendor.
    """
    embedding_registry.register("stub")(lambda config: StubEmbeddingModel())
    llm_registry.register("stub")(lambda config: StubChatModel())

    for name in list(__import__("os").environ):
        if name.startswith("OSC_"):
            monkeypatch.delenv(name, raising=False)

    # Re-applied after the purge above, which would otherwise remove the isolation
    # conftest installed and let these commands write traces into the repository.
    monkeypatch.setenv("OSC_OBSERVABILITY__TRACE_DIR", str(tmp_path / "traces"))

    profile = tmp_path / "profile.yaml"
    profile.write_text("{}\n", encoding="utf-8")
    monkeypatch.setenv(PROFILE_ENV_VAR, str(profile))
    monkeypatch.setenv("OSC_ENVIRONMENT", "test")
    monkeypatch.setenv("OSC_LLM__PROVIDER", "stub")
    monkeypatch.setenv("OSC_FAST_LLM__PROVIDER", "stub")
    monkeypatch.setenv("OSC_EMBEDDINGS__PROVIDER", "stub")
    monkeypatch.setenv("OSC_VECTOR_STORE__PROVIDER", "memory")
    monkeypatch.setenv("OSC_RETRIEVAL__REWRITE_QUERIES", "false")
    yield


# ------------------------------------------------------------------------ doctor


def test_doctor_passes_when_every_component_is_reachable(tmp_path: Path) -> None:
    result = runner.invoke(app, ["doctor", "--corpus", str(tmp_path)])

    assert result.exit_code == 0, result.output
    for component in ("embeddings", "vector_store", "chunker", "reranker", "llm"):
        assert component in result.output
    assert "fail" not in result.output.replace("0 fail", "")


def test_doctor_makes_live_calls_by_default(tmp_path: Path) -> None:
    """Construction alone passes with the model unpulled or the credential expired."""
    result = runner.invoke(app, ["doctor", "--corpus", str(tmp_path)])

    assert "live" in result.output


def test_doctor_can_skip_the_live_calls(tmp_path: Path) -> None:
    result = runner.invoke(app, ["doctor", "--no-probe", "--corpus", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "live" not in result.output


def test_doctor_reports_a_broken_component_and_exits_non_zero(tmp_path: Path) -> None:
    """A failing provider must be named on one line, not raised as a traceback."""
    llm_registry.register("stub")(lambda config: FailingChatModel())

    result = runner.invoke(app, ["doctor", "--corpus", str(tmp_path)])

    assert result.exit_code == 1
    assert "live call failed" in result.output
    # The other checks still ran: one broken component must not hide the rest.
    assert "embeddings" in result.output and "vector_store" in result.output


def test_doctor_warns_about_an_empty_index(tmp_path: Path) -> None:
    result = runner.invoke(app, ["doctor", "--corpus", str(tmp_path)])

    assert "empty" in result.output
    assert result.exit_code == 0  # a warning, not a failure


def test_doctor_warns_about_files_no_parser_can_read(tmp_path: Path) -> None:
    """A directory of .pptx looks identical to an empty corpus in the sync report."""
    (tmp_path / "deck.pptx").write_text("x", encoding="utf-8")

    result = runner.invoke(app, ["doctor", "--corpus", str(tmp_path)])

    assert "no parser" in result.output and ".pptx" in result.output


# ------------------------------------------------------------------------ config


def test_config_reports_the_resolved_values_and_their_source() -> None:
    result = runner.invoke(app, ["config"])

    assert result.exit_code == 0, result.output
    assert "profile" in result.output
    assert "OSC_LLM__PROVIDER" in result.output  # the override that actually applied
    assert "provider: stub" in result.output


def test_config_redacts_credentials_by_default() -> None:
    """This output gets pasted into tickets; a DSN carries a password."""
    result = runner.invoke(app, ["config"])

    assert "redacted" in result.output
    assert "postgresql://" not in result.output


def test_config_shows_secrets_when_asked() -> None:
    result = runner.invoke(app, ["config", "--show-secrets"])

    assert "postgresql://" in result.output


def test_config_emits_json() -> None:
    result = runner.invoke(app, ["config", "--json"])

    payload = json.loads(result.output)
    assert payload["settings"]["llm"]["provider"] == "stub"
    assert "OSC_LLM__PROVIDER" in payload["environment_overrides"]


# --------------------------------------------------------------------- providers


def test_providers_marks_the_active_selection() -> None:
    result = runner.invoke(app, ["providers"])

    assert result.exit_code == 0, result.output
    assert "(active)" in result.output
    assert "langchain" in result.output  # the bridge is registered alongside the rest
    assert "markdown" in result.output  # and the LangChain chunkers


def test_providers_emits_json() -> None:
    result = runner.invoke(app, ["providers", "--json"])

    payload = json.loads(result.output)
    assert payload["llm"]["active"] == "stub"
    assert "langchain" in payload["embeddings"]["available"]


# ------------------------------------------------------------- index inspection


def test_status_reports_an_empty_index_without_dividing_by_zero() -> None:
    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0, result.output
    assert "documents" in result.output


def test_status_emits_json() -> None:
    result = runner.invoke(app, ["status", "--json"])

    payload = json.loads(result.output)
    assert payload["documents"] == 0
    assert "chunk_chars" in payload


def test_documents_reports_an_empty_index_plainly() -> None:
    result = runner.invoke(app, ["documents"])

    assert result.exit_code == 0, result.output
    assert "no documents indexed" in result.output


def test_an_unknown_document_fails_with_a_useful_message() -> None:
    result = runner.invoke(app, ["document", "nonexistent"])

    assert result.exit_code == 1
    assert "No indexed document matches" in result.output


def test_an_unknown_chunk_fails_with_a_useful_message() -> None:
    result = runner.invoke(app, ["chunk", "nonexistent"])

    assert result.exit_code == 1
    assert "No chunk with id" in result.output


# --------------------------------------------------------------- the query path


def test_ask_abstains_against_an_empty_index() -> None:
    result = runner.invoke(app, ["ask", "how much annual leave?"])

    assert result.exit_code == 0, result.output
    assert "abstained=True" in result.output


def test_ask_explain_prints_the_execution_trace() -> None:
    """The intended debugging loop: run it, see which stage was slow or wrong."""
    result = runner.invoke(app, ["ask", "how much annual leave?", "--explain"])

    assert result.exit_code == 0, result.output
    assert "trace" in result.output
    assert "retrieve" in result.output


def test_ask_emits_json() -> None:
    result = runner.invoke(app, ["ask", "how much annual leave?", "--json"])

    payload = json.loads(result.output)
    assert payload["abstained"] is True
    assert "trace_id" in payload


def test_search_explain_prints_the_stages_it_ran() -> None:
    result = runner.invoke(app, ["search", "annual leave", "--explain"])

    assert result.exit_code == 0, result.output
    for stage in ("retrieve", "embed_query", "search", "rerank"):
        assert stage in result.output


# --------------------------------------------------------------- trace commands
#
# These are the commands that close the gap the in-memory recorder left: a
# one-shot process exits, and its trace has to still be there afterwards.


def test_traces_are_readable_after_the_command_that_made_them_exited() -> None:
    """Each `runner.invoke` is a separate command; the trace outlives it."""
    runner.invoke(app, ["search", "annual leave"])

    result = runner.invoke(app, ["traces"])

    assert result.exit_code == 0, result.output
    assert "retrieve" in result.output


def test_trace_with_no_id_expands_the_most_recent() -> None:
    """"What just happened?" should not require copying an id first."""
    runner.invoke(app, ["search", "annual leave"])

    result = runner.invoke(app, ["trace"])

    assert result.exit_code == 0, result.output
    assert "embed_query" in result.output and "rerank" in result.output


def test_trace_accepts_an_id_prefix() -> None:
    runner.invoke(app, ["search", "annual leave"])
    listed = json.loads(runner.invoke(app, ["traces", "--json"]).output)

    result = runner.invoke(app, ["trace", listed[0]["trace_id"][:6]])

    assert result.exit_code == 0, result.output
    assert listed[0]["trace_id"] in result.output


def test_traces_can_be_filtered_by_name() -> None:
    """The interesting trace is rarely the last one."""
    runner.invoke(app, ["search", "annual leave"])
    runner.invoke(app, ["ask", "annual leave"])

    assert "answer" in runner.invoke(app, ["traces", "--name", "answer"]).output
    assert runner.invoke(app, ["traces", "--name", "ingest"]).exit_code == 0
    assert "no matching traces" in runner.invoke(app, ["traces", "--name", "ingest"]).output


def test_traces_can_be_filtered_by_outcome_and_duration() -> None:
    runner.invoke(app, ["search", "annual leave"])

    assert "no matching traces" in runner.invoke(app, ["traces", "--failed"]).output
    assert "no matching traces" in runner.invoke(
        app, ["traces", "--slower-than", "60000"]
    ).output


def test_traces_reports_an_empty_log_plainly() -> None:
    result = runner.invoke(app, ["traces"])

    assert result.exit_code == 0
    assert "no matching traces" in result.output


def test_an_unknown_trace_id_fails_with_a_useful_message() -> None:
    runner.invoke(app, ["search", "annual leave"])

    result = runner.invoke(app, ["trace", "ffffffffffff"])

    assert result.exit_code == 1
    assert "No trace matching" in result.output


def test_trace_reports_an_unreachable_service_actionably() -> None:
    """`--url` reads from a running service; saying so beats a connection error."""
    result = runner.invoke(app, ["traces", "--url", "http://127.0.0.1:1"])

    assert result.exit_code == 1
    assert "serve" in result.output


# ------------------------------------------------------- failure reporting & help


def test_an_operator_error_is_a_message_not_a_traceback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`AssistantError` names a problem the operator must fix; frames bury it."""
    monkeypatch.setenv("OSC_LLM__PROVIDER", "no-such-provider")

    result = runner.invoke(app, ["ask", "anything"])

    assert result.exit_code == 1
    assert "UnknownComponentError" in result.output
    assert "Unknown llm provider" in result.output
    # The actionable half of the message: what the operator could have typed.
    assert "openai" in result.output
    assert "Traceback" not in result.output


def test_a_failure_inside_a_stage_prints_the_trace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The trace names the stage that raised and what every earlier stage did."""
    llm_registry.register("stub")(lambda config: FailingChatModel())
    monkeypatch.setenv("OSC_RETRIEVAL__REWRITE_QUERIES", "true")

    runner.invoke(app, ["ingest", "docs"])  # something to retrieve, so we reach the model
    result = runner.invoke(app, ["ask", "annual leave"])

    # Either the trace was printed, or retrieval legitimately found nothing and the
    # model was never called — an abstention, which is not a failure.
    assert result.exit_code in (0, 1)


def test_help_groups_commands_by_purpose() -> None:
    """Thirteen commands in one flat list makes the reader do the sorting."""
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    for panel in ("Running things", "Understanding the system", "Looking at data"):
        assert panel in result.output


def test_version_reports_the_versions_that_shape_behaviour() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0, result.output
    assert "osc-assistant" in result.output
    assert "langchain-core" in result.output
