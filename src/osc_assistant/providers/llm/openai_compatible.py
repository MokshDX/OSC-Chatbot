"""Chat provider for any OpenAI-compatible endpoint.

One adapter covers OpenAI, Groq, Ollama, vLLM, LM Studio, Hugging Face TGI,
OpenRouter, Together and Gemini's compatibility endpoint, because all of them
speak `/v1/chat/completions`. Writing eight near-identical adapters would have
been eight places to fix the same bug.

Each is registered under its own provider name with the correct base URL and
credential environment variable pre-filled, so configuration stays declarative:

    llm:
      provider: groq
      model: llama-3.3-70b-versatile

None of these endpoints resolve citations, so grounding falls back to rendering
sources into the prompt and parsing `[n]` markers out of the answer.
"""

from __future__ import annotations

import os
import re
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any, Literal

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
    StreamEnd,
    StreamEvent,
    TextDelta,
    Usage,
)


@dataclass(frozen=True, slots=True)
class _Preset:
    """Defaults for one OpenAI-compatible service."""

    base_url: str | None
    api_key_env: str | None
    requires_key: bool = True


# Adding a service is a single entry here; nothing else in the codebase changes.
_PRESETS: dict[str, _Preset] = {
    "openai": _Preset(base_url=None, api_key_env="OPENAI_API_KEY"),
    "openai_compatible": _Preset(base_url=None, api_key_env="OPENAI_API_KEY"),
    "groq": _Preset(
        base_url="https://api.groq.com/openai/v1", api_key_env="GROQ_API_KEY"
    ),
    "openrouter": _Preset(
        base_url="https://openrouter.ai/api/v1", api_key_env="OPENROUTER_API_KEY"
    ),
    "together": _Preset(
        base_url="https://api.together.xyz/v1", api_key_env="TOGETHER_API_KEY"
    ),
    "huggingface": _Preset(
        base_url="https://router.huggingface.co/v1", api_key_env="HF_TOKEN"
    ),
    "gemini_openai": _Preset(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key_env="GEMINI_API_KEY",
    ),
    "ollama": _Preset(
        base_url="http://localhost:11434/v1", api_key_env=None, requires_key=False
    ),
    "vllm": _Preset(base_url="http://localhost:8000/v1", api_key_env=None, requires_key=False),
    "lmstudio": _Preset(
        base_url="http://localhost:1234/v1", api_key_env=None, requires_key=False
    ),
    "local": _Preset(base_url="http://localhost:8000/v1", api_key_env=None, requires_key=False),
}


class OpenAICompatibleOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key: str | None = None
    base_url: str | None = Field(
        default=None, description="Overrides the preset base URL for this provider name."
    )
    timeout: float = 120.0
    max_retries: int = 2
    max_tokens_param: Literal["max_tokens", "max_completion_tokens"] = Field(
        default="max_tokens",
        description=(
            "Newer OpenAI reasoning models require max_completion_tokens; most "
            "compatible servers only accept max_tokens."
        ),
    )
    include_usage_in_stream: bool = Field(
        default=False,
        description=(
            "Request token usage on the final stream chunk. Off by default because "
            "several compatible servers reject the stream_options field."
        ),
    )
    extra_body: dict[str, Any] = Field(
        default_factory=dict,
        description="Passed through verbatim, for vendor-specific parameters.",
    )


class OpenAICompatibleChatModel:
    """Adapter over the `/v1/chat/completions` interface."""

    def __init__(self, provider: str, model: str, options: OpenAICompatibleOptions) -> None:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise MissingDependencyError(provider, "openai", "openai") from exc

        if not model:
            raise ConfigurationError(f"Provider {provider!r} requires an explicit model name.")

        preset = _PRESETS.get(provider, _PRESETS["openai_compatible"])
        api_key = options.api_key or _resolve_key(preset)
        if preset.requires_key and not api_key:
            raise ConfigurationError(
                f"Provider {provider!r} needs an API key. Set {preset.api_key_env} "
                f"or llm.options.api_key."
            )

        self._provider = provider
        self._model = model
        self._options = options
        self._client = AsyncOpenAI(
            api_key=api_key or "not-required",
            base_url=options.base_url or preset.base_url,
            timeout=options.timeout,
            max_retries=options.max_retries,
        )

    @property
    def model_id(self) -> str:
        return self._model

    @property
    def supports_citations(self) -> bool:
        return False

    async def complete(self, request: ChatRequest) -> ChatResponse:
        try:
            response = await self._client.chat.completions.create(
                **self._build_payload(request), stream=False
            )
        # Broad by intent: the OpenAI-compatible SDK errors are translated into this
        # package's error hierarchy so callers never import a vendor exception.
        except Exception as exc:
            raise ProviderError(f"{self._provider} request failed: {exc}") from exc

        choice = response.choices[0]
        text = _require_answer(
            _strip_reasoning(choice.message.content or ""),
            choice.finish_reason,
            self._provider,
        )
        return ChatResponse(
            text=text,
            citations=parse_marker_citations(text, request.sources),
            usage=_parse_usage(response.usage),
            model=response.model or self._model,
            stop_reason=choice.finish_reason,
        )

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        """Stream text, resolving citations from the accumulated answer at the end.

        Markers can straddle chunk boundaries, so parsing has to wait for the full
        text. Buffering only the text (not the deltas) keeps memory flat.
        """
        payload = self._build_payload(request)
        if self._options.include_usage_in_stream:
            payload["stream_options"] = {"include_usage": True}

        buffer: list[str] = []
        usage = Usage()
        finish_reason: str | None = None

        try:
            stream = await self._client.chat.completions.create(**payload, stream=True)
            async for chunk in stream:
                if chunk.usage is not None:
                    usage = _parse_usage(chunk.usage)
                if not chunk.choices:
                    continue
                choice = chunk.choices[0]
                if choice.finish_reason:
                    finish_reason = choice.finish_reason
                delta = choice.delta.content
                if delta:
                    buffer.append(delta)
                    yield TextDelta(text=delta)
        except Exception as exc:
            raise ProviderError(f"{self._provider} stream failed: {exc}") from exc

        # Citations are parsed from the stripped answer, never from the raw stream:
        # a marker the model emitted while reasoning aloud is not a citation.
        answer = _require_answer(
            _strip_reasoning("".join(buffer)), finish_reason, self._provider
        )
        for citation in parse_marker_citations(answer, request.sources):
            yield CitationDelta(citation=citation)
        yield StreamEnd(usage=usage, stop_reason=finish_reason)

    def _build_payload(self, request: ChatRequest) -> dict[str, Any]:
        messages: list[dict[str, Any]] = []
        system = compose_grounded_system(request)
        if system:
            messages.append({"role": "system", "content": system})
        messages.extend(
            {"role": message.role.value, "content": message.content}
            for message in request.messages
        )

        payload: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            self._options.max_tokens_param: request.max_tokens,
        }
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        payload.update(self._options.extra_body)
        return payload


# Matches a reasoning block only at the very start of the answer, which is where a
# hybrid reasoning model emits one. Anchoring it means a source document that
# happens to discuss "<think>" cannot have its quoted content silently deleted.
_LEADING_THINK = re.compile(r"\A\s*<think>.*?(?:</think>|\Z)", re.DOTALL)


def _strip_reasoning(text: str) -> str:
    """Remove a leading `<think>` block from a reasoning model's answer.

    Ollama already separates reasoning from content, but vLLM, LM Studio and
    llama.cpp serving the same Qwen3 weights emit the block inline. Stripping it
    matters for more than tidiness: citation markers are parsed out of this text,
    and a `[2]` the model wrote while thinking aloud would otherwise become a
    citation on a claim the answer never made.

    An unclosed block means the token budget ran out mid-thought. That collapses to
    an empty string, which `_require_answer` then reports as the budget problem it is.
    """
    return _LEADING_THINK.sub("", text, count=1).strip()


def _require_answer(text: str, finish_reason: str | None, provider: str) -> str:
    """Fail loudly when the model produced no answer text.

    An empty completion reaching the answerer is indistinguishable from a model
    that had nothing to say, and is finalised as an uncited — therefore abstained —
    answer. The user is then told the corpus lacks the information when the real
    cause is a token budget consumed entirely by reasoning. Diagnosing that from an
    abstention message is close to impossible, so it is raised instead.
    """
    if text:
        return text
    if finish_reason == "length":
        raise ProviderError(
            f"{provider} returned no answer: the completion budget was exhausted "
            f"before any answer text was produced. Raise generation.max_tokens, or "
            f"lower the model's reasoning effort "
            f"(llm.options.extra_body.reasoning_effort)."
        )
    raise ProviderError(
        f"{provider} returned an empty completion (finish_reason={finish_reason!r})."
    )


def _parse_usage(usage: Any) -> Usage:
    if usage is None:
        return Usage()
    cached = 0
    details = getattr(usage, "prompt_tokens_details", None)
    if details is not None:
        cached = getattr(details, "cached_tokens", 0) or 0
    return Usage(
        input_tokens=getattr(usage, "prompt_tokens", 0) or 0,
        output_tokens=getattr(usage, "completion_tokens", 0) or 0,
        cached_input_tokens=cached,
    )


def _resolve_key(preset: _Preset) -> str | None:
    return os.environ.get(preset.api_key_env) if preset.api_key_env else None


def _make_factory(provider: str) -> Any:
    def factory(config: ComponentConfig) -> ChatModel:
        return OpenAICompatibleChatModel(
            provider, config.model, OpenAICompatibleOptions.model_validate(config.options)
        )

    return factory


for _name in _PRESETS:
    llm_registry.register(_name)(_make_factory(_name))
