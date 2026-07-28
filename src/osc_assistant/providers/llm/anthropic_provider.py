"""Anthropic chat provider.

This is the only adapter with native citation support: sources are passed as
structured `document` blocks with citations enabled, and the API returns, for each
cited span of the answer, the exact source text that supports it. That is a
verified citation rather than an asserted one, which is why Anthropic is the
default answer model. Every other adapter falls back to marker parsing.

Two provider-specific details this adapter absorbs so callers never see them:

* Current Opus and Sonnet models reject `temperature`, `top_p` and `top_k`
  outright, so `ChatRequest.temperature` is deliberately ignored here.
* `effort` is only accepted by newer models, so it is sent only when configured.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ...errors import MissingDependencyError, ProviderError
from ...protocols import ChatModel
from ...registries import llm_registry
from ...registry import ComponentConfig
from ...types import (
    ChatRequest,
    ChatResponse,
    Citation,
    CitationDelta,
    Message,
    SourceDocument,
    StreamEnd,
    StreamEvent,
    TextDelta,
    Usage,
)

DEFAULT_MODEL = "claude-opus-5"


class AnthropicOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key: str | None = Field(
        default=None, description="Falls back to the SDK's own credential resolution."
    )
    base_url: str | None = None
    timeout: float = 120.0
    max_retries: int = 2
    effort: str | None = Field(
        default=None,
        description=(
            "One of low/medium/high/xhigh/max on models that support it. Left unset "
            "by default because older models reject the parameter."
        ),
    )
    cache_system_prompt: bool = Field(
        default=True,
        description=(
            "Mark the system prompt as cacheable. Requires the prompt to stay "
            "byte-identical between requests, which is why no dynamic value is "
            "ever interpolated into it."
        ),
    )


class AnthropicChatModel:
    """Adapter over the Anthropic Messages API.

    Satisfies `protocols.ChatModel` structurally; it deliberately does not inherit
    from it, so the protocol stays a description of a shape rather than a base class.
    """

    def __init__(self, model: str, options: AnthropicOptions) -> None:
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise MissingDependencyError("anthropic", "anthropic", "anthropic") from exc

        self._model = model or DEFAULT_MODEL
        self._options = options
        self._client = anthropic.AsyncAnthropic(
            api_key=options.api_key,
            base_url=options.base_url,
            timeout=options.timeout,
            max_retries=options.max_retries,
        )

    @property
    def model_id(self) -> str:
        return self._model

    @property
    def supports_citations(self) -> bool:
        return True

    async def complete(self, request: ChatRequest) -> ChatResponse:
        payload = self._build_payload(request)
        try:
            response = await self._client.messages.create(**payload)
        # Broad by intent: Anthropic SDK errors are translated into this
        # package's error hierarchy so callers never import a vendor exception.
        except Exception as exc:
            raise ProviderError(f"Anthropic request failed: {exc}") from exc

        text, citations = _parse_content(response.content, request.sources)
        return ChatResponse(
            text=text,
            citations=citations,
            usage=_parse_usage(response.usage),
            model=getattr(response, "model", self._model),
            stop_reason=getattr(response, "stop_reason", None),
        )

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        """Stream the answer, then emit citations once the message is complete.

        Text is streamed as it arrives so time-to-first-token stays low. Citations
        are resolved from the final message rather than from incremental deltas:
        a citation is only meaningful once its span has finished, and reading them
        off the completed message keeps this adapter independent of the wire-level
        delta shape.
        """
        payload = self._build_payload(request)
        try:
            async with self._client.messages.stream(**payload) as stream:
                async for chunk in stream.text_stream:
                    if chunk:
                        yield TextDelta(text=chunk)
                final = await stream.get_final_message()
        except Exception as exc:
            raise ProviderError(f"Anthropic stream failed: {exc}") from exc

        _, citations = _parse_content(final.content, request.sources)
        for citation in citations:
            yield CitationDelta(citation=citation)
        yield StreamEnd(
            usage=_parse_usage(final.usage),
            stop_reason=getattr(final, "stop_reason", None),
        )

    def _build_payload(self, request: ChatRequest) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self._model,
            "max_tokens": request.max_tokens,
            "messages": _build_messages(request.messages, request.sources),
        }
        if request.system:
            block: dict[str, Any] = {"type": "text", "text": request.system}
            if self._options.cache_system_prompt:
                block["cache_control"] = {"type": "ephemeral"}
            payload["system"] = [block]
        if self._options.effort:
            payload["output_config"] = {"effort": self._options.effort}
        return payload


def _build_messages(
    messages: list[Message], sources: list[SourceDocument]
) -> list[dict[str, Any]]:
    """Attach sources as citable documents on the final user turn.

    Sources belong to the current question, so they ride on the last user message
    rather than the system prompt. Keeping them out of the system prompt is also
    what allows the system prompt to stay cacheable across requests.
    """
    rendered: list[dict[str, Any]] = [
        {"role": message.role.value, "content": message.content} for message in messages
    ]
    if not sources:
        return rendered

    document_blocks: list[dict[str, Any]] = [
        {
            "type": "document",
            "source": {"type": "text", "media_type": "text/plain", "data": source.text},
            "title": source.title,
            "citations": {"enabled": True},
        }
        for source in sources
    ]

    last_user = _last_user_index(rendered)
    if last_user is None:
        rendered.append({"role": "user", "content": document_blocks})
        return rendered

    question = rendered[last_user]["content"]
    rendered[last_user] = {
        "role": "user",
        "content": [*document_blocks, {"type": "text", "text": question}],
    }
    return rendered


def _last_user_index(messages: list[dict[str, Any]]) -> int | None:
    for index in range(len(messages) - 1, -1, -1):
        if messages[index]["role"] == "user":
            return index
    return None


def _parse_content(
    blocks: list[Any], sources: list[SourceDocument]
) -> tuple[str, list[Citation]]:
    """Flatten response blocks into text, appending a marker after each cited span.

    The API splits the answer into one text block per citation boundary. We
    reassemble those into a single string and insert `[n]` markers so the rendered
    answer matches the marker-based fallback exactly.
    """
    parts: list[str] = []
    citations: dict[int, Citation] = {}

    for block in blocks:
        if getattr(block, "type", None) != "text":
            continue
        parts.append(block.text)
        for raw in getattr(block, "citations", None) or []:
            index = getattr(raw, "document_index", None)
            if index is None or not 0 <= index < len(sources):
                continue
            marker = index + 1
            source = sources[index]
            citations.setdefault(
                marker,
                Citation(
                    index=marker,
                    chunk_id=source.chunk_id,
                    document_id=source.document_id,
                    title=source.title,
                    source_uri=source.source_uri,
                    quoted_text=getattr(raw, "cited_text", "") or "",
                ),
            )
            parts.append(f"[{marker}]")

    ordered = [citations[key] for key in sorted(citations)]
    return "".join(parts), ordered


def _parse_usage(usage: Any) -> Usage:
    return Usage(
        input_tokens=getattr(usage, "input_tokens", 0) or 0,
        output_tokens=getattr(usage, "output_tokens", 0) or 0,
        cached_input_tokens=getattr(usage, "cache_read_input_tokens", 0) or 0,
    )


@llm_registry.register("anthropic")
def _build(config: ComponentConfig) -> ChatModel:
    return AnthropicChatModel(config.model, AnthropicOptions.model_validate(config.options))
