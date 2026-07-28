"""Voyage AI embedding provider.

Voyage is Anthropic's recommended embedding partner and consistently strong on
retrieval benchmarks, so it is worth having as a first-class option alongside a
Claude answer model. Implemented directly against the REST endpoint with `httpx`
rather than pulling in another SDK for a single POST.

Voyage embeddings are asymmetric: queries and documents must be tagged with
different `input_type` values or recall degrades measurably.
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, Field

from ...errors import ConfigurationError, ProviderError
from ...protocols import EmbeddingModel
from ...registries import embedding_registry
from ...registry import ComponentConfig
from ...types import Vector

_KNOWN_DIMENSIONS: dict[str, int] = {
    "voyage-3-large": 1024,
    "voyage-3": 1024,
    "voyage-3-lite": 512,
    "voyage-code-3": 1024,
    "voyage-finance-2": 1024,
    "voyage-law-2": 1024,
}

DEFAULT_MODEL = "voyage-3-large"
_ENDPOINT = "https://api.voyageai.com/v1/embeddings"


class VoyageOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key: str | None = None
    base_url: str = _ENDPOINT
    timeout: float = 60.0
    dimensions: int | None = None
    batch_size: int = Field(default=64, ge=1)


class VoyageEmbeddingModel:
    """Adapter over the Voyage AI embeddings endpoint."""

    def __init__(self, model: str, options: VoyageOptions) -> None:
        api_key = options.api_key or os.environ.get("VOYAGE_API_KEY")
        if not api_key:
            raise ConfigurationError(
                "The 'voyage' embedding provider needs an API key. Set VOYAGE_API_KEY "
                "or embeddings.options.api_key."
            )

        self._model = model or DEFAULT_MODEL
        dimensions = options.dimensions or _KNOWN_DIMENSIONS.get(self._model)
        if dimensions is None:
            raise ConfigurationError(
                f"Vector width for Voyage model {self._model!r} is unknown. Set "
                f"embeddings.options.dimensions."
            )

        self._options = options
        self._dimensions = dimensions
        self._client = httpx.AsyncClient(
            timeout=options.timeout,
            headers={"Authorization": f"Bearer {api_key}"},
        )

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
            vectors.extend(await self._embed(batch, "document"))
        return vectors

    async def embed_query(self, text: str) -> Vector:
        return (await self._embed([text], "query"))[0]

    async def _embed(self, texts: list[str], input_type: str) -> list[Vector]:
        payload: dict[str, Any] = {
            "model": self._model,
            "input": texts,
            "input_type": input_type,
        }
        if self._options.dimensions:
            payload["output_dimension"] = self._options.dimensions
        try:
            response = await self._client.post(self._options.base_url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ProviderError(f"Voyage embedding request failed: {exc}") from exc

        data = response.json().get("data", [])
        ordered = sorted(data, key=lambda item: item.get("index", 0))
        return [list(item["embedding"]) for item in ordered]

    async def aclose(self) -> None:
        await self._client.aclose()


@embedding_registry.register("voyage")
def _build(config: ComponentConfig) -> EmbeddingModel:
    return VoyageEmbeddingModel(config.model, VoyageOptions.model_validate(config.options))
