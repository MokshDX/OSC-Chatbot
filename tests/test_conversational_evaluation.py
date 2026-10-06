"""Multi-turn evaluation tests.

The conversational harness has one property that matters more than the rest: the
control run. Without it `follow_up_resolution` can look healthy on a system with no
memory at all, because a follow-up may retrieve the right document by keyword luck.
These tests pin that the control actually runs, that the lift is computed from the
pair, and that the lift is honest in both directions.

Everything runs against the in-process doubles in `conftest`. The production corpus
is never touched.
"""

from __future__ import annotations

import pytest

from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
from osc_assistant.conversation import Conversation, InMemorySessionStore
from osc_assistant.errors import EvaluationError
from osc_assistant.evaluation import (
    ConversationalEvaluator,
    ConversationalSet,
    TurnResult,
    load_conversational_set,
    summarise_conversation,
)
from osc_assistant.generation import Answerer
from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader
from osc_assistant.providers.reranking.noop import NoopReranker
from osc_assistant.providers.vectorstores.memory import MemoryVectorStore
from osc_assistant.retrieval import RetrievalPipeline
from osc_assistant.settings import (
    GenerationSettings,
    RetrievalSettings,
    SessionSettings,
    Settings,
)
from osc_assistant.types import Document

from .conftest import EMBEDDING_DIMENSIONS, FailingChatModel, StubChatModel, StubEmbeddingModel

pytestmark = pytest.mark.anyio


@pytest.fixture
def corpus() -> list[Document]:
    return [
        Document(
            id="doc-leave",
            source_uri="file:///corpus/hr/leave.md",
            title="Leave Policy",
            text="Employees accrue twenty five leave days each calendar year.",
            metadata={"relative_path": "hr/leave.md"},
        ),
        Document(
            id="doc-expenses",
            source_uri="file:///corpus/hr/expenses.md",
            title="Expense Policy",
            text="Expense claims must be submitted within thirty days of purchase.",
            metadata={"relative_path": "hr/expenses.md"},
        ),
    ]


def _settings() -> Settings:
    return Settings(
        retrieval=RetrievalSettings(rewrite_queries=False, top_k=3, candidates=10),
        session=SessionSettings(),
    )


@pytest.fixture
async def evaluator(
    corpus: list[Document], embeddings: StubEmbeddingModel
) -> ConversationalEvaluator:
    store = MemoryVectorStore(dimensions=EMBEDDING_DIMENSIONS)
    await IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
        embeddings=embeddings,
        store=store,
    ).ingest(InMemoryLoader(corpus).load())

    retrieval = RetrievalPipeline(
        store=store,
        embeddings=embeddings,
        reranker=NoopReranker(),
        settings=RetrievalSettings(rewrite_queries=False, top_k=3, candidates=10),
    )
    conversation = Conversation(
        answerer=Answerer(
            retrieval=retrieval,
            model=StubChatModel(),  # type: ignore[arg-type]
            settings=GenerationSettings(),
        ),
        store=InMemorySessionStore(),
    )
    return ConversationalEvaluator(conversation, retrieval, _settings())


def _set(*turns: dict[str, object], case_id: str = "case") -> ConversationalSet:
    return ConversationalSet.model_validate(
        {"cases": [{"id": case_id, "turns": list(turns), "tags": ["t"]}]}
    )


# ------------------------------------------------------------------- the dataset


def test_a_case_needs_at_least_two_turns() -> None:
    """A one-turn "conversation" belongs in the single-turn suite."""
    with pytest.raises(Exception, match=r"at least 2|too_short"):
        ConversationalSet.model_validate(
            {"cases": [{"id": "c", "turns": [{"question": "q", "relevant_documents": ["a.md"]}]}]}
        )


def test_an_opening_turn_may_not_require_context() -> None:
    """There is no prior turn for it to resolve against."""
    with pytest.raises(Exception, match="requires_context"):
        ConversationalSet.model_validate(
            {
                "cases": [
                    {
                        "id": "c",
                        "turns": [
                            {
                                "question": "what about it?",
                                "relevant_documents": ["a.md"],
                                "requires_context": True,
                            },
                            {"question": "b", "relevant_documents": ["a.md"]},
                        ],
                    }
                ]
            }
        )


def test_a_turn_cannot_both_depend_on_and_be_independent_of_the_conversation() -> None:
    """`requires_context` and `context_switch` disagree about what good looks like.

    One says the turn should score better with history, the other that it should
    score the same. A turn in both aggregates would be judged by two standards.
    """
    with pytest.raises(Exception, match="context_switch"):
        ConversationalSet.model_validate(
            {
                "cases": [
                    {
                        "id": "c",
                        "turns": [
                            {"question": "a", "relevant_documents": ["a.md"]},
                            {
                                "question": "b",
                                "relevant_documents": ["a.md"],
                                "requires_context": True,
                                "context_switch": True,
                            },
                        ],
                    }
                ]
            }
        )


def test_an_unscoreable_turn_is_rejected_rather_than_scored_zero() -> None:
    with pytest.raises(Exception, match="relevant_documents"):
        ConversationalSet.model_validate(
            {
                "cases": [
                    {
                        "id": "c",
                        "turns": [
                            {"question": "a", "relevant_documents": ["a.md"]},
                            {"question": "b"},
                        ],
                    }
                ]
            }
        )


def test_duplicate_case_ids_are_rejected() -> None:
    with pytest.raises(Exception, match="duplicate"):
        ConversationalSet.model_validate(
            {
                "cases": [
                    {"id": "c", "turns": [{"question": "a", "relevant_documents": ["a.md"]}] * 2},
                    {"id": "c", "turns": [{"question": "b", "relevant_documents": ["a.md"]}] * 2},
                ]
            }
        )


def test_a_missing_conversational_set_names_the_file(tmp_path) -> None:
    with pytest.raises(EvaluationError, match=r"missing\.yaml"):
        load_conversational_set(tmp_path / "missing.yaml")


def test_the_shipped_conversational_suite_is_valid() -> None:
    """The suite the canonical command runs must load.

    A validation error here is a broken `make eval`, and it is cheap to catch at
    test time rather than forty minutes into an evaluation run.
    """
    from pathlib import Path

    suite = load_conversational_set(Path("evaluation/suites/conversational.yaml"))
    assert suite.corpus == "docs/company/schema"
    assert suite.turn_count > len(suite.cases)


# -------------------------------------------------------------------- the runner


async def test_every_turn_of_a_case_is_scored(evaluator: ConversationalEvaluator) -> None:
    report = await evaluator.run(
        _set(
            {"question": "how many leave days", "relevant_documents": ["hr/leave.md"]},
            {"question": "when are they lost", "relevant_documents": ["hr/leave.md"]},
        )
    )

    assert report.case_count == 1
    assert report.turn_count == 2
    assert [turn.ordinal for turn in report.turns] == [1, 2]
    assert report.failed_turns == 0


async def test_a_turn_records_the_context_it_was_answered_against(
    evaluator: ConversationalEvaluator,
) -> None:
    """Turn n sees exactly 2*(n-1) messages, which is what `session_isolation` checks."""
    report = await evaluator.run(
        _set(
            {"question": "how many leave days", "relevant_documents": ["hr/leave.md"]},
            {"question": "and expenses", "relevant_documents": ["hr/expenses.md"]},
            {"question": "and again", "relevant_documents": ["hr/leave.md"]},
        )
    )

    assert [turn.context_messages for turn in report.turns] == [0, 2, 4]
    assert report.summary["session_isolation"] == 1.0


async def test_a_control_run_happens_only_for_the_turns_that_need_one(
    evaluator: ConversationalEvaluator,
) -> None:
    """Control runs cost a retrieval each; ordinary turns must not pay for one."""
    report = await evaluator.run(
        _set(
            {"question": "how many leave days", "relevant_documents": ["hr/leave.md"]},
            {"question": "plain follow up", "relevant_documents": ["hr/leave.md"]},
            {
                "question": "when are they lost",
                "relevant_documents": ["hr/leave.md"],
                "requires_context": True,
            },
        )
    )

    assert report.turns[0].control_hit is None
    assert report.turns[1].control_hit is None
    assert report.turns[2].control_hit is not None
    assert report.turns[2].control_trace_id


async def test_follow_up_lift_is_the_difference_between_the_pair() -> None:
    """The lift must come from the two measurements, not from the in-session one.

    Constructed directly so the pair can be set independently — a live run cannot
    produce "resolved in session, missed cold" on demand.
    """
    turns = [
        TurnResult(
            case_id="c",
            ordinal=2,
            question="q",
            requires_context=True,
            relevant_documents=["a.md"],
            hit=True,
            control_hit=False,
        ),
        TurnResult(
            case_id="c",
            ordinal=3,
            question="q2",
            requires_context=True,
            relevant_documents=["a.md"],
            hit=True,
            control_hit=True,
        ),
    ]
    summary = summarise_conversation(turns, top_k=5, wall_seconds=1.0, max_messages=20)

    assert summary["follow_up_resolution"] == 1.0
    assert summary["follow_up_resolution_no_context"] == 0.5
    assert summary["follow_up_lift"] == 0.5


async def test_a_negative_lift_is_reported_rather_than_clamped() -> None:
    """The conversation making retrieval *worse* is a real outcome.

    Clamping it to zero would hide the single most important thing a conversational
    harness can discover.
    """
    turns = [
        TurnResult(
            case_id="c",
            ordinal=2,
            question="q",
            requires_context=True,
            relevant_documents=["a.md"],
            hit=False,
            control_hit=True,
        )
    ]
    summary = summarise_conversation(turns, top_k=5, wall_seconds=1.0, max_messages=20)

    assert summary["follow_up_lift"] == -1.0


async def test_context_pollution_measures_falling_below_the_cold_control() -> None:
    """For a context switch the control is the benchmark to match, not to beat."""
    polluted = summarise_conversation(
        [
            TurnResult(
                case_id="c",
                ordinal=2,
                question="q",
                context_switch=True,
                relevant_documents=["a.md"],
                hit=False,
                control_hit=True,
            )
        ],
        top_k=5,
        wall_seconds=1.0,
        max_messages=20,
    )
    clean = summarise_conversation(
        [
            TurnResult(
                case_id="c",
                ordinal=2,
                question="q",
                context_switch=True,
                relevant_documents=["a.md"],
                hit=True,
                control_hit=True,
            )
        ],
        top_k=5,
        wall_seconds=1.0,
        max_messages=20,
    )

    assert polluted["context_pollution"] == 1.0
    assert clean["context_pollution"] == 0.0


async def test_beating_the_control_on_a_switch_is_not_negative_pollution() -> None:
    """Pollution is floored at zero: doing better than cold is not "negative harm"."""
    summary = summarise_conversation(
        [
            TurnResult(
                case_id="c",
                ordinal=2,
                question="q",
                context_switch=True,
                relevant_documents=["a.md"],
                hit=True,
                control_hit=False,
            )
        ],
        top_k=5,
        wall_seconds=1.0,
        max_messages=20,
    )
    assert summary["context_pollution"] == 0.0


async def test_a_failing_provider_costs_one_turn_not_the_whole_run(
    corpus: list[Document], embeddings: StubEmbeddingModel
) -> None:
    """A harness that is itself fragile does not get run."""
    store = MemoryVectorStore(dimensions=EMBEDDING_DIMENSIONS)
    await IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
        embeddings=embeddings,
        store=store,
    ).ingest(InMemoryLoader(corpus).load())

    retrieval = RetrievalPipeline(
        store=store,
        embeddings=embeddings,
        reranker=NoopReranker(),
        settings=RetrievalSettings(rewrite_queries=False, top_k=3),
    )
    evaluator = ConversationalEvaluator(
        Conversation(
            answerer=Answerer(
                retrieval=retrieval,
                model=FailingChatModel(),  # type: ignore[arg-type]
                settings=GenerationSettings(),
            ),
            store=InMemorySessionStore(),
        ),
        retrieval,
        _settings(),
    )

    report = await evaluator.run(
        _set(
            {"question": "how many leave days", "relevant_documents": ["hr/leave.md"]},
            {"question": "and expenses", "relevant_documents": ["hr/expenses.md"]},
        )
    )

    assert report.failed_turns == 2
    assert all("provider unavailable" in (turn.error or "") for turn in report.turns)
    # Still a report, not a traceback.
    assert report.summary["turns_scored"] == 0.0


async def test_a_failed_turn_still_releases_its_session(
    corpus: list[Document], embeddings: StubEmbeddingModel
) -> None:
    """A harness leaking a session per failed case becomes an OOM report."""
    store = MemoryVectorStore(dimensions=EMBEDDING_DIMENSIONS)
    await IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
        embeddings=embeddings,
        store=store,
    ).ingest(InMemoryLoader(corpus).load())

    retrieval = RetrievalPipeline(
        store=store,
        embeddings=embeddings,
        reranker=NoopReranker(),
        settings=RetrievalSettings(rewrite_queries=False, top_k=3),
    )
    sessions = InMemorySessionStore()
    evaluator = ConversationalEvaluator(
        Conversation(
            answerer=Answerer(
                retrieval=retrieval,
                model=FailingChatModel(),  # type: ignore[arg-type]
                settings=GenerationSettings(),
            ),
            store=sessions,
        ),
        retrieval,
        _settings(),
    )

    await evaluator.run(
        _set(
            {"question": "a", "relevant_documents": ["hr/leave.md"]},
            {"question": "b", "relevant_documents": ["hr/leave.md"]},
        )
    )

    assert sessions.live_sessions == 0


async def test_failed_turns_are_excluded_from_quality_means() -> None:
    """Averaging a provider timeout in as a zero lets an outage read as a regression."""
    summary = summarise_conversation(
        [
            TurnResult(
                case_id="c", ordinal=1, question="q", relevant_documents=["a.md"], hit=True,
                recall=1.0,
            ),
            TurnResult(
                case_id="c", ordinal=2, question="q2", relevant_documents=["a.md"],
                error="ProviderError: down",
            ),
        ],
        top_k=5,
        wall_seconds=1.0,
        max_messages=20,
    )

    assert summary["turns_scored"] == 1.0
    assert summary["multi_turn_recall@5"] == 1.0


async def test_the_configuration_travels_with_the_numbers(
    evaluator: ConversationalEvaluator,
) -> None:
    report = await evaluator.run(
        _set(
            {"question": "how many leave days", "relevant_documents": ["hr/leave.md"]},
            {"question": "and expenses", "relevant_documents": ["hr/expenses.md"]},
        )
    )

    assert report.configuration["retrieval"]["top_k"] == 3
    assert report.configuration["retrieval"]["rewrite_queries"] is False


async def test_a_report_round_trips_to_a_serialisable_dict(
    evaluator: ConversationalEvaluator,
) -> None:
    import json

    report = await evaluator.run(
        _set(
            {"question": "how many leave days", "relevant_documents": ["hr/leave.md"]},
            {"question": "and expenses", "relevant_documents": ["hr/expenses.md"]},
        )
    )
    payload = json.loads(json.dumps(report.to_dict()))

    assert payload["turn_count"] == 2
    assert payload["turns"][0]["case_id"] == "case"
    assert "multi_turn_recall@3" in payload["summary"]


def test_conversational_false_abstention_excludes_required_refusals_and_errors() -> None:
    turns = [
        TurnResult(case_id="a", ordinal=1, question="q", answer="yes"),
        TurnResult(case_id="a", ordinal=2, question="q", abstained=True),
        TurnResult(case_id="a", ordinal=3, question="q", must_abstain=True, abstained=True),
        TurnResult(case_id="a", ordinal=4, question="q", error="timeout"),
    ]
    summary = summarise_conversation(turns, top_k=5, wall_seconds=1.0, max_messages=20)
    assert summary["multi_turn_false_abstention_rate"] == 0.5
    for subset in ([], turns[2:3], turns[3:]):
        empty = summarise_conversation(subset, top_k=5, wall_seconds=1.0, max_messages=20)
        assert "multi_turn_false_abstention_rate" not in empty
