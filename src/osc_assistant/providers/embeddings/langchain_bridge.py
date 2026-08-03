"""Embedding provider backed by any LangChain `Embeddings` implementation.

The counterpart to the chat bridge, for the same reason and with the same
boundaries: OSC's own adapters cover the providers it uses, and this covers
everything else — Bedrock, Vertex, Azure, Cohere, Jina, Fireworks — without an
adapter per vendor.

    embeddings:
      provider: langchain
      model: embed-english-v3.0
      options:
        class_path: langchain_cohere.CohereEmbeddings
        dimensions: 1024

`dimensions` is configuration rather than something to probe, because the vector
store needs it before the first embedding call: it is substituted into the DDL at
migration time. The bridge verifies it against the first batch it embeds and
refuses to continue on a mismatch — silently storing vectors of the wrong width
into a column that happens to accept them is the failure mode that produces
plausible nonsense rather than an error.
"""

from __future__ import annotations

import importlib
from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ...errors import (
    ConfigurationError,
    DimensionMismatchError,
    MissingDependencyError,
    ProviderError,
)
from ...protocols import EmbeddingModel
from ...registries import embedding_registry
from ...registry import ComponentConfig
from ...types import Vector


class LangChainEmbeddingOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    class_path: str = Field(
        description=(
            "Dotted path to a LangChain Embeddings subclass, e.g. "
            "'langchain_cohere.CohereEmbeddings'."
        )
    )
    dimensions: int = Field(
        gt=0,
        description=(
            "Vector width the model produces. Required: the store fixes its column "
            "width at migration time, before any embedding call has been made."
        ),
    )
    init: dict[str, Any] = Field(
        default_factory=dict, description="Keyword arguments for the class constructor."
    )


class LangChainEmbeddingModel:
    """Adapter presenting a LangChain embeddings object as an OSC `EmbeddingModel`."""

    def __init__(self, model: str, options: LangChainEmbeddingOptions) -> None:
        self._model_name = model
        self._options = options
        self._client = _instantiate(options.class_path, model, options.init)

    @property
    def model_id(self) -> str:
        return self._model_name or self._options.class_path

    @property
    def dimensions(self) -> int:
        return self._options.dimensions

    async def embed_documents(self, texts: Sequence[str]) -> list[Vector]:
        if not texts:
            return []
        try:
            vectors = await self._client.aembed_documents(list(texts))
        except Exception as exc:
            raise ProviderError(
                f"langchain ({self._options.class_path}) embedding failed: {exc}"
            ) from exc
        self._assert_width(vectors[0])
        return [list(vector) for vector in vectors]

    async def embed_query(self, text: str) -> Vector:
        try:
            vector = await self._client.aembed_query(text)
        except Exception as exc:
            raise ProviderError(
                f"langchain ({self._options.class_path}) embedding failed: {exc}"
            ) from exc
        self._assert_width(vector)
        return list(vector)

    def _assert_width(self, vector: Sequence[float]) -> None:
        """Catch a misconfigured `dimensions` at the first call rather than at query time.

        A too-narrow declaration is rejected by the store's own guard; a too-wide one
        would not be, and would produce a corpus embedded at one width and queried at
        another with no error anywhere.
        """
        if len(vector) != self._options.dimensions:
            raise DimensionMismatchError(self._options.dimensions, len(vector), self.model_id)


def _instantiate(class_path: str, model: str, init: dict[str, Any]) -> Any:
    module_name, _, class_name = class_path.rpartition(".")
    if not module_name:
        raise ConfigurationError(
            f"embeddings.options.class_path must be a dotted path such as "
            f"'langchain_cohere.CohereEmbeddings', got {class_path!r}."
        )

    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise MissingDependencyError("langchain", module_name, "langchain") from exc

    try:
        factory = getattr(module, class_name)
    except AttributeError as exc:
        raise ConfigurationError(f"{module_name} has no attribute {class_name!r}.") from exc

    kwargs = dict(init)
    if model:
        kwargs.setdefault("model", model)
    try:
        return factory(**kwargs)
    except Exception as exc:
        raise ConfigurationError(
            f"Could not construct {class_path} with {sorted(kwargs)}: {exc}"
        ) from exc


@embedding_registry.register("langchain")
def _build(config: ComponentConfig) -> EmbeddingModel:
    return LangChainEmbeddingModel(
        config.model, LangChainEmbeddingOptions.model_validate(config.options)
    )
