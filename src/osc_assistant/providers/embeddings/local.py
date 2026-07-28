"""Local embedding provider backed by `sentence-transformers`.

Present for two reasons that matter to this project: it removes the third-party
embedding vendor entirely for deployments that cannot send corpus text off-site,
and it makes offline experimentation free — sweeping five embedding models over a
golden set costs nothing but CPU time.

Encoding is CPU-bound and the library is synchronous, so calls are dispatched to a
worker thread to keep the event loop responsive.
"""

from __future__ import annotations

import asyncio
from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ...errors import MissingDependencyError, ProviderError
from ...protocols import EmbeddingModel
from ...registries import embedding_registry
from ...registry import ComponentConfig
from ...types import Vector

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"


class LocalEmbeddingOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    device: str | None = Field(default=None, description="e.g. 'cpu', 'cuda', 'mps'.")
    normalize: bool = Field(
        default=True,
        description="Unit-normalise vectors so cosine and dot product agree.",
    )
    batch_size: int = Field(default=32, ge=1)
    query_prefix: str = Field(
        default="",
        description=(
            "Prepended to queries only. Several retrieval models (bge, e5) are "
            "asymmetric and expect an instruction prefix such as "
            "'Represent this sentence for searching relevant passages: '."
        ),
    )
    document_prefix: str = ""


class LocalEmbeddingModel:
    """Adapter over a `sentence-transformers` model loaded in-process."""

    def __init__(self, model: str, options: LocalEmbeddingOptions) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise MissingDependencyError("local", "sentence-transformers", "local") from exc

        self._model_id = model or DEFAULT_MODEL
        self._options = options
        self._encoder = SentenceTransformer(self._model_id, device=options.device)
        dimensions = self._encoder.get_sentence_embedding_dimension()
        if dimensions is None:  # pragma: no cover - defensive; models expose this
            raise ProviderError(
                f"Could not determine the vector width of {self._model_id!r}."
            )
        self._dimensions = int(dimensions)

    @property
    def model_id(self) -> str:
        return self._model_id

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed_documents(self, texts: Sequence[str]) -> list[Vector]:
        prefixed = [self._options.document_prefix + text for text in texts]
        return await asyncio.to_thread(self._encode, prefixed)

    async def embed_query(self, text: str) -> Vector:
        vectors = await asyncio.to_thread(self._encode, [self._options.query_prefix + text])
        return vectors[0]

    def _encode(self, texts: list[str]) -> list[Vector]:
        result: Any = self._encoder.encode(
            texts,
            batch_size=self._options.batch_size,
            normalize_embeddings=self._options.normalize,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return [[float(value) for value in row] for row in result]


@embedding_registry.register("local")
@embedding_registry.register("sentence_transformers")
def _build(config: ComponentConfig) -> EmbeddingModel:
    return LocalEmbeddingModel(config.model, LocalEmbeddingOptions.model_validate(config.options))
