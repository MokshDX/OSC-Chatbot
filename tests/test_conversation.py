"""Session-scoped conversational memory.

The properties tested here are the ones a chatbot is judged on and the ones that
are cheap to get subtly wrong: that a follow-up actually sees the previous turn,
that two conversations cannot see each other, and that closing one destroys it.

Isolation is tested by *behaviour* rather than by reading the mapping — asserting
`len(store._sessions) == 2` would pass just as happily if `history()` returned the
union of both. The question worth asking is what the answerer was handed.
"""

from __future__ import annotations

import asyncio

import pytest

from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
from osc_assistant.conversation import (
    Conversation,
    InMemorySessionStore,
    SessionStore,
    UnknownSessionError,
)
from osc_assistant.generation import AnswerComplete, Answerer, RetrievalReady
from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader
from osc_assistant.observability import RECORDER, configure_observability
from osc_assistant.providers.reranking.noop import NoopReranker
from osc_assistant.providers.vectorstores.memory import MemoryVectorStore
from osc_assistant.retrieval import RetrievalPipeline
from osc_assistant.settings import GenerationSettings, RetrievalSettings, SessionSettings
from osc_assistant.types import Document, Role, TextDelta

from .conftest import FailingChatModel, StubChatModel, StubEmbeddingModel


@pytest.fixture
async def conversation(
    store: MemoryVectorStore, embeddings: StubEmbeddingModel, documents: list[Document]
) -> tuple[Conversation, StubChatModel, InMemorySessionStore]:
    """A `Conversation` over the shared fixture corpus, with an inspectable model.

    Returns the chat model too: what a turn actually sent to generation is the
    only honest way to assert that history reached it.
    """
    await IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
        embeddings=embeddings,
        store=store,
    ).ingest(InMemoryLoader(documents).load())

    model = StubChatModel()
    answerer = Answerer(
        retrieval=RetrievalPipeline(
            store=store,
            embeddings=embeddings,
            reranker=NoopReranker(),
            settings=RetrievalSettings(rewrite_queries=False, top_k=4),
        ),
        model=model,  # type: ignore[arg-type]
        settings=GenerationSettings(),
    )
    sessions = InMemorySessionStore()
    return Conversation(answerer=answerer, store=sessions), model, sessions


# ------------------------------------------------------------------ the store


async def test_the_protocol_is_satisfied_structurally() -> None:
    """`InMemorySessionStore` is a `SessionStore` without inheriting from it.

    The same rule the five provider seams follow: a durable implementation must be
    able to satisfy this by shape alone, with no base class to import.
    """
    assert isinstance(InMemorySessionStore(), SessionStore)


async def test_a_new_session_starts_empty() -> None:
    store = InMemorySessionStore()
    session = await store.create()
    assert await store.history(session) == []


async def test_a_recorded_turn_becomes_user_then_assistant_messages() -> None:
    store = InMemorySessionStore()
    session = await store.create()
    await store.record(session, "How many vacation days?", "Twenty five.")

    history = await store.history(session)
    assert [(message.role, message.content) for message in history] == [
        (Role.USER, "How many vacation days?"),
        (Role.ASSISTANT, "Twenty five."),
    ]


async def test_history_is_a_copy_so_a_caller_cannot_mutate_the_session() -> None:
    """The list handed out is not the list held.

    `Answerer._build_request` does `[*history, Message(...)]`, which is safe today.
    A future caller appending in place would otherwise write into the session and
    corrupt the next turn, in a way no test of that caller would reveal.
    """
    store = InMemorySessionStore()
    session = await store.create()
    await store.record(session, "q", "a")

    borrowed = await store.history(session)
    borrowed.clear()

    assert len(await store.history(session)) == 2


async def test_sessions_cannot_see_each_other() -> None:
    store = InMemorySessionStore()
    first, second = await store.create(), await store.create()

    await store.record(first, "vacation days?", "Twenty five.")
    await store.record(second, "expense limit?", "Twenty euros.")

    assert [m.content for m in await store.history(first)] == ["vacation days?", "Twenty five."]
    assert [m.content for m in await store.history(second)] == ["expense limit?", "Twenty euros."]


async def test_closing_a_session_destroys_its_memory() -> None:
    store = InMemorySessionStore()
    session = await store.create()
    await store.record(session, "q", "a")

    assert await store.destroy(session) is True
    with pytest.raises(UnknownSessionError):
        await store.history(session)


async def test_destroying_an_unknown_session_reports_that_there_was_nothing() -> None:
    """False rather than raising: the API's DELETE is idempotent by design."""
    assert await InMemorySessionStore().destroy("never-existed") is False


async def test_a_reopened_session_id_is_never_reissued() -> None:
    """A closed session's id does not come back and does not resurrect its history."""
    store = InMemorySessionStore()
    first = await store.create()
    await store.record(first, "remembered", "answer")
    await store.destroy(first)

    second = await store.create()
    assert second != first
    assert await store.history(second) == []


async def test_an_unknown_session_names_the_three_ordinary_causes() -> None:
    """The message is the whole error report for an operator problem."""
    with pytest.raises(UnknownSessionError) as raised:
        await InMemorySessionStore().history("bogus")
    message = str(raised.value)
    assert "closed" in message and "idled out" in message and "restarted" in message


async def test_history_is_trimmed_from_the_oldest_end() -> None:
    """`max_messages` bounds the prompt, and it must keep the *recent* turns.

    A follow-up refers to what was just said. Trimming the newest would bound
    memory just as effectively and destroy the feature it exists to support.
    """
    store = InMemorySessionStore(SessionSettings(max_messages=4))
    session = await store.create()
    for turn in range(5):
        await store.record(session, f"question {turn}", f"answer {turn}")

    history = await store.history(session)
    assert [m.content for m in history] == [
        "question 3",
        "answer 3",
        "question 4",
        "answer 4",
    ]


async def test_a_trimmed_session_still_reports_its_true_length() -> None:
    store = InMemorySessionStore(SessionSettings(max_messages=4))
    session = await store.create()
    for turn in range(5):
        await store.record(session, f"q{turn}", f"a{turn}")

    state = store.describe(session)
    assert state is not None
    assert state.turns == 5
    assert len(state.messages) == 4


async def test_the_least_recently_used_session_is_evicted_at_capacity() -> None:
    store = InMemorySessionStore(SessionSettings(max_sessions=2))
    first = await store.create()
    second = await store.create()
    await store.record(first, "keeps first recent", "ok")  # first is now most recent

    third = await store.create()

    with pytest.raises(UnknownSessionError):
        await store.history(second)
    assert await store.history(first) is not None
    assert await store.history(third) == []


async def test_an_idle_session_expires() -> None:
    store = InMemorySessionStore(SessionSettings(idle_ttl_seconds=0.05))
    session = await store.create()
    await store.record(session, "q", "a")

    await asyncio.sleep(0.08)

    with pytest.raises(UnknownSessionError):
        await store.history(session)


async def test_activity_postpones_expiry() -> None:
    """The TTL is measured from the last turn, not from creation.

    Otherwise a conversation longer than the TTL would die mid-sentence.
    """
    store = InMemorySessionStore(SessionSettings(idle_ttl_seconds=0.15))
    session = await store.create()
    for _ in range(3):
        await asyncio.sleep(0.06)
        await store.record(session, "still here", "yes")

    assert len(await store.history(session)) == 6


async def test_reading_history_postpones_expiry_so_a_turn_cannot_outlive_itself() -> None:
    """Regression: a turn is read, then generate, then write.

    If only the write advanced the clock, a session idle for almost the whole TTL
    would pass the read, spend ten seconds generating, and fail at `record()` —
    discarding a turn after the model call had already been paid for. Found by the
    end-to-end suite, where generation is real and takes seconds.

    Simulated here with sleeps rather than a model: the property is about the clock,
    not about the provider.
    """
    store = InMemorySessionStore(SessionSettings(idle_ttl_seconds=0.12))
    session = await store.create()
    await store.record(session, "first", "answer")

    await asyncio.sleep(0.09)          # nearly idled out
    await store.history(session)       # a turn begins: this must reset the clock
    await asyncio.sleep(0.09)          # a slow generation, longer than the remaining TTL

    await store.record(session, "second", "answer")  # must not raise
    assert len(await store.history(session)) == 4


async def test_live_session_count_tracks_creation_and_closure() -> None:
    store = InMemorySessionStore()
    assert store.live_sessions == 0
    first = await store.create()
    await store.create()
    assert store.live_sessions == 2
    await store.destroy(first)
    assert store.live_sessions == 1


# ----------------------------------------------------------- the conversation


async def test_a_first_turn_is_answered_with_no_history(
    conversation: tuple[Conversation, StubChatModel, InMemorySessionStore],
) -> None:
    """Single-turn behaviour is unchanged by the existence of sessions."""
    chat, model, _ = conversation
    session = await chat.start()

    answer = await chat.answer(session, "How many vacation days do employees get?")

    assert not answer.abstained
    assert answer.citations
    # The request carried exactly the question: no history, nothing prepended.
    assert [m.content for m in model.requests[-1].messages] == [
        "How many vacation days do employees get?"
    ]


async def test_a_follow_up_turn_carries_the_previous_exchange_into_generation(
    conversation: tuple[Conversation, StubChatModel, InMemorySessionStore],
) -> None:
    """The load-bearing assertion of this whole module.

    Checked against what the *model was sent*, not against what the store holds.
    A store that remembers correctly and a `Conversation` that forgets to pass the
    history are indistinguishable from the outside, and only one of them is a
    working chatbot.
    """
    chat, model, _ = conversation
    session = await chat.start()

    await chat.answer(session, "How many vacation days do employees get?")
    await chat.answer(session, "When do they expire?")

    sent = [(m.role, m.content) for m in model.requests[-1].messages]
    assert sent == [
        (Role.USER, "How many vacation days do employees get?"),
        (Role.ASSISTANT, "The answer is documented. [1]"),
        (Role.USER, "When do they expire?"),
    ]


async def test_two_sessions_answered_in_parallel_do_not_mix_context(
    conversation: tuple[Conversation, StubChatModel, InMemorySessionStore],
) -> None:
    """Context isolation under concurrency, which is how a service is actually used."""
    chat, model, _ = conversation
    first, second = await chat.start(), await chat.start()

    await asyncio.gather(
        chat.answer(first, "vacation days"),
        chat.answer(second, "expense receipts"),
    )
    await asyncio.gather(
        chat.answer(first, "follow up one"),
        chat.answer(second, "follow up two"),
    )

    by_final_question = {
        request.messages[-1].content: [m.content for m in request.messages]
        for request in model.requests
    }
    assert "vacation days" in by_final_question["follow up one"]
    assert "expense receipts" not in by_final_question["follow up one"]
    assert "expense receipts" in by_final_question["follow up two"]
    assert "vacation days" not in by_final_question["follow up two"]


async def test_a_closed_session_refuses_further_turns(
    conversation: tuple[Conversation, StubChatModel, InMemorySessionStore],
) -> None:
    chat, _, _ = conversation
    session = await chat.start()
    await chat.answer(session, "How many vacation days do employees get?")

    assert await chat.close(session) is True

    with pytest.raises(UnknownSessionError):
        await chat.answer(session, "and when do they expire?")


async def test_a_new_session_after_a_close_starts_with_clean_context(
    conversation: tuple[Conversation, StubChatModel, InMemorySessionStore],
) -> None:
    """The full cleanup cycle: close destroys, and the replacement inherits nothing."""
    chat, model, _ = conversation

    first = await chat.start()
    await chat.answer(first, "How many vacation days do employees get?")
    await chat.close(first)

    second = await chat.start()
    await chat.answer(second, "How are expenses reimbursed?")

    assert [m.content for m in model.requests[-1].messages] == ["How are expenses reimbursed?"]


async def test_an_abstention_is_still_recorded_as_a_turn(
    store: MemoryVectorStore, embeddings: StubEmbeddingModel, documents: list[Document]
) -> None:
    """Otherwise a follow-up like "why not?" resolves against nothing.

    The abstention *message* is what goes into the history, because that is what
    the user saw and what their next question refers to.

    Driven through the uncited-answer path rather than the no-hits path: the stub
    embedder is bag-of-words, so even nonsense retrieves something and the only
    abstention reachable here is the citation policy. That is the more interesting
    of the two anyway — it is the one where the model did produce text.
    """
    await IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
        embeddings=embeddings,
        store=store,
    ).ingest(InMemoryLoader(documents).load())

    sessions = InMemorySessionStore()
    chat = Conversation(
        answerer=Answerer(
            retrieval=RetrievalPipeline(
                store=store,
                embeddings=embeddings,
                reranker=NoopReranker(),
                settings=RetrievalSettings(rewrite_queries=False, top_k=4),
            ),
            model=StubChatModel("I could not find that."),  # no [n] marker
            settings=GenerationSettings(require_citations=True),
        ),
        store=sessions,
    )
    session = await chat.start()

    answer = await chat.answer(session, "What is the policy on quantum kumquats?")

    assert answer.abstained
    history = await sessions.history(session)
    assert len(history) == 2
    assert history[1].content == answer.text


async def test_a_streamed_turn_is_recorded_once_the_answer_completes(
    conversation: tuple[Conversation, StubChatModel, InMemorySessionStore],
) -> None:
    chat, _, sessions = conversation
    session = await chat.start()

    events = [event async for event in chat.stream(session, "How many vacation days?")]
    complete = [event for event in events if isinstance(event, AnswerComplete)]

    assert len(complete) == 1
    assert isinstance(events[0], RetrievalReady)
    assert any(isinstance(event, TextDelta) for event in events)

    history = await sessions.history(session)
    assert history[0].content == "How many vacation days?"
    # The authoritative answer, not the concatenated deltas.
    assert history[1].content == complete[0].answer.text


async def test_a_streamed_follow_up_sees_the_previous_streamed_turn(
    conversation: tuple[Conversation, StubChatModel, InMemorySessionStore],
) -> None:
    """Memory must work identically in both modes, as the abstention policy does."""
    chat, model, _ = conversation
    session = await chat.start()

    async for _ in chat.stream(session, "How many vacation days?"):
        pass
    async for _ in chat.stream(session, "When do they expire?"):
        pass

    # Asserted on roles and on the questions, not on the assistant text: the stub
    # emits one delta per word, so the reassembled answer differs from the buffered
    # one by whitespace alone. Pinning that would test the stub's spacing.
    sent = model.requests[-1].messages
    assert [m.role for m in sent] == [Role.USER, Role.ASSISTANT, Role.USER]
    assert sent[0].content == "How many vacation days?"
    assert sent[1].content.strip() == "The answer is documented. [1]"
    assert sent[2].content == "When do they expire?"


async def test_a_stream_that_fails_partway_records_no_turn(
    store: MemoryVectorStore, embeddings: StubEmbeddingModel, documents: list[Document]
) -> None:
    """A failed turn is not a turn.

    Recording the deltas seen before the failure would put a half-sentence into the
    history and let the next question resolve against an answer that was never
    given.
    """
    await IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
        embeddings=embeddings,
        store=store,
    ).ingest(InMemoryLoader(documents).load())

    sessions = InMemorySessionStore()
    chat = Conversation(
        answerer=Answerer(
            retrieval=RetrievalPipeline(
                store=store,
                embeddings=embeddings,
                reranker=NoopReranker(),
                settings=RetrievalSettings(rewrite_queries=False, top_k=4),
            ),
            model=FailingChatModel(),  # type: ignore[arg-type]
            settings=GenerationSettings(),
        ),
        store=sessions,
    )
    session = await chat.start()

    with pytest.raises(RuntimeError):
        async for _ in chat.stream(session, "How many vacation days?"):
            pass

    assert await sessions.history(session) == []


async def test_the_session_context_span_distinguishes_a_follow_up_from_a_first_turn(
    conversation: tuple[Conversation, StubChatModel, InMemorySessionStore],
) -> None:
    """Diagnosability: "answered as if it were a first question" must be visible.

    That failure and "answered badly" produce identical output and need completely
    different fixes, so the trace has to separate them.
    """
    configure_observability(enabled=True, capacity=64, persist=False, log_traces=False)
    chat, _, _ = conversation
    session = await chat.start()

    await chat.answer(session, "How many vacation days do employees get?")
    await chat.answer(session, "When do they expire?")

    # Filtered by session id, not just by span name: `RECORDER` is a module-global
    # ring buffer that other tests in this run have already written to, and the
    # fixture's own ingestion contributes traces before the test body starts.
    contexts = [
        span
        for recorded in RECORDER.recent(limit=64)
        for span in recorded.spans
        if span.name == "session_context" and span.attributes.get("session_id") == session
    ]
    assert len(contexts) == 2
    # Most recent trace first, so the follow-up is the one carrying context.
    assert contexts[0].attributes["is_follow_up"] is True
    assert contexts[0].attributes["turns_in_context"] == 1
    assert contexts[1].attributes["is_follow_up"] is False
    assert contexts[1].attributes["turns_in_context"] == 0
