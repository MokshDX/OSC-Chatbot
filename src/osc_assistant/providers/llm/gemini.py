"""Google Gemini chat provider (native SDK).

Gemini also exposes an OpenAI-compatible endpoint, reachable through the
`gemini_openai` provider name. This native adapter exists because the first-party
API exposes usage accounting and generation controls that the compatibility shim
flattens away; prefer it unless you specifically want the compatibility path.

Like every non-Anthropic adapter, grounding falls back to rendered sources and
`[n]` marker parsing.
"""

from __future__ import annotations

import inspect
import os
from collections.abc import AsyncIterator
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ...errors import ConfigurationError, MissingDependencyError, ProviderError
from ...grounding import compose_grounded_system, parse_marker_citations
from ...protocols import ChatModel
from ...registries import llm_registry
from ...registry import ComponentConfig
from ...types import (
    ChatRequest,
    ChatResponse,
    CitationDelta,
    Role,
    StreamEnd,
    StreamEvent,
    TextDelta,
    Usage,
)

DEFAULT_MODEL = "gemini-2.5-flash"


class GeminiOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key: str | None = Field(
        default=None, description="Falls back to GEMINI_API_KEY or GOOGLE_API_KEY."
    )
    generation_config: dict[str, Any] = Field(
        default_factory=dict,
        description="Merged into GenerateContentConfig for model-specific settings.",
    )


class GeminiChatModel:
    """Adapter over `google-genai`'s async models interface."""

    def __init__(self, model: str, options: GeminiOptions) -> None:
        try:
            from google import genai
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise MissingDependencyError("gemini", "google-genai", "gemini") from exc

        api_key = (
            options.api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        )
        if not api_key:
            raise ConfigurationError(
                "The 'gemini' provider needs an API key. Set GEMINI_API_KEY or "
                "llm.options.api_key."
            )

        self._model = model or DEFAULT_MODEL
        self._options = options
        self._client = genai.Client(api_key=api_key)

    @property
    def model_id(self) -> str:
        return self._model

    @property
    def supports_citations(self) -> bool:
        return False

    async def complete(self, request: ChatRequest) -> ChatResponse:
        try:
            response = await self._client.aio.models.generate_content(
                model=self._model,
                contents=_build_contents(request),
                config=self._build_config(request),
            )
        # Broad by intent: Gemini SDK errors are translated into this
        # package's error hierarchy so callers never import a vendor exception.
        except Exception as exc:
            raise ProviderError(f"Gemini request failed: {exc}") from exc

        text = response.text or ""
        return ChatResponse(
            text=text,
            citations=parse_marker_citations(text, request.sources),
            usage=_parse_usage(getattr(response, "usage_metadata", None)),
            model=self._model,
            stop_reason=_finish_reason(response),
        )

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        buffer: list[str] = []
        usage = Usage()
        try:
            stream = self._client.aio.models.generate_content_stream(
                model=self._model,
                contents=_build_contents(request),
                config=self._build_config(request),
            )
            # The async streaming call returns a coroutine yielding the iterator on
            # some SDK versions and the iterator directly on others. Normalising here
            # keeps the adapter working across both without pinning a patch release.
            if inspect.isawaitable(stream):
                stream = await stream

            async for chunk in stream:
                if getattr(chunk, "usage_metadata", None):
                    usage = _parse_usage(chunk.usage_metadata)
                text = getattr(chunk, "text", None)
                if text:
                    buffer.append(text)
                    yield TextDelta(text=text)
        except Exception as exc:
            raise ProviderError(f"Gemini stream failed: {exc}") from exc

        for citation in parse_marker_citations("".join(buffer), request.sources):
            yield CitationDelta(citation=citation)
        yield StreamEnd(usage=usage)

    def _build_config(self, request: ChatRequest) -> dict[str, Any]:
        """Build the generation config as a plain mapping.

        `google-genai` accepts a dict here and converts it internally, which avoids
        importing its typed config classes and keeps this adapter tolerant of
        additions to that type.
        """
        config: dict[str, Any] = {"max_output_tokens": request.max_tokens}
        system = compose_grounded_system(request)
        if system:
            config["system_instruction"] = system
        if request.temperature is not None:
            config["temperature"] = request.temperature
        config.update(self._options.generation_config)
        return config


def _build_contents(request: ChatRequest) -> list[dict[str, Any]]:
    """Map the neutral message list onto Gemini's `contents` shape.

    Gemini names the assistant role "model"; that rename is the adapter's job.
    """
    return [
        {
            "role": "model" if message.role is Role.ASSISTANT else "user",
            "parts": [{"text": message.content}],
        }
        for message in request.messages
    ]


def _parse_usage(metadata: Any) -> Usage:
    if metadata is None:
        return Usage()
    return Usage(
        input_tokens=getattr(metadata, "prompt_token_count", 0) or 0,
        output_tokens=getattr(metadata, "candidates_token_count", 0) or 0,
        cached_input_tokens=getattr(metadata, "cached_content_token_count", 0) or 0,
    )


def _finish_reason(response: Any) -> str | None:
    candidates = getattr(response, "candidates", None) or []
    if not candidates:
        return None
    reason = getattr(candidates[0], "finish_reason", None)
    return str(reason) if reason is not None else None


@llm_registry.register("gemini")
def _build(config: ComponentConfig) -> ChatModel:
    return GeminiChatModel(config.model, GeminiOptions.model_validate(config.options))
