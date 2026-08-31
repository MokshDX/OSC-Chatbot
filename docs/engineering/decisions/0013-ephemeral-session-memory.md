# ADR 0013 — Conversational memory is ephemeral, process-local and bounded

**Status:** Accepted · **Date:** Phase 6

---

## Context

Through Phase 5 OSC was a single-turn question answering service. The API accepted a
`history` array and the caller was responsible for keeping it; the bundled UI did not
send one, so every follow-up was an independent question. `PROJECT_STATUS.md` recorded
"conversation persistence" as item 4 of what was not implemented.

The pieces for multi-turn were already in place and unused. `Answerer.answer()` and
`Answerer.stream()` both take `history`. `QueryRewriter` exists specifically to resolve
conversational references into a standalone retrieval query, and takes `history` too.
What was missing was not a capability — it was somewhere for the conversation to live
between turns.

That absence is also what made the feature a question about *storage*, and storage is
where a conversational feature usually acquires a database table it did not need.

## Decision

**Session state lives in the answering process, is bounded three ways, and is
destroyed on close, on idle expiry and on restart.**

Three pieces, in `conversation.py`:

* **`SessionStore`** — a `Protocol` with four methods (`create`, `history`, `record`,
  `destroy`). The seam.
* **`InMemorySessionStore`** — the only implementation. An `OrderedDict` with LRU
  eviction, per-session message trimming and idle expiry swept on access.
* **`Conversation`** — binds a store to an `Answerer`: read history, answer against it,
  record the exchange. It exists so the three call sites that need this — the buffered
  route, the streaming route and the evaluation harness — share one definition of what
  a turn is.

**No registry.** The five swappable seams each have one because an operator picks
between implementations by configuration; there is exactly one session store, so
adding `session_store_registry` today would be a naming ceremony around a single
constructor. `Container.sessions` builds it directly. When a durable store lands, that
line becomes a registry lookup and nothing above it changes — which is the property
the Protocol is actually buying.

**Three bounds, because an unbounded conversation store fails in three unrelated ways:**

| Bound | Failure it prevents |
|---|---|
| `max_messages` (20) | A long conversation growing the prompt until generation truncates |
| `max_sessions` (1000) | A client that never closes |
| `idle_ttl_seconds` (3600) | A browser tab closed without a DELETE |

Trimming is from the **front**. A follow-up refers to what was just said, essentially
never to the opening of a long conversation, so the oldest exchange is the cheapest
thing to lose.

**Session ids are `secrets.token_hex(16)`.** Unguessability is load-bearing here in a
way it would not be under authentication: no endpoint on this service is authenticated
yet, so the session id is the only thing standing between two users' conversations.

## Alternatives considered

**A `conversations` table in PostgreSQL.** The obvious "proper" answer, and rejected
for the reasons ADR 0004 rejected a traces table: it puts write load on the primary
datastore for a feature that does not need durability, and it creates a second place
where user text is retained, with its own retention and deletion story. The audit
stream already holds one durable record per answered question — which is what a
compliance or quality question actually wants — without any of that.

**Redis.** A dependency, a deployment component and a failure mode, bought for a
single-process deployment that has neither yet. The Protocol is there so this is a
later decision rather than a rewrite.

**Keep it client-side — just make the UI send `history`.** Genuinely simpler, and it is
still supported: `history` on the request body works and is the right shape for a
stateless programmatic integration. Rejected as the *default* because it puts the
security boundary in the client. A caller replaying a transcript can replay any
transcript, including one it composed, and with no authentication there is nothing to
check it against. Server-held history means the server knows what was actually said.

The two are mutually exclusive on one request, and supplying both is a 422 rather than
a silent choice about which to believe.

**Summarising older turns instead of trimming them.** A model call per turn, on the
critical path, to compress context that is bounded at ten exchanges anyway. Not worth
it at this size; revisit if `max_messages` ever needs to be large.

## Consequences

**Memory does not survive a restart, and clients must handle that.** An expired or
unknown session is a 404 with a message naming the three ordinary causes — closed,
idled out, service restarted — and the client's correct response to all three is to
open a new session. This is a real limitation on a single-process deployment and would
become a real problem behind more than one replica, where a client's next turn may
reach a process that has never heard of its session. **Sticky sessions or a shared
store is a prerequisite for horizontal scaling**, and this ADR is the reason it is not
free.

**History reaches generation but not retrieval, unless query rewriting is on.**
Retrieval sees history only through `QueryRewriter`. With `rewrite_queries: false` a
follow-up is *generated* with full context and *retrieved* for as if it were
standalone. The conversational evaluation measures this directly — `follow_up_lift`
compares each context-dependent turn against the same question run cold — and reported
a lift of exactly 0.0 on the default profile, which is what made the gap a number
rather than a suspicion.

**An abstention is recorded as a turn.** Dropping it would leave a follow-up like "why
not?" with nothing to resolve against. The abstention *message* goes into the history,
because that is what the user saw.

**A stream that fails partway records nothing.** The turn is recorded on
`AnswerComplete` and nowhere else, because that event is authoritative — an abstention
can replace everything streamed before it — so recording concatenated deltas would
sometimes write a history entry the user never saw.

**The store is not thread-safe**, and does not need to be: it is awaited from one event
loop and no method has an `await` between reading and mutating the mapping. A durable
implementation will not have that luxury, which is worth knowing before writing one.
