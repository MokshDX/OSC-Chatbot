"""Embedding provider for any OpenAI-compatible `/v1/embeddings` endpoint.

Covers OpenAI, Ollama, LM Studio, vLLM, Together and Hugging Face TGI. Chosen
independently of the chat model — running Claude for generation and a local
embedding model for retrieval is a supported and common configuration.
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ...errors import ConfigurationError, MissingDependencyError, ProviderError
from ...protocols import EmbeddingModel
from ...registries import embedding_registry
from ...registry import ComponentConfig
from ...types import Vector

# Vector width has to be known before the first call, because the store's column
# is created with a fixed dimension. Models outside this table must declare
# `options.dimensions` explicitly rather than be guessed at.
_KNOWN_DIMENSIONS: dict[str, int] = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536,
    "nomic-embed-text": 768,
    "mxbai-embed-large": 1024,
    "bge-m3": 1024,
    "all-minilm": 384,
}

_BASE_URLS: dict[str, str | None] = {
    "openai": None,
    "openai_compatible": None,
    "ollama": "http://localhost:11434/v1",
    "lmstudio": "http://localhost:1234/v1",
    "vllm": "http://localhost:8000/v1",
    "together": "https://api.together.xyz/v1",
    "huggingface": "https://router.huggingface.co/v1",
}

_API_KEY_ENVS: dict[str, str] = {
    "openai": "OPENAI_API_KEY",
    "openai_compatible": "OPENAI_API_KEY",
    "together": "TOGETHER_API_KEY",
    "huggingface": "HF_TOKEN",
}


class OpenAIEmbeddingOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key: str | None = None
    base_url: str | None = None
    timeout: float = 60.0
    max_retries: int = 2
    dimensions: int | None = Field(
        default=None,
        description=(
            "Required for models not in the built-in table. On OpenAI's v3 models "
            "this also requests a truncated vector."
        ),
    )
    batch_size: int = Field(
        default=64, ge=1, description="Texts per request during corpus ingestion."
    )
    send_dimensions: bool = Field(
        default=False,
        description=(
            "Forward `dimensions` to the API. Only OpenAI v3 models accept it; "
            "most compatible servers reject the field."
        ),
    )


class OpenAICompatibleEmbeddingModel:
    """Adapter over the `/v1/embeddings` interface."""

    def __init__(self, provider: str, model: str, options: OpenAIEmbeddingOptions) -> None:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise MissingDependencyError(provider, "openai", "openai") from exc

        if not model:
            raise ConfigurationError(f"Provider {provider!r} requires an explicit model name.")

        dimensions = options.dimensions or _KNOWN_DIMENSIONS.get(model)
        if dimensions is None:
            raise ConfigurationError(
                f"Vector width for embedding model {model!r} is unknown. Set "
                f"embeddings.options.dimensions so the vector store can be sized correctly."
            )

        env_var = _API_KEY_ENVS.get(provider)
        self._provider = provider
        self._model = model
        self._options = options
        self._dimensions = dimensions
        self._client = AsyncOpenAI(
            api_key=options.api_key or (os.environ.get(env_var) if env_var else None) or "local",
            base_url=options.base_url or _BASE_URLS.get(provider),
            timeout=options.timeout,
            max_retries=options.max_retries,
        )

    async def aclose(self) -> None:
        """Release the underlying HTTP client.

        `Container.shutdown()` probes every component it built for this method. An
        adapter that owns a client and does not offer one is silently exempt from
        that mechanism — which is how the default local stack leaked a connection
        pool per container until it was caught by the event loop closing underneath
        an unclosed client during the end-to-end suite.
        """
        await self._client.close()

    @property
    def model_id(self) -> str:
        return self._model

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed_documents(self, texts: Sequence[str]) -> list[Vector]:
        vectors: list[Vector] = []
        for start in range(0, len(texts), self._options.batch_size):
            batch = texts[start : start + self._options.batch_size]
            vectors.extend(await self._embed(list(batch)))
        return vectors

    async def embed_query(self, text: str) -> Vector:
        return (await self._embed([text]))[0]

    async def _embed(self, texts: list[str]) -> list[Vector]:
        payload: dict[str, Any] = {"model": self._model, "input": texts}
        if self._options.send_dimensions and self._options.dimensions:
            payload["dimensions"] = self._options.dimensions
        try:
            response = await self._client.embeddings.create(**payload)
        # Broad by intent: the OpenAI-compatible SDK errors are translated into this
        # package's error hierarchy so callers never import a vendor exception.
        except Exception as exc:
            raise ProviderError(f"{self._provider} embedding request failed: {exc}") from exc

        # The API is documented to preserve input order, but sorting by index makes
        # that independent of any given compatible server honouring it.
        ordered = sorted(response.data, key=lambda item: item.index)
        return [list(item.embedding) for item in ordered]


def _make_factory(provider: str) -> Any:
    def factory(config: ComponentConfig) -> EmbeddingModel:
        return OpenAICompatibleEmbeddingModel(
            provider, config.model, OpenAIEmbeddingOptions.model_validate(config.options)
        )

    return factory


for _name in _BASE_URLS:
    embedding_registry.register(_name)(_make_factory(_name))
