"""The registries for every swappable component.

Kept in one small module so that a provider implementation imports only this, and
the composition root imports only the packages whose modules do the registering.
Neither depends on the other, so adding a provider is a new file plus one import
line in its package `__init__`.
"""

from __future__ import annotations

from .protocols import ChatModel, Chunker, EmbeddingModel, Reranker, VectorStore
from .registry import Registry

llm_registry: Registry[ChatModel] = Registry("llm")
embedding_registry: Registry[EmbeddingModel] = Registry("embedding")
reranker_registry: Registry[Reranker] = Registry("reranker")
vector_store_registry: Registry[VectorStore] = Registry("vector store")
chunker_registry: Registry[Chunker] = Registry("chunker")

__all__ = [
    "chunker_registry",
    "embedding_registry",
    "llm_registry",
    "reranker_registry",
    "vector_store_registry",
]
