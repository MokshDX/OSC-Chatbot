"""Exception hierarchy for the assistant.

A single root (`AssistantError`) lets the API layer translate any internal failure
into a structured response without catching bare `Exception`, while callers that
care about a specific failure mode can still catch a narrow subclass.
"""

from __future__ import annotations


class AssistantError(Exception):
    """Base class for every error raised by this package."""


class ConfigurationError(AssistantError):
    """The system is misconfigured and cannot start or serve a request.

    Raised for problems an operator must fix: an unknown provider name, a missing
    credential, or an embedding model whose dimensions disagree with the store.
    """


class UnknownComponentError(ConfigurationError):
    """A component was requested by a name that is not registered."""

    def __init__(self, kind: str, name: str, available: list[str]) -> None:
        self.kind = kind
        self.name = name
        self.available = available
        super().__init__(
            f"Unknown {kind} provider {name!r}. "
            f"Registered providers: {', '.join(sorted(available)) or '(none)'}. "
            f"If this is a new provider, ensure its module is imported so it can "
            f"register itself."
        )


class MissingDependencyError(ConfigurationError):
    """A provider was selected but its optional dependency is not installed."""

    def __init__(self, provider: str, package: str, extra: str) -> None:
        super().__init__(
            f"The {provider!r} provider requires the {package!r} package. "
            f"Install it with: pip install 'osc-assistant[{extra}]'"
        )


class ParseError(AssistantError):
    """A source file could not be turned into text.

    Raised per file and caught by the ingestion pipeline, which records it and
    continues: one unreadable document must never abort a corpus-wide sync.
    """


class EvaluationError(AssistantError):
    """An evaluation could not be run as specified.

    Raised for a malformed golden set, a missing baseline, or a run whose result
    cannot be trusted — all of which an operator fixes in a file rather than in the
    code, so they are reported as messages and not as tracebacks.
    """


class ProviderError(AssistantError):
    """An upstream provider (LLM, embeddings, reranker) failed."""


class VectorStoreError(AssistantError):
    """The vector store could not complete an operation."""


class DimensionMismatchError(ConfigurationError):
    """The configured embedding model does not match the store's vector width.

    Changing embedding models requires a full re-index; failing loudly at startup
    is preferable to silently returning nonsense similarity scores.
    """

    def __init__(self, expected: int, actual: int, model_id: str) -> None:
        super().__init__(
            f"Vector store expects {expected}-dimensional vectors but embedding model "
            f"{model_id!r} produces {actual}. Re-run migrations with the new dimension "
            f"and re-index the corpus."
        )
