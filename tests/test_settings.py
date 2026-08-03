"""Configuration precedence tests.

`settings.py` carries the only hand-written logic an operator routinely touches: a
custom YAML source and a four-layer precedence order. A regression here is
invisible — nothing crashes — and surfaces later as "production is running the
wrong model", which is why it is worth pinning explicitly.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from osc_assistant.settings import PROFILE_ENV_VAR, Settings, load_settings


@pytest.fixture(autouse=True)
def _isolate_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Strip inherited OSC_ variables and point at an empty profile.

    Without this the developer's own `.env` and shell decide the result, and the
    test passes or fails depending on whose machine it runs on.
    """
    for name in list(__import__("os").environ):
        if name.startswith("OSC_"):
            monkeypatch.delenv(name, raising=False)
    empty = tmp_path / "empty.yaml"
    empty.write_text("{}\n", encoding="utf-8")
    monkeypatch.setenv(PROFILE_ENV_VAR, str(empty))


def _profile(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "profile.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def test_a_yaml_profile_supplies_values(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv(
        PROFILE_ENV_VAR,
        str(_profile(tmp_path, "llm:\n  provider: ollama\n  model: qwen3:8b\n")),
    )

    settings = load_settings()

    assert settings.llm.provider == "ollama"
    assert settings.llm.model == "qwen3:8b"


def test_the_environment_beats_the_profile(tmp_path: Path, monkeypatch) -> None:
    """The layer order exists so a deployment can override a checked-in file."""
    monkeypatch.setenv(
        PROFILE_ENV_VAR,
        str(_profile(tmp_path, "llm:\n  provider: ollama\n  model: qwen3:8b\n")),
    )
    monkeypatch.setenv("OSC_LLM__PROVIDER", "groq")

    settings = load_settings()

    assert settings.llm.provider == "groq"


def test_a_nested_override_replaces_only_the_named_field(
    tmp_path: Path, monkeypatch
) -> None:
    """The behaviour operators actually rely on, and the easiest to break.

    Overriding `OSC_LLM__PROVIDER` must not discard the model set in the profile.
    """
    monkeypatch.setenv(
        PROFILE_ENV_VAR,
        str(
            _profile(
                tmp_path,
                "llm:\n  provider: ollama\n  model: qwen3:8b\n"
                "  options:\n    timeout: 30\n",
            )
        ),
    )
    monkeypatch.setenv("OSC_LLM__PROVIDER", "groq")

    settings = load_settings()

    assert settings.llm.provider == "groq"
    assert settings.llm.model == "qwen3:8b"
    assert settings.llm.options == {"timeout": 30}


def test_init_arguments_beat_the_environment(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("OSC_ENVIRONMENT", "staging")

    assert load_settings(environment="test").environment == "test"


def test_a_missing_profile_is_tolerated(monkeypatch) -> None:
    """The built-in defaults are a working configuration; absence is not an error."""
    monkeypatch.setenv(PROFILE_ENV_VAR, "config/does-not-exist.yaml")

    assert load_settings().llm.provider


def test_an_empty_profile_is_tolerated(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv(PROFILE_ENV_VAR, str(_profile(tmp_path, "\n")))

    assert load_settings().llm.provider


def test_a_profile_that_is_not_a_mapping_is_rejected(tmp_path: Path, monkeypatch) -> None:
    """Failing loudly beats silently ignoring the file an operator just edited."""
    monkeypatch.setenv(PROFILE_ENV_VAR, str(_profile(tmp_path, "- one\n- two\n")))

    with pytest.raises(TypeError, match="YAML mapping"):
        load_settings()


def test_an_unknown_key_in_a_typed_block_is_rejected(tmp_path: Path, monkeypatch) -> None:
    """A typo in a tuning knob must not be silently discarded."""
    monkeypatch.setenv(PROFILE_ENV_VAR, str(_profile(tmp_path, "retrieval:\n  top_kk: 5\n")))

    with pytest.raises(Exception, match="top_kk"):
        load_settings()


def test_observability_defaults_are_on(tmp_path: Path) -> None:
    settings = Settings()

    assert settings.observability.enabled
    assert settings.observability.capture_text
    assert settings.observability.trace_buffer_size > 0


def test_traces_are_exposed_only_in_development() -> None:
    """The environment check is not overridable by the setting, on purpose.

    A profile copied from a developer's machine into production must not be able to
    publish question text and chunk ids on an unauthenticated endpoint.
    """
    assert Settings(environment="development").traces_are_exposed

    assert not Settings(environment="production").traces_are_exposed
    assert not Settings(
        environment="development", observability={"expose_traces": False}
    ).traces_are_exposed
