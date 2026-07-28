"""Embedding providers. Imported for registration side effects."""

from __future__ import annotations

from . import gemini, local, openai_compatible, voyage

__all__ = ["gemini", "local", "openai_compatible", "voyage"]
