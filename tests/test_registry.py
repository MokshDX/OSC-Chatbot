"""The registry is the mechanism that makes providers pluggable, so it is tested
directly: a broken registry means silent misconfiguration everywhere else."""

from __future__ import annotations

import pytest

from osc_assistant.errors import UnknownComponentError
from osc_assistant.registries import (
    chunker_registry,
    embedding_registry,
    llm_registry,
    reranker_registry,
    vector_store_registry,
)
from osc_assistant.registry import ComponentConfig, Registry


def test_registered_factory_is_used() -> None:
    registry: Registry[str] = Registry("thing")

    @registry.register("example")
    def _build(config: ComponentConfig) -> str:
        return f"built:{config.model}"

    assert registry.create(ComponentConfig(provider="example", model="v1")) == "built:v1"


def test_unknown_provider_lists_the_alternatives() -> None:
    registry: Registry[str] = Registry("thing")
    registry.register("alpha")(lambda config: "a")
    registry.register("beta")(lambda config: "b")

    with pytest.raises(UnknownComponentError) as excinfo:
        registry.create(ComponentConfig(provider="gamma"))

    message = str(excinfo.value)
    assert "gamma" in message
    assert "alpha" in message and "beta" in message


def test_re_registration_overrides() -> None:
    """Overriding a built-in must be possible without editing it."""
    registry: Registry[str] = Registry("thing")
    registry.register("x")(lambda config: "first")
    registry.register("x")(lambda config: "second")

    assert registry.create(ComponentConfig(provider="x")) == "second"


def test_options_are_passed_through_untouched() -> None:
    registry: Registry[dict[str, object]] = Registry("thing")
    registry.register("x")(lambda config: config.options)

    options = {"api_key": "secret", "nested": {"a": 1}}
    assert registry.create(ComponentConfig(provider="x", options=options)) == options


def test_unknown_config_key_is_rejected() -> None:
    """A typo in a profile must fail loudly rather than be silently ignored."""
    with pytest.raises(ValueError, match="extra"):
        ComponentConfig(provider="x", modle="typo")  # type: ignore[call-arg]


@pytest.mark.parametrize(
    ("registry", "expected"),
    [
        (llm_registry, {"anthropic", "openai", "gemini", "groq", "ollama", "huggingface"}),
        (embedding_registry, {"openai", "voyage", "gemini", "local", "ollama"}),
        (reranker_registry, {"noop", "cross_encoder"}),
        (vector_store_registry, {"pgvector", "memory"}),
        (chunker_registry, {"recursive", "fixed"}),
    ],
)
def test_built_in_providers_are_registered(registry: Registry[object], expected: set[str]) -> None:
    """Importing the package must make every built-in provider selectable."""
    import osc_assistant.container  # noqa: F401 - triggers provider registration

    assert expected <= set(registry.names())
