"""Executes multi-turn golden cases against a live system and scores them.

Separate from `runner` because a conversation is a different unit of work, not a
harder single-turn case: turns are ordered, share a session, and cannot be run
concurrently within a case. What is *not* different is the arithmetic — every turn
is scored by the same functions in `metrics` that score a single-turn case, so
`recall@k` means the same thing in both reports.

## The control run

The design decision that makes this worth having. A follow-up that gets answered
proves nothing on its own: "what type is it?" may retrieve the right document by
keyword luck, and a harness that only reported the in-session number would show a
healthy `follow_up_resolution` for a system with no memory at all.

So every turn flagged `requires_context` or `context_switch` is run **twice**: once
in the session, and once cold with no history at all. The pair is the measurement.

* For `requires_context`, the cold run is the floor. The session run should beat it,
  and `follow_up_lift` is by how much. A lift of zero means either the memory is not
  reaching retrieval or the golden set's follow-ups are not really context
  dependent — both worth knowing, and neither visible from one number.
* For `context_switch`, the cold run is the *benchmark to match*. A standalone
  question should retrieve exactly as well mid-conversation as it does cold;
  scoring below the control is the signature of history polluting retrieval.

The control is a retrieval-only call. It costs no generation, and retrieval is
where the whole effect lives: history reaches search only through the query
rewriter, and reaches generation as prompt context regardless.

## Session isolation

Cases run interleaved when concurrency allows, which is what a real service does.
`session_isolation` checks that turn *n* of a case was answered against exactly its
own `2 * (n - 1)` preceding messages: a session that had absorbed another live
conversation would carry more. Counting context, not comparing retrieved documents
— with eleven documents and `top_k` of five, nearly every turn legitimately
retrieves something another case also expects, so a document-overlap metric would
report a catastrophic leak on a perfectly isolated system.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

from ..conversation import Conversation
from ..logging import get_logger
from ..retrieval.pipeline import RetrievalPipeline
from ..settings import Settings
from ..types import Answer
from . import metrics
from .dataset import ConversationalCase, ConversationalSet, ConversationalTurn, document_key
from .judge import FaithfulnessJudge
from .metrics import mean_of

# The one thing this module borrows from its sibling. `configuration_snapshot`
# defines what a result file records about the system that produced it, and both
# report shapes must agree on that or two runs cannot be compared. `mean_of` used to
# come from here too and now lives in `metrics`, where a pure function belongs.
from .runner import configuration_snapshot

log = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class TurnResult:
    """One scored turn. Flat and JSON-serialisable, like `CaseResult`."""

    case_id: str
    ordinal: int
    question: str
    tags: list[str] = field(default_factory=list)

    requires_context: bool = False
    context_switch: bool = False
    context_messages: int = 0
    """Messages the session held when this turn ran. Feeds `session_isolation`."""

    # ---- retrieval, in session
    relevant_documents: list[str] = field(default_factory=list)
    retrieved_documents: list[str] = field(default_factory=list)
    recall: float = 0.0
    precision: float = 0.0
    reciprocal_rank: float = 0.0
    ndcg: float = 0.0
    hit: bool = False

    # ---- retrieval, cold control. None when this turn was not control-run.
    control_recall: float | None = None
    control_hit: bool | None = None
    control_trace_id: str = ""

    # ---- generation
    answer: str = ""
    abstained: bool = False
    must_abstain: bool = False
    citations: int = 0
    grounded_citations: int = 0
    cited_relevant: int = 0
    missing_facts: list[str] = field(default_factory=list)
    expected_facts: int = 0
    faithful: bool | None = None

    # ---- cost
    latency_seconds: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0

    trace_id: str = ""
    error: str | None = None

    @property
    def scored(self) -> bool:
        return self.error is None


@dataclass(frozen=True, slots=True)
class ConversationalReport:
    """One multi-turn evaluation run."""

    started_at: str
    duration_seconds: float
    golden_set: str
    case_count: int
    turn_count: int
    failed_turns: int
    top_k: int
    concurrency: int
    generation: bool
    configuration: dict[str, Any]
    summary: dict[str, float]
    turns: list[TurnResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "started_at": self.started_at,
            "duration_seconds": round(self.duration_seconds, 3),
            "golden_set": self.golden_set,
            "case_count": self.case_count,
            "turn_count": self.turn_count,
            "failed_turns": self.failed_turns,
            "top_k": self.top_k,
            "concurrency": self.concurrency,
            "generation": self.generation,
            "configuration": self.configuration,
            "summary": self.summary,
            "turns": [asdict(turn) for turn in self.turns],
        }


class ConversationalEvaluator:
    """Runs a multi-turn golden set and scores it."""

    def __init__(
        self,
        conversation: Conversation,
        retrieval: RetrievalPipeline,
        settings: Settings,
        judge: FaithfulnessJudge | None = None,
    ) -> None:
        self._conversation = conversation
        self._retrieval = retrieval
        self._settings = settings
        self._judge = judge

    async def run(
        self,
        conversational: ConversationalSet,
        *,
        name: str = "conversational",
        concurrency: int = 1,
    ) -> ConversationalReport:
        """Score every case, at most `concurrency` sessions at a time.

        Concurrency is over *cases*, never over turns: the turns of one conversation
        are ordered by definition, and running them in parallel would measure a
        system nobody uses.
        """
        top_k = self._settings.retrieval.top_k
        limit = asyncio.Semaphore(max(1, concurrency))
        started = time.perf_counter()
        started_at = datetime.now(UTC).isoformat()

        async def run_one(case: ConversationalCase) -> list[TurnResult]:
            async with limit:
                return await self._evaluate_case(case, top_k)

        per_case = await asyncio.gather(*(run_one(case) for case in conversational.cases))
        elapsed = time.perf_counter() - started
        turns = [turn for case_turns in per_case for turn in case_turns]

        report = ConversationalReport(
            started_at=started_at,
            duration_seconds=elapsed,
            golden_set=name,
            case_count=len(conversational.cases),
            turn_count=len(turns),
            failed_turns=sum(1 for turn in turns if not turn.scored),
            top_k=top_k,
            concurrency=concurrency,
            generation=True,
            configuration=configuration_snapshot(self._settings),
            summary=summarise_conversation(
                turns,
                top_k=top_k,
                wall_seconds=elapsed,
                max_messages=self._settings.session.max_messages,
            ),
            turns=turns,
        )
        log.info(
            "evaluation.conversational_complete",
            extra={
                "cases": report.case_count,
                "turns": report.turn_count,
                "failed": report.failed_turns,
                "duration_seconds": round(elapsed, 3),
                **report.summary,
            },
        )
        return report

    async def _evaluate_case(
        self, case: ConversationalCase, top_k: int
    ) -> list[TurnResult]:
        """Run one session end to end, closing it whichever way the case ends.

        The session is closed in a `finally`, so a turn that raises still releases
        its memory. A harness that leaked a session per failed case would slowly
        turn a long evaluation run into an out-of-memory report.
        """
        session_id = await self._conversation.start()
        results: list[TurnResult] = []
        try:
            for ordinal, turn in enumerate(case.turns, start=1):
                results.append(await self._evaluate_turn(case, turn, ordinal, session_id, top_k))
        finally:
            await self._conversation.close(session_id)
        return results

    async def _evaluate_turn(
        self,
        case: ConversationalCase,
        turn: ConversationalTurn,
        ordinal: int,
        session_id: str,
        top_k: int,
    ) -> TurnResult:
        started = time.perf_counter()
        try:
            # Read before the turn runs: afterwards it includes this exchange, and
            # the property being checked is what the turn was *answered against*.
            context_messages = len(await self._conversation.history(session_id))
            answer = await self._conversation.answer(session_id, turn.question)
            result = self._score(
                case, turn, ordinal, answer, time.perf_counter() - started, top_k,
                context_messages=context_messages,
            )

            if turn.requires_context or turn.context_switch:
                result = await self._add_control(result, turn, top_k)
            if self._judge is not None and not result.abstained and result.answer:
                verdict = await self._judge.is_faithful(
                    turn.question, result.answer, answer.retrieved
                )
                result = TurnResult(**{**asdict(result), "faithful": verdict})
            return result
        # Broad by intent, and the same reasoning as the single-turn runner: one
        # provider hiccup must not discard the rest of the run. The turn is recorded
        # as failed and the conversation continues, because a later turn failing
        # differently is itself information.
        except Exception as exc:
            log.error(
                "evaluation.turn_failed",
                extra={"case": case.id, "turn": ordinal, "error": str(exc)},
            )
            return TurnResult(
                case_id=case.id,
                ordinal=ordinal,
                question=turn.question,
                tags=list(case.tags),
                requires_context=turn.requires_context,
                context_switch=turn.context_switch,
                relevant_documents=list(turn.relevant_documents),
                must_abstain=turn.must_abstain,
                expected_facts=len(turn.expected_facts),
                latency_seconds=time.perf_counter() - started,
                error=f"{type(exc).__name__}: {exc}",
            )

    async def _add_control(
        self, result: TurnResult, turn: ConversationalTurn, top_k: int
    ) -> TurnResult:
        """Re-run this turn's question cold, and attach what it retrieved.

        Retrieval only. The lift being measured lives entirely in retrieval —
        history reaches search through the rewriter and nowhere else — and running
        generation again would double the cost of the run to produce a number
        nothing reads.
        """
        control = await self._retrieval.retrieve(turn.question)
        ranked = metrics.dedupe(document_key(hit.chunk) for hit in control.chunks)
        return TurnResult(
            **{
                **asdict(result),
                "control_recall": metrics.recall_at_k(turn.relevant_documents, ranked, top_k),
                "control_hit": metrics.hit_at_k(turn.relevant_documents, ranked, top_k),
                "control_trace_id": control.trace_id,
            }
        )

    def _score(
        self,
        case: ConversationalCase,
        turn: ConversationalTurn,
        ordinal: int,
        answer: Answer,
        latency: float,
        top_k: int,
        *,
        context_messages: int,
    ) -> TurnResult:
        ranked = metrics.dedupe(document_key(hit.chunk) for hit in answer.retrieved)
        relevant = turn.relevant_documents

        retrieved_chunk_ids = {hit.chunk.id for hit in answer.retrieved}
        chunk_documents = {hit.chunk.id: document_key(hit.chunk) for hit in answer.retrieved}
        grounded = [
            citation for citation in answer.citations if citation.chunk_id in retrieved_chunk_ids
        ]
        cited_relevant = [
            citation
            for citation in grounded
            if chunk_documents.get(citation.chunk_id, "") in set(relevant)
        ]

        lowered = answer.text.lower()
        return TurnResult(
            case_id=case.id,
            ordinal=ordinal,
            question=turn.question,
            tags=list(case.tags),
            requires_context=turn.requires_context,
            context_switch=turn.context_switch,
            context_messages=context_messages,
            relevant_documents=list(relevant),
            retrieved_documents=ranked,
            recall=metrics.recall_at_k(relevant, ranked, top_k),
            precision=metrics.precision_at_k(relevant, ranked, top_k),
            reciprocal_rank=metrics.reciprocal_rank(relevant, ranked),
            ndcg=metrics.ndcg_at_k(relevant, ranked, top_k),
            hit=metrics.hit_at_k(relevant, ranked, top_k),
            answer=answer.text,
            abstained=answer.abstained,
            must_abstain=turn.must_abstain,
            citations=len(answer.citations),
            grounded_citations=len(grounded),
            cited_relevant=len(cited_relevant),
            missing_facts=[fact for fact in turn.expected_facts if fact.lower() not in lowered],
            expected_facts=len(turn.expected_facts),
            latency_seconds=latency,
            input_tokens=answer.usage.input_tokens,
            output_tokens=answer.usage.output_tokens,
            trace_id=answer.trace_id,
        )


def summarise_conversation(
    turns: Sequence[TurnResult],
    *,
    top_k: int,
    wall_seconds: float,
    max_messages: int,
) -> dict[str, float]:
    """Aggregate turns into the conversational numbers a run is judged on.

    Failed turns are excluded from every quality mean and reported as a count, for
    the same reason the single-turn runner excludes them: averaging a provider
    timeout in as a zero lets an infrastructure problem read as a memory regression.
    """
    scored = [turn for turn in turns if turn.scored]
    if not scored:
        return {"turns_scored": 0.0, "throughput_per_second": 0.0}

    retrieval_turns = [turn for turn in scored if turn.relevant_documents]
    follow_ups = [turn for turn in scored if turn.requires_context and turn.relevant_documents]
    switches = [turn for turn in scored if turn.context_switch and turn.relevant_documents]
    answered = [turn for turn in scored if not turn.abstained and turn.answer]
    with_facts = [turn for turn in scored if turn.expected_facts]
    abstention_turns = [turn for turn in scored if turn.must_abstain]
    judged = [turn for turn in scored if turn.faithful is not None]
    latencies = [turn.latency_seconds for turn in scored]

    citations_total = sum(turn.citations for turn in answered)
    grounded_total = sum(turn.grounded_citations for turn in answered)
    relevant_citations = sum(turn.cited_relevant for turn in answered)

    summary: dict[str, float] = {
        "cases_scored": float(len({turn.case_id for turn in scored})),
        "turns_scored": float(len(scored)),
        # ---- retrieval across every turn
        f"multi_turn_recall@{top_k}": mean_of(retrieval_turns, lambda t: t.recall),
        f"multi_turn_precision@{top_k}": mean_of(retrieval_turns, lambda t: t.precision),
        f"multi_turn_ndcg@{top_k}": mean_of(retrieval_turns, lambda t: t.ndcg),
        "multi_turn_mrr": mean_of(retrieval_turns, lambda t: t.reciprocal_rank),
        f"multi_turn_hit_rate@{top_k}": mean_of(retrieval_turns, lambda t: float(t.hit)),
        # ---- generation across every turn
        "multi_turn_citation_coverage": mean_of(answered, lambda t: float(t.citations > 0)),
        "multi_turn_groundedness": metrics.ratio(grounded_total, citations_total),
        "multi_turn_citation_precision": metrics.ratio(relevant_citations, citations_total),
        "multi_turn_fact_match": mean_of(with_facts, lambda t: float(not t.missing_facts)),
        "multi_turn_abstention_accuracy": mean_of(
            abstention_turns, lambda t: float(t.abstained)
        ),
    }

    answerable = [turn for turn in scored if not turn.must_abstain]
    if answerable:
        summary["multi_turn_false_abstention_rate"] = mean_of(
            answerable, lambda t: float(t.abstained)
        )

    # ---- the conversational metrics proper, each reported with its control.
    if follow_ups:
        with_context = mean_of(follow_ups, lambda t: float(t.hit))
        cold = mean_of(follow_ups, lambda t: float(bool(t.control_hit)))
        summary.update(
            {
                "follow_up_resolution": with_context,
                "follow_up_resolution_no_context": cold,
                # Signed on purpose. Negative means the conversation made these
                # questions *harder* to retrieve for, which is a real and reportable
                # outcome, not an impossible one.
                "follow_up_lift": round(with_context - cold, 4),
            }
        )
    if switches:
        in_context = mean_of(switches, lambda t: float(t.hit))
        cold_switch = mean_of(switches, lambda t: float(bool(t.control_hit)))
        summary.update(
            {
                "context_switch_recovery": in_context,
                "context_switch_recovery_no_context": cold_switch,
                # Here the control is the benchmark to match, so the useful number is
                # how far *below* it the in-conversation run fell. Zero is the target.
                "context_pollution": round(max(0.0, cold_switch - in_context), 4),
            }
        )

    summary["session_isolation"] = _session_isolation(scored, max_messages)

    if judged:
        summary["multi_turn_faithfulness"] = mean_of(judged, lambda t: float(bool(t.faithful)))

    summary.update(
        {
            "latency_p50_seconds": round(metrics.percentile(latencies, 0.50), 3),
            "latency_p95_seconds": round(metrics.percentile(latencies, 0.95), 3),
            "latency_mean_seconds": round(metrics.mean(latencies), 3),
            "throughput_per_second": (
                round(len(scored) / wall_seconds, 3) if wall_seconds else 0.0
            ),
            "input_tokens_total": float(sum(turn.input_tokens for turn in scored)),
            "output_tokens_total": float(sum(turn.output_tokens for turn in scored)),
        }
    )
    return summary


def _session_isolation(turns: Sequence[TurnResult], max_messages: int) -> float:
    """Fraction of turns whose session held exactly its own conversation, no more.

    Turn *n* of a case must run against exactly `2 * (n - 1)` messages — its own
    preceding exchanges and nothing else — bounded by `session.max_messages` once a
    long conversation starts being trimmed. A session that had absorbed another
    concurrently-live conversation would carry more.

    Counting messages rather than comparing retrieved documents is deliberate, and
    the alternative is worth recording because it looks correct and is not. This
    corpus has eleven documents and `top_k` is five, so nearly every turn
    legitimately retrieves documents that some other case also expects. A metric
    built on that overlap would report a catastrophic leak on a perfectly isolated
    system. Context size is the property actually at stake, and it is exact.

    Expected to be 1.0 — like `groundedness`, the value is that it stops being 1.0
    the day sessions start sharing state.
    """
    if not turns:
        return 1.0
    clean = sum(
        1
        for turn in turns
        if turn.context_messages == min(2 * (turn.ordinal - 1), max_messages)
    )
    return round(clean / len(turns), 4)


__all__ = [
    "ConversationalEvaluator",
    "ConversationalReport",
    "TurnResult",
    "summarise_conversation",
]
