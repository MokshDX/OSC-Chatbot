"""Server-sent event encoding.

SSE rather than WebSockets: the stream is one-directional, it survives proxies that
mishandle upgrades, and browsers reconnect on their own. The named-event form is
used so a client can dispatch on the event name without first parsing the payload.
"""

from __future__ import annotations

import json
from typing import Any

SSE_MEDIA_TYPE = "text/event-stream"

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    # Nginx buffers responses by default, which defeats streaming entirely.
    "X-Accel-Buffering": "no",
}


def encode_event(event: str, data: Any) -> str:
    """Encode one named SSE frame.

    The payload is serialised without literal newlines so it always occupies a
    single `data:` line, which keeps the framing trivial for clients.
    """
    payload = json.dumps(data, default=str, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"
