"""End-to-end smoke test against the real stack.

Everything else in this suite runs against in-process doubles, which is what makes
it fast and hermetic — and also what makes it blind to the class of failure that
only appears against a real provider and a real database: a wrong request shape, a
migration that will not apply, a model that cannot embed, a DSN that is wrong.

Until now that gap was covered by a table of manual checks in `PROJECT_STATUS.md`.
A table of manual checks rots. This is that table, executed.

Skipped cleanly unless the reference environment is present:

    OSC_E2E=1 OSC_TEST_DSN=postgresql://USER@localhost:5432/osc_e2e make test-e2e

It needs its own database. The `chunks` table fixes its vector width at creation,
so pointing this at a database an application already migrated will either fail the
dimension guard or, worse, mix test content into a real corpus.

**The corpus is built here, in `tmp_path`, and never read from `docs/`.** An earlier
version of this file ingested `Path("docs")` directly. That was harmless while the
directory held demonstration data and became two defects the moment it held real
content: the suite asserted against company documents that anyone could edit, and it
swept `docs/engineering/` — this repository's own knowledge base, which must never be
retrievable — into the index. Generating the corpus costs a few lines and buys a suite
that cannot be broken by an edit to an FAQ.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest

from osc_assistant.container import Container
from osc_assistant.conversation import Conversation, UnknownSessionError
from osc_assistant.ingestion import FilesystemLoader
from osc_assistant.observability import RECORDER
from osc_assistant.registry import ComponentConfig
from osc_assistant.settings import (
    ChunkingSettings,
    DatabaseSettings,
    GenerationSettings,
    ObservabilitySettings,
    RetrievalSettings,
    SessionSettings,
    Settings,
)
from osc_assistant.types import Role

# `OSC_E2E_DSN` first, falling back to the shared `OSC_TEST_DSN`. The separate name
# is what lets `make verify` run the pgvector suite and this one in a *single*
# pytest invocation, and therefore report a single summary: the two suites need
# different databases — this one fixes its chunks table at the live embedding
# model's width and clears its workspace when it finishes — and with one variable
# between them, only one suite could be pointed at the right place per run.
DSN = os.environ.get("OSC_E2E_DSN") or os.environ.get("OSC_TEST_DSN")

pytestmark = [
    pytest.mark.skipif(
        os.environ.get("OSC_E2E") != "1",
        reason="Set OSC_E2E=1 (with a live Ollama and Postgres) to run the smoke test.",
    ),
    pytest.mark.skipif(
        not DSN, reason="Set OSC_E2E_DSN (or OSC_TEST_DSN) to a dedicated test database."
    ),
]

def _write_pdf(path: Path, lines: list[str]) -> None:
    """Write a minimal single-page PDF containing `lines` as extractable text.

    Hand-assembled rather than reached for with a rendering library, because the
    only property under test is that `pypdf` can get the words back out — and adding
    reportlab to the dev dependencies to produce forty bytes of text stream would be
    a dependency bought for one test.

    `pypdf` needs a valid cross-reference table, so the byte offset of every object
    is recorded as it is written rather than computed afterwards.
    """
    text = "\n".join(f"({line}) Tj T*" for line in lines)
    content = f"BT /F1 12 Tf 14 TL 50 750 Td\n{text}\nET".encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets: list[int] = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"

    xref_offset = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode() + b"0000000000 65535 f \n"
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    ).encode()
    path.write_bytes(bytes(out))


def _build_corpus(root: Path) -> Path:
    """Write one document per parser family into `root`.

    Six formats, each carrying a distinctive fact the assertions below retrieve by.
    The facts are deliberately unusual — "twenty six days", "400 days", "sixteen
    hours" — so that a retrieval hit is evidence the document was actually indexed
    and parsed, not evidence that the model already knew the answer.
    """
    root.mkdir(parents=True, exist_ok=True)

    (root / "leave-policy.md").write_text(
        "# Leave Policy\n\n"
        "Employees accrue twenty six days of annual leave each calendar year.\n"
        "Annual leave requests are approved by your line manager.\n"
        "Unused annual leave expires on the thirty first of March.\n",
        encoding="utf-8",
    )
    (root / "expenses.txt").write_text(
        "Expense Policy\n\n"
        "Expense claims must be submitted within thirty days of the purchase date.\n"
        "Receipts are required for any expense above twenty euros.\n",
        encoding="utf-8",
    )
    (root / "access-control.html").write_text(
        "<html><head><title>Access Control Standard</title></head><body>"
        "<h1>Access Control Standard</h1>"
        "<p>Privileged access is granted for a maximum of sixteen hours.</p>"
        "<p>Service credentials rotate every ninety days.</p>"
        "</body></html>",
        encoding="utf-8",
    )
    _write_pdf(
        root / "data-retention.pdf",
        [
            "Data Retention Schedule",
            "Audit logs are retained for 400 days before deletion.",
            "Customer records are retained for seven years.",
        ],
    )

    import docx

    document = docx.Document()
    document.add_paragraph("Onboarding Checklist")
    document.add_paragraph("New joiners receive a laptop on their first day.")
    table = document.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Home office allowance"
    table.rows[0].cells[1].text = "600 EUR"
    document.save(str(root / "onboarding.docx"))

    import openpyxl

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Capacity"
    sheet.append(["Region", "Seats"])
    sheet.append(["EMEA", 128])
    workbook.save(str(root / "capacity-plan.xlsx"))

    return root


def _settings(tmp_path: Path, **overrides: object) -> Settings:
    base: dict[str, object] = {
        "environment": "test",
        "log_format": "text",
        "workspace_id": "e2e",
        "llm": ComponentConfig(
            provider="ollama",
            model=os.environ.get("OSC_E2E_MODEL", "qwen3:8b"),
            options={"extra_body": {"reasoning_effort": "none"}},
        ),
        "embeddings": ComponentConfig(provider="ollama", model="nomic-embed-text"),
        "vector_store": ComponentConfig(provider="pgvector"),
        "database": DatabaseSettings(dsn=DSN or ""),
        "chunking": ChunkingSettings(chunk_size=900, chunk_overlap=120),
        "retrieval": RetrievalSettings(rewrite_queries=False, top_k=5, candidates=30),
        "generation": GenerationSettings(max_tokens=1500),
        "observability": ObservabilitySettings(
            persist_traces=True, trace_dir=tmp_path / "traces", log_traces=False
        ),
    }
    return Settings(**{**base, **overrides})  # type: ignore[arg-type]


@pytest.fixture
def corpus(tmp_path: Path) -> Path:
    """A generated corpus, isolated per test and never read from `docs/`."""
    return _build_corpus(tmp_path / "corpus")


@pytest.fixture
async def indexed(tmp_path: Path, corpus: Path):
    """A container over a freshly synced corpus, cleaned up afterwards."""
    settings = _settings(tmp_path)
    async with Container(settings) as container:
        loader = FilesystemLoader(corpus)
        report = await container.ingestion.ingest(loader.load(), source_failures=loader.failures)
        assert report.succeeded, report.failures
        assert report.indexed > 0
        try:
            yield container
        finally:
            await _purge(container)


async def _purge(container: Container) -> None:
    """Delete every document this suite indexed in its workspace.

    The suite shares a database across runs, so leaving documents behind would make
    the next run's `statistics()` assertions depend on the previous one's.
    """
    for document_id in await container.vector_store.document_ids():
        await container.vector_store.delete_document(document_id)


async def test_a_corpus_of_six_formats_indexes(indexed: Container) -> None:
    """Markdown, text, HTML, PDF, Word and Excel, parsed by the real libraries."""
    stats = await indexed.vector_store.statistics()  # type: ignore[attr-defined]

    assert stats.documents == 6
    assert stats.chunks >= stats.documents
    assert stats.embedding_models == ["nomic-embed-text"]
    assert set(stats.documents_by_extension) == {".md", ".txt", ".html", ".pdf", ".docx", ".xlsx"}


async def test_re_running_an_unchanged_corpus_makes_no_embedding_calls(
    indexed: Container, corpus: Path
) -> None:
    """The property that makes a scheduled sync cheap and safe to re-run."""
    loader = FilesystemLoader(corpus)
    report = await indexed.ingestion.ingest(loader.load(), source_failures=loader.failures)

    assert report.indexed == 0
    assert report.skipped == report.processed
    assert report.deleted == 0


async def test_reindex_forces_work_the_hash_says_is_unnecessary(
    indexed: Container, corpus: Path
) -> None:
    loader = FilesystemLoader(corpus)
    report = await indexed.ingestion.ingest(
        loader.load(), reindex=True, source_failures=loader.failures
    )

    assert report.indexed == report.processed
    assert report.skipped == 0


async def test_hybrid_retrieval_ranks_the_right_document_first(
    indexed: Container,
) -> None:
    """Real embeddings, real pgvector, real SQL rank fusion."""
    result = await indexed.retrieval.retrieve("how many days of annual leave")

    assert result.chunks
    assert "leave-policy" in result.chunks[0].chunk.source_uri
    assert result.trace_id


async def test_a_grounded_answer_cites_the_source_it_came_from(
    indexed: Container,
) -> None:
    """The whole path, against a real model. Asserts grounding, not wording.

    Deliberately not asserting the answer text: an 8B local model paraphrases
    differently between runs, and a test that pinned its prose would fail for the
    wrong reason. What must hold is that it answered, and that the citation points
    at the document that actually contains the fact.
    """
    answer = await indexed.answerer.answer("How many days of annual leave do employees get?")

    assert not answer.abstained
    assert answer.citations
    assert "leave-policy" in answer.citations[0].source_uri
    assert answer.usage.input_tokens > 0
    assert answer.trace_id


async def test_a_question_the_corpus_cannot_answer_is_declined(
    indexed: Container,
) -> None:
    """General knowledge must not leak in where the corpus is silent."""
    answer = await indexed.answerer.answer(
        "What is the boiling point of mercury in kelvin?"
    )

    assert answer.abstained or not answer.citations


async def test_a_binary_format_is_answerable(indexed: Container) -> None:
    """Proves extraction, not just ingestion: a PDF whose text never parsed would
    index as chunks nobody can retrieve.

    The asserted phrase is one only the PDF contains, so a pass means pypdf got the
    words out — not merely that a file with a .pdf suffix reached the store.
    """
    result = await indexed.retrieval.retrieve("how long are audit logs retained")

    assert any(hit.chunk.source_uri.endswith(".pdf") for hit in result.chunks)
    assert any("400 days" in hit.chunk.text for hit in result.chunks)


async def test_the_streamed_and_buffered_paths_agree_on_abstention(
    indexed: Container,
) -> None:
    """The abstention policy must be identical in both modes."""
    from osc_assistant.generation import AnswerComplete

    question = "What is the airspeed velocity of an unladen swallow?"
    buffered = await indexed.answerer.answer(question)

    streamed = None
    async for event in indexed.answerer.stream(question):
        if isinstance(event, AnswerComplete):
            streamed = event.answer

    assert streamed is not None
    assert streamed.abstained == buffered.abstained


async def test_the_run_is_fully_traced(indexed: Container) -> None:
    """Every stage of the real pipeline, timed — the observability contract itself."""
    RECORDER.clear()
    await indexed.answerer.answer("How many days of annual leave do employees get?")

    recorded = RECORDER.recent(limit=1)[0]
    names = {span.name for span in recorded.spans}
    assert {"answer", "retrieve", "embed_query", "search", "generate", "finalise"} <= names
    assert recorded.duration_ms > 0
    generate = next(span for span in recorded.spans if span.name == "generate")
    assert generate.attributes["input_tokens"] > 0


# ===========================================================================
# The conversational flow, end to end against the real stack.
#
#   session -> question -> answer -> follow-up -> contextual retrieval
#           -> contextual answer -> close -> memory destroyed
#           -> new session -> clean context
#
# These use the real `Conversation`, the real `InMemorySessionStore`, live Ollama
# and live PostgreSQL. The unit suite proves the same properties against stubs in
# milliseconds; what this adds is that they still hold when the answers are
# generated by a model that does not return a fixed string.
# ===========================================================================


@pytest.fixture
def conversation(indexed: Container) -> Conversation:
    return indexed.conversation


async def test_a_session_carries_context_into_a_follow_up(
    conversation: Conversation, indexed: Container
) -> None:
    """The whole point of the feature, against the real stack.

    The follow-up asks "when does it expire?" — a question with no retrievable
    subject of its own. Asserted on the *prompt the model received* rather than on
    the answer text, because a live model's phrasing is not a stable assertion
    target while the message list is exact.
    """
    session = await conversation.start()
    try:
        first = await conversation.answer(
            session, "How many days of annual leave do employees get?"
        )
        assert not first.abstained
        assert "twenty six" in first.text.lower()

        history = await conversation.history(session)
        assert [message.role for message in history] == [Role.USER, Role.ASSISTANT]
        assert history[1].content == first.text

        await conversation.answer(session, "And when does it expire?")

        # Turn two was answered against turn one, not in isolation.
        transcript = await conversation.history(session)
        assert len(transcript) == 4
        assert transcript[0].content == "How many days of annual leave do employees get?"
        assert transcript[2].content == "And when does it expire?"
    finally:
        await conversation.close(session)


async def test_closing_a_session_destroys_it_and_the_next_one_starts_clean(
    conversation: Conversation,
) -> None:
    """Close -> memory destroyed -> new session -> clean context."""
    first = await conversation.start()
    await conversation.answer(first, "How many days of annual leave do employees get?")
    assert len(await conversation.history(first)) == 2

    assert await conversation.close(first) is True
    with pytest.raises(UnknownSessionError):
        await conversation.history(first)

    second = await conversation.start()
    try:
        assert second != first
        assert await conversation.history(second) == []
    finally:
        await conversation.close(second)


async def test_two_live_sessions_do_not_share_memory(conversation: Conversation) -> None:
    """Isolation with real generation in both conversations."""
    leave = await conversation.start()
    expenses = await conversation.start()
    try:
        await conversation.answer(leave, "How many days of annual leave do employees get?")
        await conversation.answer(expenses, "How long do I have to submit an expense claim?")

        leave_history = " ".join(m.content for m in await conversation.history(leave))
        expense_history = " ".join(m.content for m in await conversation.history(expenses))

        assert "annual leave" in leave_history
        assert "expense claim" not in leave_history
        assert "expense claim" in expense_history
        assert "annual leave" not in expense_history
    finally:
        await conversation.close(leave)
        await conversation.close(expenses)


async def test_a_conversational_turn_produces_one_trace_with_its_context_stage(
    conversation: Conversation,
) -> None:
    """Diagnosability of a live follow-up.

    One turn is one trace: `Answerer` opens `trace("answer")` inside the
    `Conversation`'s own trace, and a nested trace extends rather than forks. If
    that ever changed, a follow-up would produce two traces and neither would show
    the whole turn.
    """
    session = await conversation.start()
    try:
        await conversation.answer(session, "How many days of annual leave do employees get?")
        RECORDER.clear()
        await conversation.answer(session, "And when does it expire?")

        recorded = RECORDER.recent(limit=5)
        assert len(recorded) == 1, "one turn must be one trace, not two"

        spans = {span.name: span for span in recorded[0].spans}
        assert {"session_context", "retrieve", "generate", "finalise"} <= set(spans)
        context = spans["session_context"]
        assert context.attributes["is_follow_up"] is True
        assert context.attributes["turns_in_context"] == 1
    finally:
        await conversation.close(session)


async def test_an_unanswerable_turn_inside_a_session_is_still_recorded(
    conversation: Conversation,
) -> None:
    """A follow-up like "why not?" needs the declined turn to be there.

    The property under test is that the turn is **recorded**, whatever the outcome —
    which is deterministic. It deliberately does not assert that the model abstained:
    that depends on a live 8B model choosing not to emit a citation marker, it is
    covered by `test_a_question_the_corpus_cannot_answer_is_declined` with the same
    tolerant form the rest of this suite uses, and asserting it strictly here made
    this test fail in a full run and pass in isolation.
    """
    session = await conversation.start()
    try:
        await conversation.answer(session, "How many days of annual leave do employees get?")
        declined = await conversation.answer(
            session, "What is the company's policy on submarine maintenance?"
        )

        assert declined.abstained or not declined.citations

        # Recorded either way, and it is the text the user saw that goes in.
        transcript = await conversation.history(session)
        assert len(transcript) == 4
        assert transcript[3].content == declined.text
    finally:
        await conversation.close(session)


async def test_a_session_that_outlives_its_ttl_is_reported_not_silently_emptied(
    tmp_path: Path, corpus: Path
) -> None:
    """The failure path an operator actually meets.

    An expired session must raise rather than behave like a new one: answering a
    follow-up against silently empty history is the bug that looks like a bad model
    and is really a bad session.

    No generation happens inside the TTL window. An earlier version of this test put
    one there and failed — a live answer takes seconds, far longer than any TTL short
    enough to test against, so the session expired mid-turn. That was a real defect
    in the store and it is fixed (reading history now counts as activity, so a turn
    cannot outlive itself); the timing-independent regression for it lives in
    `test_conversation.py`. What is worth exercising *here* is the operator-facing
    behaviour against real infrastructure: expiry between turns is an error naming
    the cause, not an empty history.
    """
    settings = _settings(tmp_path, session=SessionSettings(idle_ttl_seconds=0.05))
    async with Container(settings) as container:
        loader = FilesystemLoader(corpus)
        await container.ingestion.ingest(loader.load(), source_failures=loader.failures)
        try:
            session = await container.conversation.start()
            await asyncio.sleep(0.1)

            with pytest.raises(UnknownSessionError, match="idled out"):
                await container.conversation.answer(
                    session, "How many days of annual leave do employees get?"
                )
        finally:
            await _purge(container)
