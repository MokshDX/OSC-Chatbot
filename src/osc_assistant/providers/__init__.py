"""Provider implementations.

Importing this package registers every built-in provider. Provider modules are
imported for their registration side effect only — nothing else imports them, and
no business logic knows they exist.

To add a provider: create a module that registers a factory, then add it to the
matching sub-package `__init__`. Nothing else changes.
"""

from __future__ import annotations

from . import embeddings, llm, reranking, vectorstores

__all__ = ["embeddings", "llm", "reranking", "vectorstores"]
