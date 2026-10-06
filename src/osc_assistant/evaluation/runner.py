"""Executes a golden set against a live system and scores the result.

This is the module that turns "the retrieval feels better" into a number that a
pull request can be gated on. It drives the *real* pipelines — the same
`RetrievalPipeline` and `Answerer` the API and the CLI use, built by the same
`Container` — because an evaluation that runs against a special code path measures
the special code path.

Three properties are load-bearing:

**A case never aborts the run.** A provider timeout on question 34 of 90 must not
throw away the 33 results already collected; it is recorded as a failed case, and
the report says how many failed. An evaluation harness that is itself fragile does
not get run.

**Every case records its trace id.** The report says recall was 0.6; the trace id on
the two cases that missed says *why*, expandable with `./osc trace <id>` after the
run has finished. Without it a bad number is a starting point for a reproduction
rather than an explanation.

**The configuration that produced the numbers travels with them.** A result JSON
carries the chunker, the retrieval settings and both model ids, so comparing two
runs cannot silently compare two different systems — which is the whole point of
being able to run `--profile config/experiments/hosted-anthropic.yaml`.
"""

from __future__ import annotations

import asyncio
import hashlib
import time
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

from ..generation.answerer import Answerer
from ..generation.prompts import ANSWER_SYSTEM_PROMPT
from ..logging import get_logger
from ..retrieval.pipeline import RetrievalPipeline
from ..settings import Settings
from ..types import Answer, ScoredChunk
from . import metrics
from .dataset import GoldenCase, GoldenSet, document_key
from .judge import FaithfulnessJudge
from .metrics import mean_of

log = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class CaseResult:
    """Everything one golden case produced, scored.

    Kept flat and JSON-serialisable on purpose: this is the unit that is written to
    a result file, diffed against a baseline, and read by a human deciding whether
    a change helped.
    """

    id: str
    question: str
    tags: list[str] = field(default_factory=list)

    # ---- retrieval
    relevant_documents: list[str] = field(default_factory=list)
    retrieved_documents: list[str] = field(default_factory=list)
    recall: float = 0.0
    precision: float = 0.0
    reciprocal_rank: float = 0.0
    ndcg: float = 0.0
    hit: bool = False

    # ---- generation. Left at defaults by a retrieval-only run.
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
        """Whether this case contributed a measurement rather than an error."""
        return self.error is None


@dataclass(frozen=True, slots=True)
class EvaluationReport:
    """One evaluation run: what was measured, under what configuration."""

    started_at: str
    duration_seconds: float
    golden_set: str
    case_count: int
    failed_count: int
    top_k: int
    concurrency: int
    generation: bool
    configuration: dict[str, Any]
    summary: dict[str, float]
    cases: list[CaseResult]

    def to_dict(self) -> dict[str, Any]:
        """The on-disk shape. Stable, because baselines are compared against it."""
        return {
            "started_at": self.started_at,
            "duration_seconds": round(self.duration_seconds, 3),
            "golden_set": self.golden_set,
            "case_count": self.case_count,
            "failed_count": self.failed_count,
            "top_k": self.top_k,
            "concurrency": self.concurrency,
            "generation": self.generation,
            "configuration": self.configuration,
            "summary": self.summary,
            "cases": [asdict(case) for case in self.cases],
        }


def configuration_snapshot(settings: Settings) -> dict[str, Any]:
    """The settings that can change a score.

    Only these. A result file that recorded the whole configuration would differ
    between two machines over the database DSN and the log level, and a comparison
    tool cannot tell an irrelevant difference from a relevant one — so the decision
    about which settings are relevant is made here, once, in the open.
    """
    return {
        "profile_environment": settings.environment,
        "llm": f"{settings.llm.provider}/{settings.llm.model}",
        "embeddings": f"{settings.embeddings.provider}/{settings.embeddings.model}",
        "reranker": settings.reranker.provider,
        "vector_store": settings.vector_store.provider,
        "chunking": {
            "strategy": settings.chunking.strategy,
            "chunk_size": settings.chunking.chunk_size,
            "chunk_overlap": settings.chunking.chunk_overlap,
        },
        "retrieval": {
            "strategy": settings.retrieval.strategy,
            "candidates": settings.retrieval.candidates,
            "top_k": settings.retrieval.top_k,
            "rrf_k": settings.retrieval.rrf_k,
            "min_score": settings.retrieval.min_score,
            "rewrite_queries": settings.retrieval.rewrite_queries,
        },
        "generation": {
            "max_tokens": settings.generation.max_tokens,
            "require_citations": settings.generation.require_citations,
            "answer_system_prompt_sha256": hashlib.sha256(
                ANSWER_SYSTEM_PROMPT.encode("utf-8")
            ).hexdigest(),
        },
    }


class Evaluator:
    """Runs a golden set and scores it.

    Takes the pipelines rather than the `Container` so that the unit tests can
    drive it with in-process doubles through the same constructor the CLI uses.
    """

    def __init__(
        self,
        retrieval: RetrievalPipeline,
        settings: Settings,
        answerer: Answerer | None = None,
        judge: FaithfulnessJudge | None = None,
    ) -> None:
        self._retrieval = retrieval
        self._answerer = answerer
        self._judge = judge
        self._settings = settings

    async def run(
        self,
        golden: GoldenSet,
        *,
        name: str = "golden-set",
        concurrency: int = 1,
    ) -> EvaluationReport:
        """Score every case in `golden`, at most `concurrency` at a time."""
        top_k = self._settings.retrieval.top_k
        limit = asyncio.Semaphore(max(1, concurrency))
        started = time.perf_counter()
        started_at = datetime.now(UTC).isoformat()

        async def run_one(case: GoldenCase) -> CaseResult:
            async with limit:
                return await self._evaluate_case(case, top_k)

        # `gather` rather than a loop even at concurrency 1: it keeps one code path,
        # and `_evaluate_case` already converts a failure into a result, so no
        # exception can reach here and cancel the siblings.
        results = await asyncio.gather(*(run_one(case) for case in golden.cases))
        elapsed = time.perf_counter() - started

        report = EvaluationReport(
            started_at=started_at,
            duration_seconds=elapsed,
            golden_set=name,
            case_count=len(results),
            failed_count=sum(1 for result in results if not result.scored),
            top_k=top_k,
            concurrency=concurrency,
            generation=self._answerer is not None,
            configuration=configuration_snapshot(self._settings),
            summary=summarise(
                results,
                top_k=top_k,
                wall_seconds=elapsed,
                generation=self._answerer is not None,
            ),
            cases=list(results),
        )
        log.info(
            "evaluation.complete",
            extra={
                "cases": report.case_count,
                "failed": report.failed_count,
                "duration_seconds": round(elapsed, 3),
                **report.summary,
            },
        )
        return report

    async def _evaluate_case(self, case: GoldenCase, top_k: int) -> CaseResult:
        started = time.perf_counter()
        try:
            if self._answerer is not None:
                answer = await self._answerer.answer(case.question)
                result = self._score_answer(case, answer, top_k, time.perf_counter() - started)
                # Judged here rather than in a second pass because this is the only
                # point at which the source text the answer was built from is still
                # in hand. Carrying it out to a later pass would mean putting whole
                # chunk bodies on a result object that gets written to disk.
                if self._judge is not None and not result.abstained and result.answer:
                    verdict = await self._judge.is_faithful(
                        case.question, result.answer, answer.retrieved
                    )
                    result = CaseResult(**{**asdict(result), "faithful": verdict})
                return result

            retrieval = await self._retrieval.retrieve(case.question)
            return self._score_retrieval(
                case,
                retrieval.chunks,
                top_k,
                time.perf_counter() - started,
                retrieval.trace_id,
            )
        # Broad by intent, and the same reasoning as the ingestion loader: one
        # provider hiccup on one question must not discard the rest of the run.
        # The error is carried on the result so the report can name it.
        except Exception as exc:
            log.error(
                "evaluation.case_failed",
                extra={"case": case.id, "error": str(exc)},
            )
            return CaseResult(
                id=case.id,
                question=case.question,
                tags=list(case.tags),
                relevant_documents=list(case.relevant_documents),
                must_abstain=case.must_abstain,
                expected_facts=len(case.expected_facts),
                latency_seconds=time.perf_counter() - started,
                error=f"{type(exc).__name__}: {exc}",
            )

    def _score_retrieval(
        self,
        case: GoldenCase,
        chunks: Sequence[ScoredChunk],
        top_k: int,
        latency: float,
        trace_id: str,
    ) -> CaseResult:
        ranked = metrics.dedupe(document_key(hit.chunk) for hit in chunks)
        relevant = case.relevant_documents
        return CaseResult(
            id=case.id,
            question=case.question,
            tags=list(case.tags),
            relevant_documents=list(relevant),
            retrieved_documents=ranked,
            recall=metrics.recall_at_k(relevant, ranked, top_k),
            precision=metrics.precision_at_k(relevant, ranked, top_k),
            reciprocal_rank=metrics.reciprocal_rank(relevant, ranked),
            ndcg=metrics.ndcg_at_k(relevant, ranked, top_k),
            hit=metrics.hit_at_k(relevant, ranked, top_k),
            must_abstain=case.must_abstain,
            expected_facts=len(case.expected_facts),
            latency_seconds=latency,
            trace_id=trace_id,
        )

    def _score_answer(
        self, case: GoldenCase, answer: Answer, top_k: int, latency: float
    ) -> CaseResult:
        base = self._score_retrieval(case, answer.retrieved, top_k, latency, answer.trace_id)

        retrieved_chunk_ids = {hit.chunk.id for hit in answer.retrieved}
        relevant = set(case.relevant_documents)
        chunk_documents = {hit.chunk.id: document_key(hit.chunk) for hit in answer.retrieved}

        # A citation whose chunk was not in the retrieved set cannot have been read
        # from a source, because the model was never shown one. On the native
        # citation path that is impossible; on the marker-parsing path it is the
        # exact failure mode being measured, and it is measurable without a judge.
        grounded = [
            citation for citation in answer.citations if citation.chunk_id in retrieved_chunk_ids
        ]
        cited_relevant = [
            citation
            for citation in grounded
            if chunk_documents.get(citation.chunk_id, "") in relevant
        ]

        lowered = answer.text.lower()
        missing = [fact for fact in case.expected_facts if fact.lower() not in lowered]

        return CaseResult(
            **{
                **{
                    key: value
                    for key, value in asdict(base).items()
                    if key not in {"answer", "abstained", "citations"}
                },
                "answer": answer.text,
                "abstained": answer.abstained,
                "citations": len(answer.citations),
                "grounded_citations": len(grounded),
                "cited_relevant": len(cited_relevant),
                "missing_facts": missing,
                "input_tokens": answer.usage.input_tokens,
                "output_tokens": answer.usage.output_tokens,
            }
        )

def summarise(
    results: Sequence[CaseResult],
    *,
    top_k: int,
    wall_seconds: float,
    generation: bool = True,
) -> dict[str, float]:
    """Aggregate per-case results into the numbers a run is judged on.

    Two exclusions are deliberate, and both exist to stop the summary from
    reporting a number that is arithmetically correct and factually a lie.

    **Failed cases are excluded from every quality mean** and reported separately as
    a count. Averaging a provider timeout in as a zero would let an unrelated
    infrastructure problem read as a retrieval regression, which is the fastest way
    to teach a team to ignore the dashboard.

    **A retrieval-only run reports no generation metrics at all.** It is tempting to
    let them fall out at zero, but `fact_match` is computed as "no expected fact was
    missing", and a run that generated no answers has missed nothing — so it scores
    a perfect 1.0 for work it never did. Omitting the keys also makes `compare`
    refuse to diff a retrieval-only run against a full one, which is the right
    answer to a comparison that was never meaningful.
    """
    scored = [result for result in results if result.scored]
    if not scored:
        return {"cases_scored": 0.0, "throughput_per_second": 0.0}

    retrieval_cases = [result for result in scored if result.relevant_documents]
    latencies = [result.latency_seconds for result in scored]

    summary: dict[str, float] = {
        "cases_scored": float(len(scored)),
        # ---- retrieval
        f"recall@{top_k}": mean_of(retrieval_cases, lambda r: r.recall),
        f"precision@{top_k}": mean_of(retrieval_cases, lambda r: r.precision),
        f"ndcg@{top_k}": mean_of(retrieval_cases, lambda r: r.ndcg),
        "mrr": mean_of(retrieval_cases, lambda r: r.reciprocal_rank),
        f"hit_rate@{top_k}": mean_of(retrieval_cases, lambda r: float(r.hit)),
    }

    if generation:
        answered = [result for result in scored if not result.abstained and result.answer]
        with_facts = [result for result in scored if result.expected_facts]
        abstention_cases = [result for result in scored if result.must_abstain]
        judged = [result for result in scored if result.faithful is not None]

        citations_total = sum(result.citations for result in answered)
        grounded_total = sum(result.grounded_citations for result in answered)
        relevant_citations = sum(result.cited_relevant for result in answered)

        summary.update(
            {
                "citation_coverage": mean_of(answered, lambda r: float(r.citations > 0)),
                "groundedness": metrics.ratio(grounded_total, citations_total),
                "citation_precision": metrics.ratio(relevant_citations, citations_total),
                "fact_match": mean_of(with_facts, lambda r: float(not r.missing_facts)),
                "abstention_accuracy": mean_of(abstention_cases, lambda r: float(r.abstained)),
            }
        )
        answerable = [result for result in scored if not result.must_abstain]
        if answerable:
            summary["false_abstention_rate"] = mean_of(answerable, lambda r: float(r.abstained))
        if judged:
            summary["faithfulness"] = mean_of(judged, lambda r: float(bool(r.faithful)))

    summary.update(
        {
            "latency_p50_seconds": round(metrics.percentile(latencies, 0.50), 3),
            "latency_p95_seconds": round(metrics.percentile(latencies, 0.95), 3),
            "latency_mean_seconds": round(metrics.mean(latencies), 3),
            "throughput_per_second": round(len(scored) / wall_seconds, 3) if wall_seconds else 0.0,
            "input_tokens_total": float(sum(result.input_tokens for result in scored)),
            "output_tokens_total": float(sum(result.output_tokens for result in scored)),
        }
    )
    return summary


def compare(baseline: dict[str, Any], current: dict[str, Any]) -> list[tuple[str, float, float]]:
    """Metrics present in both runs, as (name, baseline, current).

    Only the intersection: a metric that appeared or disappeared between two runs
    is a change in the harness, not a change in quality, and presenting it as a
    delta against zero would be a lie in whichever direction the metric points.
    """
    before = baseline.get("summary", {})
    after = current.get("summary", {})
    return [
        (name, float(before[name]), float(after[name]))
        for name in sorted(set(before) & set(after))
        if isinstance(before[name], int | float) and isinstance(after[name], int | float)
    ]
