"""Corpus ingestion: connectors and the chunk/embed/store pipeline."""

from __future__ import annotations

from .loaders import (
    DEFAULT_EXTENSIONS,
    FilesystemLoader,
    InMemoryLoader,
    stable_document_id,
)
from .pipeline import IngestionPipeline, IngestionReport

__all__ = [
    "DEFAULT_EXTENSIONS",
    "FilesystemLoader",
    "InMemoryLoader",
    "IngestionPipeline",
    "IngestionReport",
    "stable_document_id",
]
