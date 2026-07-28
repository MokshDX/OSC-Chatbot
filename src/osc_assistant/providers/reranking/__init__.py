"""Reranker providers. Imported for registration side effects."""

from __future__ import annotations

from . import cross_encoder, noop

__all__ = ["cross_encoder", "noop"]
