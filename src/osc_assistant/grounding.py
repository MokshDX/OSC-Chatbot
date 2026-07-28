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


def _escape(value: str) -> str:
    """Escape the characters that would otherwise break out of an XML-ish attribute."""
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "'")
