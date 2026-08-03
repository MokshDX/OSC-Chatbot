"""Chat provider backed by any LangChain `BaseChatModel`.

**Why this exists.** OSC ships hand-written adapters for the providers it actually
uses, and those stay: they are smaller, they carry no framework in the request
path, and the Anthropic one is the only implementation in the codebase that returns
*verified* citations. What they cannot do is cover the long tail — Bedrock, Vertex,
Azure OpenAI, Cohere, Fireworks, Mistral, Databricks and whatever ships next month.
Writing an adapter each time is the work this bridge removes: LangChain maintains
those integrations, and one adapter makes all of them selectable by configuration.

The result is a deliberate two-tier provider strategy:

* **Tier 1 — native adapters.** The default path. Direct SDK use, no framework, and
  provider-specific capabilities (Anthropic's verified citations, the reasoning
  controls on the OpenAI-compatible family) are available because nothing is
  normalising them away.
* **Tier 2 — this bridge.** Everything else, at the cost of marker-parsed rather
  than verified citations and one more layer to reason about. Reaching for a
  provider OSC has never used is a configuration change, not a sprint.

**Selection is explicit.** The class is named by import path rather than resolved
from a short string by `init_chat_model`:

    llm:
      provider: langchain
      model: mistral-large-latest
      options:
        class_path: langchain_mistralai.ChatMistralAI
        init: {timeout: 60}

`init_chat_model` would accept `mistralai:mistral-large-latest` instead, but it
lives in the `langchain` meta-package, which pulls LangGraph and its dependency
tree in to save one line of configuration. An import path also fails at startup
with the name of the module to install, rather than inside a resolver.

Citations use the same marker path as every other non-Anthropic provider, so an
answer produced through this bridge is indistinguishable downstream from one
produced by a native adapter.
"""

from __future__ import annotations

import importlib
from collections.abc import AsyncIterator
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ...errors import ConfigurationError, MissingDependencyError, ProviderError
from ...grounding import (
    compose_grounded_system,
    parse_marker_citations,
    require_answer,
    strip_reasoning,
)
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


class LangChainChatOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    class_path: str = Field(
        description=(
            "Dotted path to a LangChain BaseChatModel subclass, e.g. "
            "'langchain_anthropic.ChatAnthropic'."
        )
    )
    init: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Keyword arguments for the class constructor. Passed through verbatim, "
            "so any integration-specific parameter is reachable without a code change."
        ),
    )
    bind_max_tokens: bool = Field(
        default=True,
        description=(
            "Pass generation.max_tokens to the model per request. On by default so "
            "the configured budget is honoured; turn it off for an integration that "
            "rejects the parameter and set the limit in `init` instead."
        ),
    )


class LangChainChatModel:
    """Adapter presenting a LangChain chat model as an OSC `ChatModel`.

    Translation happens at both edges and nowhere else: OSC types in, LangChain
    messages out, LangChain messages in, OSC types out. No LangChain object escapes
    this module, which is what keeps the rest of the system framework-free.
    """

    def __init__(self, model: str, options: LangChainChatOptions) -> None:
        self._model_name = model
        self._options = options
        self._client = _instantiate(options.class_path, model, options.init)

    @property
    def model_id(self) -> str:
        return self._model_name or self._options.class_path

    @property
    def supports_citations(self) -> bool:
        """False: LangChain normalises provider responses to a common message shape.

        Anthropic's citation blocks do survive into `content`, but as raw provider
        payload that this adapter would have to re-parse per provider — which is the
        work the native Anthropic adapter already does properly. Claiming native
        citation support here would mean asserting a verification that is not
        happening.
        """
        return False

    async def complete(self, request: ChatRequest) -> ChatResponse:
        client = self._bind(request)
        try:
            message = await client.ainvoke(_to_langchain_messages(request))
        # Broad by intent: LangChain surfaces each integration's own exception type,
        # and callers must never have to import one.
        except Exception as exc:
            raise ProviderError(f"langchain ({self._options.class_path}) failed: {exc}") from exc

        stop_reason = _stop_reason(message)
        text = require_answer(strip_reasoning(_text_of(message)), stop_reason, "langchain")
        return ChatResponse(
            text=text,
            citations=parse_marker_citations(text, request.sources),
            usage=_parse_usage(message),
            model=_reported_model(message) or self.model_id,
            stop_reason=stop_reason,
        )

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        """Stream text, resolving citations once the full answer is known.

        Markers can straddle chunk boundaries, so parsing waits for the complete
        text — the same contract as the OpenAI-compatible adapter, so the answerer
        behaves identically whichever produced the stream.
        """
        client = self._bind(request)
        buffer: list[str] = []
        usage = Usage()
        stop_reason: str | None = None

        try:
            async for chunk in client.astream(_to_langchain_messages(request)):
                # Usage arrives on a late chunk for most integrations and on none
                # for some. Accumulating whichever chunks carry it is the only shape
                # that works across both.
                chunk_usage = _parse_usage(chunk)
                if chunk_usage != Usage():
                    usage = chunk_usage
                stop_reason = _stop_reason(chunk) or stop_reason
                delta = _text_of(chunk)
                if delta:
                    buffer.append(delta)
                    yield TextDelta(text=delta)
        except Exception as exc:
            raise ProviderError(
                f"langchain ({self._options.class_path}) stream failed: {exc}"
            ) from exc

        answer = require_answer(strip_reasoning("".join(buffer)), stop_reason, "langchain")
        for citation in parse_marker_citations(answer, request.sources):
            yield CitationDelta(citation=citation)
        yield StreamEnd(usage=usage, stop_reason=stop_reason)

    def _bind(self, request: ChatRequest) -> Any:
        """Apply the per-request generation parameters.

        `bind` rather than constructor arguments because `max_tokens` is a property
        of the request (it is sized against the retrieved sources) and not of the
        deployment.
        """
        bound: dict[str, Any] = {}
        if self._options.bind_max_tokens:
            bound["max_tokens"] = request.max_tokens
        if request.temperature is not None:
            bound["temperature"] = request.temperature
        return self._client.bind(**bound) if bound else self._client


def _instantiate(class_path: str, model: str, init: dict[str, Any]) -> Any:
    """Import and construct the LangChain chat model named by `class_path`."""
    module_name, _, class_name = class_path.rpartition(".")
    if not module_name:
        raise ConfigurationError(
            f"llm.options.class_path must be a dotted path such as "
            f"'langchain_anthropic.ChatAnthropic', got {class_path!r}."
        )

    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        # The integration package name is the actionable part of this failure, so
        # it is what the operator is told to install.
        raise MissingDependencyError("langchain", module_name, "langchain") from exc

    try:
        factory = getattr(module, class_name)
    except AttributeError as exc:
        raise ConfigurationError(f"{module_name} has no attribute {class_name!r}.") from exc

    kwargs = dict(init)
    if model:
        kwargs.setdefault("model", model)
    try:
        return factory(**kwargs)
    except Exception as exc:
        raise ConfigurationError(
            f"Could not construct {class_path} with {sorted(kwargs)}: {exc}"
        ) from exc


def _to_langchain_messages(request: ChatRequest) -> list[Any]:
    """Translate an OSC request into LangChain messages.

    Sources are folded into the system message by `compose_grounded_system`, exactly
    as the OpenAI-compatible adapter does, so the nonce-delimited injection defence
    and the citation instruction apply here unchanged.
    """
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

    messages: list[Any] = []
    system = compose_grounded_system(request)
    if system:
        messages.append(SystemMessage(content=system))
    for message in request.messages:
        if message.role is Role.ASSISTANT:
            messages.append(AIMessage(content=message.content))
        else:
            messages.append(HumanMessage(content=message.content))
    return messages


def _text_of(message: Any) -> str:
    """Extract plain text from a LangChain message or chunk.

    `.text` is the documented accessor from langchain-core 1.0 onward. It handles
    both plain-string content and the content-block form that multimodal and
    reasoning models return, concatenating only the text blocks — which is exactly
    what a grounded answer should be built from.
    """
    text = getattr(message, "text", None)
    if text is None:  # pragma: no cover - every LangChain message defines .text
        content = getattr(message, "content", "")
        return content if isinstance(content, str) else ""
    return str(text)


def _parse_usage(message: Any) -> Usage:
    metadata = getattr(message, "usage_metadata", None) or {}
    details = metadata.get("input_token_details") or {}
    return Usage(
        input_tokens=metadata.get("input_tokens", 0) or 0,
        output_tokens=metadata.get("output_tokens", 0) or 0,
        cached_input_tokens=details.get("cache_read", 0) or 0,
    )


def _stop_reason(message: Any) -> str | None:
    """The provider's own stop reason, under whichever key it used.

    LangChain passes `response_metadata` through largely untouched, so the key
    differs by vendor. Truncation is the failure this value exists to reveal, and it
    is worth a small lookup table to keep it visible for every provider.
    """
    metadata = getattr(message, "response_metadata", None) or {}
    for key in ("finish_reason", "stop_reason", "done_reason"):
        value = metadata.get(key)
        if value:
            return str(value)
    return None


def _reported_model(message: Any) -> str:
    metadata = getattr(message, "response_metadata", None) or {}
    return str(metadata.get("model_name") or metadata.get("model") or "")


@llm_registry.register("langchain")
def _build(config: ComponentConfig) -> ChatModel:
    return LangChainChatModel(
        config.model, LangChainChatOptions.model_validate(config.options)
    )
