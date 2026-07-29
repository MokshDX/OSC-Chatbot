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
from pydantic import BaseModel, ConfigDict, Field
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
    log_level: str = "INFO"
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

    chunking: ChunkingSettings = ChunkingSettings()
    retrieval: RetrievalSettings = RetrievalSettings()
    generation: GenerationSettings = GenerationSettings()
    database: DatabaseSettings = DatabaseSettings()
    server: ServerSettings = ServerSettings()

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
