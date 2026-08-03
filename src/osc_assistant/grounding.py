"""Grounding and citation handling for providers without native citation support.

Anthropic's API resolves citations itself: you hand it structured documents and it
returns, per span of the answer, the exact source text that supports it. No other
provider we target does this, so those adapters render sources into the prompt,
ask for `[n]` markers, and parse them back out here.

Both paths converge on the same `Citation` shape, so nothing downstream — the
answerer, the API, the client — needs to know which provider produced the answer.
The trade-off is honest: parsed markers assert a citation, whereas native
citations verify one against the source text. That difference is measured by the
evaluation harness rather than hidden.
"""

from __future__ import annotations

import re
import secrets
from collections.abc import Sequence

from .errors import ProviderError
from .types import ChatRequest, Citation, SourceDocument

_MARKER_PATTERN = re.compile(r"\[(\d{1,3})\]")

CITATION_INSTRUCTION = (
    "Cite your sources. After every sentence containing a fact drawn from the "
    "sources, append the matching source marker in square brackets, for example "
    "[1] or [2][3]. Only cite sources you actually used. Never invent a marker "
    "number that does not appear in the sources."
)


def render_sources(sources: Sequence[SourceDocument], *, nonce: str | None = None) -> str:
    """Render sources as a delimited block for inclusion in a prompt.

    The delimiter carries a per-request random `nonce`. Indexed documents are
    untrusted input — anyone who can add a file to the corpus can put text in it —
    and with a fixed delimiter a document body containing `</source></sources>`
    closes the data block and lands its own text where the model reads it as
    instruction. A nonce cannot be guessed by content written in advance, so the
    boundary holds without escaping the body.

    Escaping the body instead was rejected: it would corrupt exactly the technical
    content this corpus is full of, turning `<div>` in a source into `&lt;div&gt;`
    for the model to read and quote back.

    Args:
        sources: Retrieved chunks, rendered in order and numbered from 1.
        nonce: Delimiter suffix. Generated per call unless supplied; pass a fixed
            value only in tests.
    """
    if not sources:
        return ""

    nonce = nonce or secrets.token_hex(8)
    tag = f"source-{nonce}"
    blocks = [
        f'<{tag} index="{index}" title="{_escape(source.title)}">\n'
        f"{source.text.strip()}\n"
        f"</{tag}>"
        for index, source in enumerate(sources, start=1)
    ]
    return f"<sources-{nonce}>\n" + "\n\n".join(blocks) + f"\n</sources-{nonce}>"


def compose_grounded_system(request: ChatRequest, *, nonce: str | None = None) -> str:
    """Fold the system prompt, citation instruction and sources into one string.

    Used by every adapter without native citation support. Sources go last so the
    stable prefix — the instructions — stays byte-identical between requests, which
    is what lets a backend cache it.
    """
    parts: list[str] = []
    if request.system:
        parts.append(request.system)
    if request.sources:
        parts.append(CITATION_INSTRUCTION)
        parts.append(render_sources(request.sources, nonce=nonce))
    return "\n\n".join(parts)


def parse_marker_citations(text: str, sources: Sequence[SourceDocument]) -> list[Citation]:
    """Extract citations from `[n]` markers in `text`.

    Markers referring to a source that was not supplied are ignored rather than
    treated as an error: a hallucinated marker should degrade to an uncited claim,
    which the `require_citations` policy can then act on, not crash the request.

    Returns citations ordered by first appearance in the answer.
    """
    seen: dict[int, Citation] = {}
    for match in _MARKER_PATTERN.finditer(text):
        index = int(match.group(1))
        if index in seen or not 1 <= index <= len(sources):
            continue
        source = sources[index - 1]
        seen[index] = Citation(
            index=index,
            chunk_id=source.chunk_id,
            document_id=source.document_id,
            title=source.title,
            source_uri=source.source_uri,
        )
    return list(seen.values())


# --------------------------------------------------------- reasoning-model hygiene
#
# These live here, beside citation parsing, because that is what they protect. They
# are shared by every marker-parsing adapter — the OpenAI-compatible family and the
# LangChain bridge — since any of them may be pointed at a hybrid reasoning model.
# Keeping one copy means a fix reaches all of them.

# Matches a reasoning block only at the very start of the answer, which is where a
# hybrid reasoning model emits one. Anchoring it means a source document that
# happens to discuss "<think>" cannot have its quoted content silently deleted.
_LEADING_THINK = re.compile(r"\A\s*<think>.*?(?:</think>|\Z)", re.DOTALL)


def strip_reasoning(text: str) -> str:
    """Remove a leading `<think>` block from a reasoning model's answer.

    Ollama already separates reasoning from content, but vLLM, LM Studio and
    llama.cpp serving the same Qwen3 weights emit the block inline. Stripping it
    matters for more than tidiness: citation markers are parsed out of this text,
    and a `[2]` the model wrote while thinking aloud would otherwise become a
    citation on a claim the answer never made.

    An unclosed block means the token budget ran out mid-thought. That collapses to
    an empty string, which `require_answer` then reports as the budget problem it is.
    """
    return _LEADING_THINK.sub("", text, count=1).strip()


def require_answer(text: str, finish_reason: str | None, provider: str) -> str:
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


def _escape(value: str) -> str:
    """Escape the characters that would otherwise break out of an XML-ish attribute."""
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "'")
