"""Embedding providers. Imported for registration side effects."""

from __future__ import annotations

from . import gemini, langchain_bridge, local, openai_compatible, voyage

__all__ = ["gemini", "langchain_bridge", "local", "openai_compatible", "voyage"]
