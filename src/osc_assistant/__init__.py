"""OSC internal knowledge assistant.

A provider-agnostic retrieval-augmented question answering service. The chat model,
embedding model, reranker, vector store and chunking strategy are all selected by
configuration; business logic depends only on the protocols in `protocols`.
"""

from __future__ import annotations

from .container import Container
from .settings import Settings, load_settings

__version__ = "0.1.0"

__all__ = ["Container", "Settings", "__version__", "load_settings"]
