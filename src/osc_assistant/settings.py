"""Configuration.

Layered, highest precedence first: process environment, then `.env`, then a YAML
profile file. The YAML layer is what makes experimentation cheap — a chunking or
model sweep is a directory of small profiles run against the same binary, with no
code change and no environment juggling:

    OSC_PROFILE=config/experiments/gemini-bge.yaml osc-assistant eval

Every swappable component is a `ComponentConfig`, so changing provider is a
two-line edit and never a code change.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from .registry import ComponentConfig

DEFAULT_PROFILE = Path("config/default.yaml")
PROFILE_ENV_VAR = "OSC_PROFILE"


class RetrievalSettings(BaseModel):
    """Tuning for the retrieval stage. Every value here is an experiment knob."""

    model_config = ConfigDict(extra="forbid")

    strategy: str = Field(default="hybrid", pattern="^(vector|keyword|hybrid)$")
    candidates: int = Field(default=40, ge=1, description="Fetched before reranking.")
    top_k: int = Field(default=8, ge=1, description="Passed to the model as sources.")
    rrf_k: int = Field(default=60, ge=1, description="Reciprocal Rank Fusion constant.")
    min_score: float = Field(
        default=0.0,
        description=(
            "Discards first-stage hits scoring below this, before reranking. The "
            "scale follows `strategy`: cosine similarity in [-1, 1] for `vector`, "
            "an RRF score around 0.016 for `hybrid`. Deliberately not applied to "
            "reranker output, whose scale is provider-defined and often negative."
        ),
    )
    rewrite_queries: bool = Field(
        default=True,
        description="Resolve conversational references into a standalone query first.",
    )


class GenerationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_tokens: int = Field(default=4096, ge=256)
    temperature: float | None = Field(
        default=None,
        description="Advisory. Several current models reject sampling parameters.",
    )
    require_citations: bool = Field(
        default=True,
        description="Abstain when the model answers without citing any source.",
    )
    abstention_message: str = (
        "I could not find anything in the indexed OSC documents that answers this. "
        "Try rephrasing, or check whether the relevant source has been indexed."
    )


class ChunkingSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    strategy: str = "recursive"
    chunk_size: int = Field(default=1200, ge=100, description="Target size in characters.")
    chunk_overlap: int = Field(default=150, ge=0)


class CorpusSettings(BaseModel):
    """Which directory is the answer corpus.

    This is configuration rather than a constant because the root was previously
    written out in three places that had to agree — the `Makefile`, the `doctor`
    command's default and the empty-index startup note — and "they must agree" is a
    rule that survives only as long as everyone remembers it. Ingesting the wrong
    root is the one corpus mistake nothing downstream catches: an answer sourced
    from the wrong universe retrieves cleanly, grounds correctly and cites
    accurately. See docs/engineering/architecture/knowledge-corpus.md.
    """

    model_config = ConfigDict(extra="forbid")

    root: Path = Field(
        default=Path("docs/company/schema"),
        description=(
            "The directory `ingest` indexes and `doctor` checks. Everything outside "
            "it is invisible to the assistant, which is what makes the corpus "
            "boundary fail safe rather than fail open."
        ),
    )


class SessionSettings(BaseModel):
    """Bounds on ephemeral conversational memory.

    Every value here is a ceiling, not a target. Conversation state is held in the
    answering process and is deliberately not durable (ADR 0010), so each bound
    exists to stop one unbounded thing: total memory, per-conversation prompt
    growth, and the lifetime of an abandoned session nobody closed.
    """

    model_config = ConfigDict(extra="forbid")

    max_messages: int = Field(
        default=20,
        ge=2,
        description=(
            "Messages retained per session, oldest evicted first. Bounds the prompt "
            "rather than the storage: history is replayed into every turn, so an "
            "unbounded session would grow the context window until generation "
            "truncated. 20 is ten exchanges."
        ),
    )
    max_sessions: int = Field(
        default=1000,
        ge=1,
        description=(
            "Concurrent sessions held in memory. The least recently used is evicted "
            "when the limit is reached, so a client that never closes a session "
            "degrades that session rather than the process."
        ),
    )
    idle_ttl_seconds: float = Field(
        default=3600.0,
        gt=0,
        description=(
            "How long a session survives without a turn. Reclaims the sessions of "
            "clients that closed a browser tab instead of calling DELETE, which is "
            "most of them."
        ),
    )


class DatabaseSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dsn: str = "postgresql://postgres:postgres@localhost:5432/osc_assistant"
    min_pool_size: int = Field(default=1, ge=1)
    max_pool_size: int = Field(default=10, ge=1)


class ServerSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host: str = "127.0.0.1"
    port: int = 8000
    cors_origins: list[str] = Field(default_factory=list)


class LoggingSettings(BaseModel):
    """Where logs are written, how long they are kept, and what may appear in them.

    Verbosity and console format stay on `Settings` as `log_level` / `log_format`
    because they predate this block and are addressed by name in profiles, the CLI
    and the tests. This model owns only what persistence added, so there is exactly
    one place to look for each setting rather than two that can disagree.
    """

    model_config = ConfigDict(extra="forbid")

    directory: Path | None = Field(
        default=Path(".osc/logs"),
        description=(
            "Where log files are written. Set to null — or an empty/`null`/`none` "
            "environment value — to disable file logging entirely. That is the right "
            "setting for a container that ships stdout to a collector, and what the "
            "test suite uses."
        ),
    )

    @field_validator("directory", mode="before")
    @classmethod
    def _disable_on_empty(cls, value: Any) -> Any:
        """Let the environment express "no directory", which it otherwise cannot.

        An environment variable is always a string, so `Path | None` reads
        `OSC_LOGGING__DIRECTORY=null` as a *relative directory named `null`* and an
        empty value as the working directory — both of which silently create log
        files rather than disabling them. Both were observed: a `null/` directory
        and a stray `osc.log`, in a repository checkout.

        This matters more here than for other optional paths because disabling file
        logging is the documented setting for a containerised deployment, and a
        container configures through the environment. A setting that is reachable
        only from YAML is not reachable where it is needed.
        """
        if isinstance(value, str) and value.strip().lower() in ("", "null", "none"):
            return None
        return value

    max_bytes: int = Field(
        default=10_000_000,
        ge=1024,
        description=(
            "Rotate the operational log at this size. Disk is bounded by "
            "max_bytes * (backup_count + 1) — a ceiling by construction, which a "
            "time-based policy would not give."
        ),
    )
    backup_count: int = Field(
        default=5,
        ge=0,
        description="Rotated operational files kept. The oldest is deleted, not archived.",
    )

    audit: bool = Field(
        default=True,
        description=(
            "Write one record per answered question to audit.log. Separate from the "
            "operational stream because 'which passages did we show this user' has to "
            "outlive a debug firehose that rotates in hours."
        ),
    )
    audit_max_bytes: int = Field(default=10_000_000, ge=1024)
    audit_backup_count: int = Field(
        default=20,
        ge=0,
        description="Higher than backup_count: audit history is the one worth keeping.",
    )

    capture_payloads: bool = Field(
        default=False,
        description=(
            "Include question, answer and chunk text in logs. Off by default: those "
            "fields are reduced to a character count, which keeps every timing and "
            "count a latency investigation needs while keeping corpus content out of "
            "a file that gets shipped elsewhere. Credentials are redacted regardless "
            "and this flag cannot re-enable them."
        ),
    )
    log_spans: bool = Field(
        default=True,
        description=(
            "Emit one TRACE record as each pipeline stage completes. Costs nothing at "
            "the default INFO level; set log_level to TRACE to watch a request move "
            "through the pipeline under `tail -f`."
        ),
    )


class ObservabilitySettings(BaseModel):
    """How much the system records about its own execution.

    Defaults are chosen for a development machine: everything on, because the cost
    is a few hundred microseconds per request and the benefit is being able to
    answer "why did it do that?" without reproducing the request.
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = Field(
        default=True, description="Collect execution traces. Off makes every span a no-op."
    )
    trace_buffer_size: int = Field(
        default=50,
        ge=1,
        description=(
            "Recent traces kept in memory for `osc-assistant trace` and /api/traces. "
            "In-process and lost on restart; durable traces belong in a collector."
        ),
    )
    max_spans_per_trace: int = Field(
        default=500,
        ge=1,
        description=(
            "Upper bound on one trace, so a corpus-wide ingestion cannot grow "
            "without limit. Totals stay accurate past the cap; only detail is lost."
        ),
    )
    log_traces: bool = Field(
        default=True,
        description="Emit each completed trace as one structured log record.",
    )
    persist_traces: bool = Field(
        default=True,
        description=(
            "Append completed traces to a bounded JSONL file, so they outlive the "
            "process. Without this a one-shot CLI command's trace is gone the "
            "moment it exits, and re-running to recreate it does not reproduce a "
            "non-deterministic generation."
        ),
    )
    trace_dir: Path = Field(
        default=Path(".osc"),
        description="Directory holding the persisted trace log. Add it to .gitignore.",
    )
    max_trace_file_bytes: int = Field(
        default=5_000_000,
        ge=1024,
        description=(
            "Rotation threshold. Two files are kept — the one being written and the "
            "one before it — so the ceiling is roughly twice this."
        ),
    )
    capture_text: bool = Field(
        default=True,
        description=(
            "Record questions, rewritten queries and answers in traces. Set false "
            "for corpora where a trace must not contain content — the shape and "
            "timings of every trace are retained, only the text becomes a length."
        ),
    )
    expose_traces: bool = Field(
        default=True,
        description=(
            "Serve /api/traces. These contain question text and retrieved chunk "
            "ids, and the API has no authentication yet, so this is refused "
            "outright when environment is not 'development'."
        ),
    )


class Settings(BaseSettings):
    """Root configuration object.

    Nested values are addressable from the environment with a double underscore,
    e.g. `OSC_LLM__PROVIDER=openai_compatible`.
    """

    model_config = SettingsConfigDict(
        env_prefix="OSC_",
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )

    workspace_id: str = Field(
        default="default",
        description=(
            "Partition key for all indexed content. Single-workspace today; carried "
            "through the schema from the start because adding a partition key to a "
            "populated corpus is a data migration."
        ),
    )
    environment: str = "development"
    log_level: str = Field(
        default="INFO",
        pattern="^(?i:TRACE|DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="TRACE adds one record per pipeline stage; see LoggingSettings.log_spans.",
    )
    log_format: str = Field(default="json", pattern="^(json|text)$")

    llm: ComponentConfig = ComponentConfig(provider="anthropic", model="claude-opus-5")
    fast_llm: ComponentConfig = ComponentConfig(
        provider="anthropic", model="claude-haiku-4-5"
    )
    embeddings: ComponentConfig = ComponentConfig(
        provider="openai_compatible", model="text-embedding-3-large"
    )
    reranker: ComponentConfig = ComponentConfig(provider="noop")
    vector_store: ComponentConfig = ComponentConfig(provider="pgvector")

    corpus: CorpusSettings = CorpusSettings()
    chunking: ChunkingSettings = ChunkingSettings()
    retrieval: RetrievalSettings = RetrievalSettings()
    generation: GenerationSettings = GenerationSettings()
    session: SessionSettings = SessionSettings()
    database: DatabaseSettings = DatabaseSettings()
    server: ServerSettings = ServerSettings()
    logging: LoggingSettings = LoggingSettings()
    observability: ObservabilitySettings = ObservabilitySettings()

    @property
    def traces_are_exposed(self) -> bool:
        """Whether the HTTP trace endpoints should be registered.

        Two conditions, not one. Traces carry question text and retrieved chunk
        ids, and no endpoint on this service is authenticated yet, so exposing them
        outside development would publish corpus content to anyone who can reach
        the port. The environment check is deliberately not overridable by the
        setting: a profile copied from a developer's machine into production must
        not be able to turn this on by accident.
        """
        return self.observability.expose_traces and self.environment == "development"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, env_settings, dotenv_settings, _YamlProfileSource(settings_cls))


class _YamlProfileSource(PydanticBaseSettingsSource):
    """Lowest-precedence source reading a YAML profile.

    The profile path comes from `OSC_PROFILE`, falling back to `config/default.yaml`.
    A missing file is not an error: the built-in defaults are a working configuration.
    """

    def get_field_value(self, field: Any, field_name: str) -> tuple[Any, str, bool]:
        raise NotImplementedError  # pragma: no cover - required by the ABC, unused

    def __call__(self) -> dict[str, Any]:
        path = Path(os.environ.get(PROFILE_ENV_VAR, DEFAULT_PROFILE))
        if not path.is_file():
            return {}
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        if loaded is None:
            return {}
        if not isinstance(loaded, dict):
            raise TypeError(f"Profile {path} must contain a YAML mapping at the top level.")
        return loaded


def load_settings(**overrides: Any) -> Settings:
    """Build settings, applying `overrides` at the highest precedence."""
    return Settings(**overrides)


def log_resolved_settings(settings: Settings) -> None:
    """Record what the configuration layers actually resolved to.

    Called from the composition roots *after* logging is configured rather than
    from `load_settings`, because settings are loaded first — anything logged
    during loading would go to an unconfigured root logger and be lost, which is
    the one time you most want the record.

    Only the values that change behaviour are emitted, for the same reason the
    evaluation harness snapshots the same subset: a record that included the whole
    configuration would differ between two machines over the log level and give a
    reader no way to tell an irrelevant difference from a relevant one. The DSN is
    redacted by the logging filter on the way out — its key contains `dsn`.
    """
    from .logging import get_logger

    get_logger(__name__).info(
        "settings.resolved",
        extra={
            "profile": os.environ.get(PROFILE_ENV_VAR, str(DEFAULT_PROFILE)),
            "environment": settings.environment,
            "workspace_id": settings.workspace_id,
            "log_level": settings.log_level,
            "llm": f"{settings.llm.provider}/{settings.llm.model}",
            "embeddings": f"{settings.embeddings.provider}/{settings.embeddings.model}",
            "reranker": settings.reranker.provider,
            "vector_store": settings.vector_store.provider,
            "chunking": settings.chunking.strategy,
            "chunk_size": settings.chunking.chunk_size,
            "retrieval_strategy": settings.retrieval.strategy,
            "top_k": settings.retrieval.top_k,
            "tracing": settings.observability.enabled,
            "log_dir": str(settings.logging.directory) if settings.logging.directory else None,
            "capture_payloads": settings.logging.capture_payloads,
        },
    )
