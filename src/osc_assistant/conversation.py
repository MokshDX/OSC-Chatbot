"""Session-scoped conversational memory.

Until this module existed, every question was independent: the API accepted a
`history` array and the caller was responsible for keeping it. That works for a
programmatic client and not for a chat UI, and it makes "does this system handle
follow-ups?" a question about the *caller* rather than about OSC.

Three pieces, in dependency order:

* `SessionStore` — the seam. Where conversation state lives.
* `InMemorySessionStore` — the only implementation today. Process-local, bounded,
  and destroyed on close, on idle expiry and on restart.
* `Conversation` — binds a session to the `Answerer`: load history, answer, record
  the turn. It exists so that the three call sites that need this (the buffered API
  route, the streaming API route and the CLI) share one definition of what a turn
  *is*, rather than three that drift.

**Memory is deliberately not durable in this phase** (ADR 0013). A conversation is
a working set, not a record: the audit stream already holds one durable entry per
answered question, which is what a compliance or quality question actually wants,
and it holds it without keeping user text in a second place with its own retention
story. `SessionStore` is a Protocol precisely so that a Redis or PostgreSQL backing
can be introduced later without any caller changing — the call sites below depend
on the four methods, never on the dictionary.

**Isolation is structural, not enforced.** Sessions are keyed by an unguessable
token in a private mapping; there is no query that spans sessions and no way to
reach one session's history from another's id. That matters more than usual here
because no endpoint on this service is authenticated yet, so the session id is the
only thing standing between two users' conversations.
"""

from __future__ import annotations

import secrets
import time
from collections import OrderedDict
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from .errors import AssistantError
from .generation.answerer import AnswerComplete, Answerer, AnswerEvent
from .logging import audit, get_logger
from .observability import annotate, span, trace
from .settings import SessionSettings
from .types import Answer, Message, Role

log = get_logger(__name__)

# Session ids are 32 hex characters from a CSPRNG. Not a UUID4: the point is that
# the id is unguessable, and `secrets` says that in the name where `uuid` does not.
_ID_BYTES = 16


class UnknownSessionError(AssistantError):
    """The session id is not known to this store.

    An operator problem rather than a bug: the usual causes are a session that was
    closed, one that idled out, and a client that outlived a service restart. All
    three are ordinary, and all three are the client's cue to open a new session.
    """


@dataclass(slots=True)
class SessionState:
    """One conversation's working set.

    `messages` alternates user and assistant and is what reaches the rewriter and
    the prompt. `turns` counts exchanges *ever* recorded rather than
    `len(messages) // 2`, so a session trimmed by `max_messages` still reports its
    true length — which is the number that tells you whether a long conversation is
    degrading, and which is what `session.closed` records in the audit stream.

    Deliberately holds no `id` and no `created_at`. Both were here and both were
    write-only: the id is already the mapping key, and nothing reads a creation
    time — expiry is measured from `last_active_at`. A field nobody reads is a
    field that will be wrong one day without anything noticing.
    """

    last_active_at: float
    messages: list[Message] = field(default_factory=list)
    turns: int = 0


@runtime_checkable
class SessionStore(Protocol):
    """Where conversation state lives between turns.

    Async because the implementation that replaces the in-memory one will be over a
    network, and every caller is already async. Making it async now costs nothing
    and saves changing four call sites later.
    """

    async def create(self) -> str:
        """Open a session and return its id."""
        ...

    async def history(self, session_id: str) -> list[Message]:
        """The messages a new turn in this session should be answered against.

        Raises:
            UnknownSessionError: No such session, or it has expired.
        """
        ...

    async def record(self, session_id: str, question: str, answer: str) -> None:
        """Append one completed exchange.

        Raises:
            UnknownSessionError: No such session, or it has expired.
        """
        ...

    async def destroy(self, session_id: str) -> bool:
        """Destroy a session's memory. Returns whether there was one to destroy.

        Named `destroy` rather than `close` so it cannot be mistaken for the
        component lifecycle `close()` that `Container.shutdown` probes for. That
        probe passes no arguments, so a same-named method taking a session id would
        fail once, in a broad except, as a warning nobody reads.
        """
        ...


class InMemorySessionStore:
    """Process-local conversation memory, bounded three ways.

    The bounds are the design. An unbounded conversation store fails in three
    distinct ways and each needs its own ceiling: total sessions (a client that
    never closes), messages per session (a conversation that grows the prompt until
    generation truncates), and time (a browser tab closed without a DELETE).

    Not thread-safe by construction, and it does not need to be: it is awaited from
    one event loop, and there is no `await` between reading and mutating the mapping
    in any method here, so no other task can interleave.
    """

    def __init__(self, settings: SessionSettings | None = None) -> None:
        self._settings = settings or SessionSettings()
        # Ordered so eviction can be least-recently-used rather than arbitrary. A
        # dict that dropped a random session would make the failure mode
        # unreproducible, which is the worst property a capacity bound can have.
        self._sessions: OrderedDict[str, SessionState] = OrderedDict()

    async def create(self) -> str:
        self._expire_idle()
        session_id = secrets.token_hex(_ID_BYTES)
        self._sessions[session_id] = SessionState(last_active_at=time.monotonic())
        self._evict_over_capacity()
        log.info("session.created", extra={"session_id": session_id, "live": len(self._sessions)})
        return session_id

    async def history(self, session_id: str) -> list[Message]:
        """The messages this session holds, and the start of an interaction.

        Reading **counts as activity**, and that is load-bearing rather than
        incidental. A turn is a read, then a generation that can take ten seconds,
        then a write. If only the write advanced the clock, a session idle for
        59:55 of a one-hour TTL would pass the read, spend ten seconds generating,
        and then fail at `record()` — discarding a turn after the model call had
        already been paid for, and reporting it as an expiry the user could not have
        avoided. Touching here makes the TTL mean "nothing has happened", which is
        what "idle" should mean.
        """
        state = self._require(session_id)
        state.last_active_at = time.monotonic()
        self._sessions.move_to_end(session_id)
        return list(state.messages)

    async def record(self, session_id: str, question: str, answer: str) -> None:
        state = self._require(session_id)
        state.messages.append(Message(role=Role.USER, content=question))
        state.messages.append(Message(role=Role.ASSISTANT, content=answer))
        state.turns += 1
        state.last_active_at = time.monotonic()

        # Trim from the front so the *recent* context survives. A follow-up refers
        # to what was just said, essentially never to the opening of a long
        # conversation, so the oldest exchange is the cheapest thing to lose.
        overflow = len(state.messages) - self._settings.max_messages
        if overflow > 0:
            del state.messages[:overflow]

        self._sessions.move_to_end(session_id)
        log.info(
            "session.turn_recorded",
            extra={
                "session_id": session_id,
                "turns": state.turns,
                "messages_retained": len(state.messages),
                "trimmed": max(0, overflow),
            },
        )

    async def destroy(self, session_id: str) -> bool:
        state = self._sessions.pop(session_id, None)
        if state is None:
            return False
        # Overwriting before dropping the reference is not a security control —
        # Python strings are immutable and copies may exist. It is here so that a
        # lingering reference held by a bug shows an empty session rather than a
        # populated one, which makes "was this closed?" answerable in a debugger.
        state.messages.clear()
        log.info(
            "session.closed",
            extra={"session_id": session_id, "turns": state.turns, "live": len(self._sessions)},
        )
        audit("session_closed", session_id=session_id, turns=state.turns)
        return True

    @property
    def live_sessions(self) -> int:
        """How many sessions are currently held. For `doctor` and for tests."""
        return len(self._sessions)

    def describe(self, session_id: str) -> SessionState | None:
        """Read a session's state without touching its activity clock.

        For diagnostics only. Deliberately not on the `SessionStore` Protocol: a
        remote implementation should not have to support introspection to be a
        usable store, which is the same reasoning that keeps `StoreInspector`
        separate from `VectorStore`.
        """
        return self._sessions.get(session_id)

    def _require(self, session_id: str) -> SessionState:
        self._expire_idle()
        state = self._sessions.get(session_id)
        if state is None:
            raise UnknownSessionError(
                f"No live session {session_id!r}. It was closed, it idled out after "
                f"{self._settings.idle_ttl_seconds:.0f}s, or the service restarted. "
                f"Open a new one with POST /api/sessions."
            )
        return state

    def _expire_idle(self) -> None:
        """Drop sessions untouched for longer than the TTL.

        Swept on access rather than on a timer. A background task would need a
        lifecycle, would keep the event loop awake in a CLI process that is about to
        exit, and would buy nothing: the only cost of a late sweep is memory, and
        `max_sessions` already bounds that.
        """
        cutoff = time.monotonic() - self._settings.idle_ttl_seconds
        expired = [
            session_id
            for session_id, state in self._sessions.items()
            if state.last_active_at < cutoff
        ]
        for session_id in expired:
            state = self._sessions.pop(session_id)
            state.messages.clear()
            log.info(
                "session.expired",
                extra={"session_id": session_id, "turns": state.turns, "reason": "idle_ttl"},
            )

    def _evict_over_capacity(self) -> None:
        while len(self._sessions) > self._settings.max_sessions:
            session_id, state = self._sessions.popitem(last=False)
            state.messages.clear()
            log.warning(
                "session.evicted",
                extra={
                    "session_id": session_id,
                    "turns": state.turns,
                    "reason": "max_sessions",
                    "limit": self._settings.max_sessions,
                },
            )


class Conversation:
    """A multi-turn question-answering session.

    The composition of a `SessionStore` and an `Answerer`, and the only place that
    defines what one turn does: read the history, answer against it, record the
    exchange. Both API routes and the CLI go through here, so a turn means the same
    thing in all three — including the part that is easy to get wrong, which is that
    an abstention is still a turn and still belongs in the history. Dropping it
    would leave a follow-up like "why not?" with nothing to resolve against.
    """

    def __init__(self, answerer: Answerer, store: SessionStore) -> None:
        self._answerer = answerer
        self._store = store

    async def start(self) -> str:
        return await self._store.create()

    async def close(self, session_id: str) -> bool:
        return await self._store.destroy(session_id)

    async def history(self, session_id: str) -> list[Message]:
        """The transcript so far, as the next turn would see it.

        For a client reconnecting to render a conversation, and for the evaluation
        harness checking what a turn was answered against. Reading extends the
        session's life — see `InMemorySessionStore.history`.
        """
        return await self._store.history(session_id)

    async def answer(self, session_id: str, question: str) -> Answer:
        """Answer one turn in `session_id`, recording it in the session's history."""
        with trace("conversation", session_id=session_id, mode="buffered"):
            history = await self._load(session_id, question)
            answer = await self._answerer.answer(question, history)
            await self._store.record(session_id, question, answer.text)
            annotate(abstained=answer.abstained, citations=len(answer.citations))
            return answer

    async def stream(self, session_id: str, question: str) -> AsyncIterator[AnswerEvent]:
        """Stream one turn in `session_id`, recording it when the answer completes.

        The turn is recorded on `AnswerComplete` and nowhere else. `AnswerComplete`
        is the authoritative event — an abstention can replace everything streamed
        before it — so recording the concatenated deltas instead would sometimes
        write a history entry the user never saw. A stream that fails partway
        records nothing, which is correct: there was no answer.
        """
        with trace("conversation", session_id=session_id, mode="stream"):
            history = await self._load(session_id, question)
            async for event in self._answerer.stream(question, history):
                if isinstance(event, AnswerComplete):
                    await self._store.record(session_id, question, event.answer.text)
                    annotate(
                        abstained=event.answer.abstained,
                        citations=len(event.answer.citations),
                    )
                yield event

    async def _load(self, session_id: str, question: str) -> list[Message]:
        """Fetch the history this turn will be answered against.

        Its own span because "the follow-up was answered as if it were a first
        question" and "the follow-up was answered badly" look identical in an
        answer and completely different in a trace. `turns_in_context` of 0 on a
        third question names the bug immediately.

        The enclosing `trace("conversation")` in the callers is what makes this
        span exist at all: `span()` outside a trace is detached and records
        nothing, so loading the history before opening the trace — which is the
        obvious way to write this — produces a trace with no evidence of whether
        there was any context. `Answerer` opens its own `trace("answer")` inside
        ours, and a nested trace extends rather than forks, so one turn is still
        exactly one trace.
        """
        with span("session_context", session_id=session_id) as stage:
            history = await self._store.history(session_id)
            stage.set(
                messages_in_context=len(history),
                turns_in_context=len(history) // 2,
                is_follow_up=bool(history),
            )
            stage.set_text("question", question)
        return history
