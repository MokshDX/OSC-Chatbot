"""Google Gemini embedding provider."""

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

DEFAULT_MODEL = "gemini-embedding-001"
_KNOWN_DIMENSIONS: dict[str, int] = {
    "gemini-embedding-001": 3072,
    "text-embedding-004": 768,
}


class GeminiEmbeddingOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key: str | None = None
    dimensions: int | None = Field(
        default=None,
        description=(
            "Requests a truncated vector. Gemini embeddings support Matryoshka "
            "truncation, so a smaller width trades a little accuracy for storage."
        ),
    )
    batch_size: int = Field(default=32, ge=1)


class GeminiEmbeddingModel:
    """Adapter over `google-genai`'s embedding interface."""

    def __init__(self, model: str, options: GeminiEmbeddingOptions) -> None:
        try:
            from google import genai
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise MissingDependencyError("gemini", "google-genai", "gemini") from exc

        api_key = (
            options.api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        )
        if not api_key:
            raise ConfigurationError(
                "The 'gemini' embedding provider needs an API key. Set GEMINI_API_KEY "
                "or embeddings.options.api_key."
            )

        self._model = model or DEFAULT_MODEL
        dimensions = options.dimensions or _KNOWN_DIMENSIONS.get(self._model)
        if dimensions is None:
            raise ConfigurationError(
                f"Vector width for Gemini model {self._model!r} is unknown. Set "
                f"embeddings.options.dimensions."
            )

        self._options = options
        self._dimensions = dimensions
        self._client = genai.Client(api_key=api_key)

    @property
    def model_id(self) -> str:
        return self._model

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed_documents(self, texts: Sequence[str]) -> list[Vector]:
        vectors: list[Vector] = []
        for start in range(0, len(texts), self._options.batch_size):
            batch = list(texts[start : start + self._options.batch_size])
            vectors.extend(await self._embed(batch, "RETRIEVAL_DOCUMENT"))
        return vectors

    async def embed_query(self, text: str) -> Vector:
        return (await self._embed([text], "RETRIEVAL_QUERY"))[0]

    async def _embed(self, texts: list[str], task_type: str) -> list[Vector]:
        config: dict[str, Any] = {"task_type": task_type}
        if self._options.dimensions:
            config["output_dimensionality"] = self._options.dimensions
        try:
            response = await self._client.aio.models.embed_content(
                model=self._model, contents=texts, config=config
            )
        # Broad by intent: Gemini SDK errors are translated into this
        # package's error hierarchy so callers never import a vendor exception.
        except Exception as exc:
            raise ProviderError(f"Gemini embedding request failed: {exc}") from exc
        return [list(embedding.values) for embedding in response.embeddings]


@embedding_registry.register("gemini")
def _build(config: ComponentConfig) -> EmbeddingModel:
    return GeminiEmbeddingModel(
        config.model, GeminiEmbeddingOptions.model_validate(config.options)
    )
