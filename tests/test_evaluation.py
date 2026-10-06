"""Evaluation harness tests.

The harness is the instrument every future retrieval decision will be read off, so
these tests care most about the ways an instrument can lie: a metric that reports a
score for work that was never done, a golden set whose typo reads as a system
regression, a failed case that silently drags a mean down, a comparison between two
runs that measured different things.

Everything runs against the in-process doubles in `conftest`. The production corpus
under `docs/company/` is deliberately never touched: a test that depended on it
would start failing the day someone edited an FAQ answer, which is exactly the kind
of false alarm that gets a suite disabled.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from osc_assistant.chunking import ChunkerOptions, RecursiveChunker
from osc_assistant.errors import EvaluationError
from osc_assistant.evaluation import (
    Evaluator,
    FaithfulnessJudge,
    GoldenSet,
    load_golden_set,
    unresolvable_documents,
)
from osc_assistant.evaluation import metrics as m
from osc_assistant.evaluation.dataset import document_key
from osc_assistant.evaluation.judge import _parse_verdict
from osc_assistant.evaluation.runner import CaseResult, compare, summarise
from osc_assistant.generation import Answerer
from osc_assistant.ingestion import IngestionPipeline, InMemoryLoader
from osc_assistant.providers.reranking.noop import NoopReranker
from osc_assistant.providers.vectorstores.memory import MemoryVectorStore
from osc_assistant.retrieval import RetrievalPipeline
from osc_assistant.settings import RetrievalSettings, Settings
from osc_assistant.types import Chunk, Document

from .conftest import EMBEDDING_DIMENSIONS, FailingChatModel, StubChatModel, StubEmbeddingModel

# --------------------------------------------------------------------------- metrics


def test_dedupe_preserves_rank_order_and_drops_repeats():
    assert m.dedupe(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]


def test_recall_counts_relevant_documents_found_within_k():
    # Two relevant, one of them inside the top 2 → 0.5.
    assert m.recall_at_k(["a", "z"], ["a", "b", "z"], 2) == pytest.approx(0.5)
    assert m.recall_at_k(["a", "z"], ["a", "b", "z"], 3) == pytest.approx(1.0)


def test_recall_of_a_case_with_no_relevant_documents_is_zero_not_undefined():
    assert m.recall_at_k([], ["a"], 5) == 0.0


def test_precision_divides_by_k_not_by_results_returned():
    # One hit in a top-5 request that only returned two results is still 0.2: the
    # three unfilled slots were context the model could have had.
    assert m.precision_at_k(["a"], ["a", "b"], 5) == pytest.approx(0.2)


def test_reciprocal_rank_is_the_inverse_of_the_first_relevant_position():
    assert m.reciprocal_rank(["c"], ["a", "b", "c"]) == pytest.approx(1 / 3)
    assert m.reciprocal_rank(["z"], ["a", "b", "c"]) == 0.0


def test_hit_is_the_binary_form_of_recall():
    assert m.hit_at_k(["a", "z"], ["b", "a"], 2) is True
    assert m.hit_at_k(["z"], ["b", "a"], 2) is False


def test_percentile_returns_an_observed_value_not_an_interpolation():
    latencies = [1.0, 2.0, 3.0, 100.0]
    assert m.percentile(latencies, 0.95) in latencies
    assert m.percentile(latencies, 0.50) in latencies
    assert m.percentile([], 0.95) == 0.0


def test_mean_of_nothing_is_zero_so_an_empty_run_stays_reportable():
    assert m.mean([]) == 0.0


# --------------------------------------------------------------------------- dataset


def _write(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "golden.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def test_a_valid_golden_set_loads(tmp_path: Path):
    golden = load_golden_set(
        _write(
            tmp_path,
            """
            version: 1
            cases:
              - id: one
                question: How many days?
                relevant_documents: ["./handbook/leave.md"]
                expected_facts: ["25"]
                tags: [hr]
            """,
        )
    )
    assert len(golden.cases) == 1
    # Leading "./" is normalised away so two spellings of one path cannot both
    # appear and be counted as two documents.
    assert golden.cases[0].relevant_documents == ["handbook/leave.md"]
    assert golden.referenced_documents == {"handbook/leave.md"}


def test_duplicate_case_ids_are_rejected(tmp_path: Path):
    with pytest.raises(EvaluationError, match="duplicate case id"):
        load_golden_set(
            _write(
                tmp_path,
                """
                cases:
                  - {id: same, question: a, relevant_documents: [x.md]}
                  - {id: same, question: b, relevant_documents: [y.md]}
                """,
            )
        )


def test_an_unscoreable_case_is_rejected_rather_than_scored_zero(tmp_path: Path):
    # No relevant documents and not an abstention case: nothing about it can be
    # measured, and left in it would look like a permanent retrieval failure.
    with pytest.raises(EvaluationError, match="nothing about it can be scored"):
        load_golden_set(_write(tmp_path, "cases:\n  - {id: a, question: q}\n"))


def test_an_abstention_case_may_not_also_name_relevant_documents(tmp_path: Path):
    with pytest.raises(EvaluationError, match="also names relevant_documents"):
        load_golden_set(
            _write(
                tmp_path,
                "cases:\n  - {id: a, question: q, must_abstain: true, "
                "relevant_documents: [x.md]}\n",
            )
        )


def test_malformed_yaml_is_an_operator_message_not_a_traceback(tmp_path: Path):
    with pytest.raises(EvaluationError, match="not valid YAML"):
        load_golden_set(_write(tmp_path, "cases: [unclosed\n"))


def test_a_missing_golden_set_names_the_file(tmp_path: Path):
    with pytest.raises(EvaluationError, match="Could not read golden set"):
        load_golden_set(tmp_path / "absent.yaml")


def test_an_empty_golden_set_is_rejected(tmp_path: Path):
    with pytest.raises(EvaluationError, match="contains no cases"):
        load_golden_set(_write(tmp_path, "cases: []\n"))


def test_unresolvable_documents_finds_a_mistyped_path():
    golden = GoldenSet.model_validate(
        {"cases": [{"id": "a", "question": "q", "relevant_documents": ["faq/typo.md"]}]}
    )
    assert unresolvable_documents(golden, {"faq/real.md"}) == {"faq/typo.md"}
    assert unresolvable_documents(golden, {"faq/typo.md"}) == set()


def test_document_key_prefers_the_corpus_relative_path():
    chunk = Chunk(
        id="c1",
        document_id="d1",
        ordinal=0,
        text="t",
        title="T",
        source_uri="file:///abs/path/faq/tax.md",
        metadata={"relative_path": "faq/tax.md"},
    )
    assert document_key(chunk) == "faq/tax.md"
    # Without one — a connector with no filesystem behind it — the URI is the key.
    assert document_key(
        Chunk(id="c", document_id="d", ordinal=0, text="t", title="T", source_uri="https://x/y")
    ) == "https://x/y"


# ---------------------------------------------------------------------------- runner


@pytest.fixture
def corpus() -> list[Document]:
    """A three-document corpus with `relative_path` set, as the loader would."""
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
        Document(
            id="doc-laptops",
            source_uri="file:///corpus/it/laptops.md",
            title="Laptop Guide",
            text="New joiners receive a laptop provisioned by the platform team.",
            metadata={"relative_path": "it/laptops.md"},
        ),
    ]


@pytest.fixture
async def retrieval(
    corpus: list[Document], embeddings: StubEmbeddingModel
) -> RetrievalPipeline:
    store = MemoryVectorStore(dimensions=EMBEDDING_DIMENSIONS)
    await IngestionPipeline(
        chunker=RecursiveChunker(ChunkerOptions(chunk_size=400, chunk_overlap=40)),
        embeddings=embeddings,
        store=store,
    ).ingest(InMemoryLoader(corpus).load())
    return RetrievalPipeline(
        store=store,
        embeddings=embeddings,
        reranker=NoopReranker(),
        settings=RetrievalSettings(rewrite_queries=False, top_k=3, candidates=10),
    )


def _settings() -> Settings:
    return Settings(retrieval=RetrievalSettings(rewrite_queries=False, top_k=3, candidates=10))


def _golden(**case: object) -> GoldenSet:
    return GoldenSet.model_validate({"cases": [{"question": "q", **case}]})


async def test_a_retrieval_run_scores_the_documents_it_found(retrieval: RetrievalPipeline):
    report = await Evaluator(retrieval, _settings()).run(
        _golden(id="leave", question="how many leave days", relevant_documents=["hr/leave.md"])
    )

    case = report.cases[0]
    assert case.scored
    assert "hr/leave.md" in case.retrieved_documents
    assert case.recall == pytest.approx(1.0)
    assert case.hit is True
    # The trace id is the bridge from a bad number back to the request that made it.
    assert case.trace_id


async def test_a_retrieval_only_run_reports_no_generation_metrics(retrieval: RetrievalPipeline):
    """Regression: `fact_match` used to read 1.0 for a run that generated nothing.

    `missing_facts` is empty when no answer was produced, so "nothing was missing"
    scored as a perfect result for work that never happened — a metric that is
    arithmetically correct and factually a lie.
    """
    report = await Evaluator(retrieval, _settings()).run(
        _golden(id="leave", question="leave days", relevant_documents=["hr/leave.md"],
                expected_facts=["twenty five"])
    )

    assert report.generation is False
    assert "recall@3" in report.summary
    for absent in ("fact_match", "citation_coverage", "groundedness", "abstention_accuracy"):
        assert absent not in report.summary


async def test_a_generation_run_scores_citations_against_what_was_retrieved(
    retrieval: RetrievalPipeline,
):
    answerer = Answerer(retrieval, StubChatModel("Twenty five days. [1]"), _settings().generation)
    report = await Evaluator(retrieval, _settings(), answerer=answerer).run(
        _golden(
            id="leave",
            question="how many leave days",
            relevant_documents=["hr/leave.md"],
            expected_facts=["twenty five"],
        )
    )

    case = report.cases[0]
    assert case.citations == 1
    # The stub cites chunk [1], which came from the retrieved set, so it is grounded.
    assert case.grounded_citations == 1
    assert case.missing_facts == []
    assert report.summary["citation_coverage"] == pytest.approx(1.0)
    assert report.summary["groundedness"] == pytest.approx(1.0)
    assert report.summary["fact_match"] == pytest.approx(1.0)
    assert report.summary["input_tokens_total"] > 0


async def test_a_missing_expected_fact_is_named_not_just_counted(retrieval: RetrievalPipeline):
    model = StubChatModel("Some number of days. [1]")
    answerer = Answerer(retrieval, model, _settings().generation)
    report = await Evaluator(retrieval, _settings(), answerer=answerer).run(
        _golden(
            id="leave",
            question="how many leave days",
            relevant_documents=["hr/leave.md"],
            expected_facts=["twenty five"],
        )
    )
    assert report.cases[0].missing_facts == ["twenty five"]
    assert report.summary["fact_match"] == 0.0


async def test_a_failing_provider_costs_one_case_not_the_whole_run(retrieval: RetrievalPipeline):
    answerer = Answerer(retrieval, FailingChatModel(), _settings().generation)
    golden = GoldenSet.model_validate(
        {
            "cases": [
                {"id": "a", "question": "leave days", "relevant_documents": ["hr/leave.md"]},
                {"id": "b", "question": "expense claims", "relevant_documents": ["hr/expenses.md"]},
            ]
        }
    )

    report = await Evaluator(retrieval, _settings(), answerer=answerer).run(golden)

    assert report.case_count == 2
    assert report.failed_count == 2
    assert all(case.error for case in report.cases)
    # Nothing was scored, so nothing is claimed. A zero here would read as a
    # retrieval collapse rather than as an unavailable provider.
    assert report.summary["cases_scored"] == 0.0


async def test_concurrency_does_not_change_the_result(retrieval: RetrievalPipeline):
    golden = GoldenSet.model_validate(
        {
            "cases": [
                {"id": "a", "question": "leave days", "relevant_documents": ["hr/leave.md"]},
                {"id": "b", "question": "expense claims", "relevant_documents": ["hr/expenses.md"]},
                {"id": "c", "question": "laptop", "relevant_documents": ["it/laptops.md"]},
            ]
        }
    )
    evaluator = Evaluator(retrieval, _settings())

    sequential = await evaluator.run(golden, concurrency=1)
    parallel = await evaluator.run(golden, concurrency=3)

    assert sequential.summary["recall@3"] == parallel.summary["recall@3"]
    assert sequential.summary["mrr"] == parallel.summary["mrr"]


async def test_the_configuration_that_produced_the_numbers_travels_with_them(
    retrieval: RetrievalPipeline,
):
    report = await Evaluator(retrieval, _settings()).run(
        _golden(id="a", question="leave", relevant_documents=["hr/leave.md"])
    )
    configuration = report.configuration
    assert configuration["chunking"]["strategy"]
    assert configuration["retrieval"]["top_k"] == 3
    assert "llm" in configuration and "embeddings" in configuration
    # No secrets, and nothing machine-specific: a result file is committed.
    assert "dsn" not in str(configuration).lower()


def test_summarise_excludes_failed_cases_from_quality_means():
    results = [
        CaseResult(id="ok", question="q", relevant_documents=["a"], recall=1.0, hit=True),
        CaseResult(
            id="broken", question="q", relevant_documents=["b"], error="ProviderError: down"
        ),
    ]
    summary = summarise(results, top_k=5, wall_seconds=1.0, generation=False)
    # One case scored, and it scored 1.0. Averaging the failure in as a zero would
    # have reported 0.5 and blamed retrieval for a provider outage.
    assert summary["cases_scored"] == 1.0
    assert summary["recall@5"] == pytest.approx(1.0)


def test_summarise_scores_abstention_only_over_abstention_cases():
    results = [
        CaseResult(id="abstain-hit", question="q", must_abstain=True, abstained=True),
        CaseResult(id="abstain-miss", question="q", must_abstain=True, answer="I think so"),
        CaseResult(id="normal", question="q", relevant_documents=["a"], recall=1.0, answer="yes"),
    ]
    summary = summarise(results, top_k=5, wall_seconds=1.0)
    assert summary["abstention_accuracy"] == pytest.approx(0.5)


def test_false_abstention_counts_all_successful_answerable_cases():
    results = [
        CaseResult(id="answered", question="q", relevant_documents=["a"], answer="yes"),
        CaseResult(id="refused", question="q", relevant_documents=["a"], abstained=True),
        CaseResult(id="required", question="q", must_abstain=True, abstained=True),
        CaseResult(id="failed", question="q", relevant_documents=["a"], error="timeout"),
    ]
    summary = summarise(results, top_k=5, wall_seconds=1.0)
    assert summary["false_abstention_rate"] == 0.5
    retrieval = summarise(results, top_k=5, wall_seconds=1.0, generation=False)
    assert "false_abstention_rate" not in retrieval


def test_false_abstention_is_absent_without_answerable_observations():
    for results in (
        [],
        [CaseResult(id="required", question="q", must_abstain=True, abstained=True)],
        [CaseResult(id="failed", question="q", relevant_documents=["a"], error="timeout")],
    ):
        assert "false_abstention_rate" not in summarise(results, top_k=5, wall_seconds=1.0)


def test_compare_only_diffs_metrics_present_in_both_runs():
    baseline = {"summary": {"recall@5": 0.8, "mrr": 0.7, "gone": 1.0}}
    current = {"summary": {"recall@5": 0.9, "mrr": 0.7, "new": 1.0}}

    deltas = {name: (before, after) for name, before, after in compare(baseline, current)}

    assert deltas == {"mrr": (0.7, 0.7), "recall@5": (0.8, 0.9)}
    # A metric that only one run reported is a change in the harness, not in
    # quality, and diffing it against zero would point in a made-up direction.
    assert "gone" not in deltas and "new" not in deltas


# ----------------------------------------------------------------------------- judge


@pytest.mark.parametrize(
    ("reply", "expected"),
    [
        ("SUPPORTED", True),
        ("UNSUPPORTED", False),
        ("  supported.  ", True),
        ("The answer is UNSUPPORTED.", False),
        ("Verdict: SUPPORTED", True),
        ("I am not sure", None),
    ],
)
def test_verdict_parsing_checks_unsupported_first_because_it_contains_supported(reply, expected):
    assert _parse_verdict(reply) is expected


async def test_a_judge_failure_records_no_verdict_rather_than_a_wrong_one(
    retrieval: RetrievalPipeline,
):
    """An unreachable judge must not be scored as either faithful or unfaithful.

    Defaulting to True would inflate the metric on exactly the runs where something
    was wrong; defaulting to False would blame the system under test for a failure
    in the instrument.
    """
    judge = FaithfulnessJudge(FailingChatModel())
    answerer = Answerer(retrieval, StubChatModel("An answer. [1]"), _settings().generation)

    report = await Evaluator(retrieval, _settings(), answerer=answerer, judge=judge).run(
        _golden(id="a", question="leave days", relevant_documents=["hr/leave.md"])
    )

    assert report.cases[0].faithful is None
    assert "faithfulness" not in report.summary


async def test_the_judge_sees_the_passages_the_answer_was_built_from(
    retrieval: RetrievalPipeline,
):
    model = StubChatModel("SUPPORTED")
    judge = FaithfulnessJudge(model)
    answering = StubChatModel("Twenty five days. [1]")
    answerer = Answerer(retrieval, answering, _settings().generation)

    report = await Evaluator(retrieval, _settings(), answerer=answerer, judge=judge).run(
        _golden(id="a", question="how many leave days", relevant_documents=["hr/leave.md"])
    )

    assert report.cases[0].faithful is True
    assert report.summary["faithfulness"] == pytest.approx(1.0)
    # The judge prompt must carry the retrieved text, or it is grading blind.
    assert "leave days" in model.requests[-1].messages[0].content


# ------------------------------------------------------------------------- nDCG


def test_ndcg_is_one_when_every_relevant_document_is_at_the_top():
    assert m.ndcg_at_k(["a", "b"], ["a", "b", "c"], 3) == pytest.approx(1.0)


def test_ndcg_separates_two_rankings_that_recall_and_mrr_cannot():
    """The reason this metric was added.

    Both rankings retrieve all three relevant documents (recall 1.0) and both put a
    relevant one first (MRR 1.0). Only nDCG distinguishes them, and the difference —
    two relevant passages pushed below a top_k boundary — is precisely the thing
    that changes what the model gets to read.
    """
    tight = m.ndcg_at_k(["a", "b", "c"], ["a", "b", "c", "x", "y"], 5)
    spread = m.ndcg_at_k(["a", "b", "c"], ["a", "x", "y", "b", "c"], 5)

    assert m.recall_at_k(["a", "b", "c"], ["a", "b", "c", "x", "y"], 5) == 1.0
    assert m.recall_at_k(["a", "b", "c"], ["a", "x", "y", "b", "c"], 5) == 1.0
    assert m.reciprocal_rank(["a", "b", "c"], ["a", "x", "y", "b", "c"]) == 1.0
    assert tight > spread


def test_ndcg_normalises_against_an_ideal_capped_at_k():
    """With four relevant documents and k=2, holding two of them is perfect.

    Normalising against all four would score the best achievable ranking at 0.5 and
    report a defect in retrieval that is really a property of k.
    """
    assert m.ndcg_at_k(["a", "b", "c", "d"], ["a", "b"], 2) == pytest.approx(1.0)


def test_ndcg_of_a_ranking_with_nothing_relevant_is_zero():
    assert m.ndcg_at_k(["a"], ["x", "y"], 2) == 0.0


def test_ndcg_discounts_by_position_not_by_count():
    """A single relevant document scores less the further down it appears."""
    first = m.ndcg_at_k(["a"], ["a", "x", "y"], 3)
    third = m.ndcg_at_k(["a"], ["x", "y", "a"], 3)
    assert first == pytest.approx(1.0)
    assert 0.0 < third < first


# ------------------------------------------------------- the shipped suites


def test_the_shipped_schema_suite_is_valid_and_declares_its_corpus():
    """`make eval` runs this file; a validation error here is a broken gate.

    Cheap to catch here rather than forty minutes into an evaluation run.
    """
    suite = load_golden_set(Path("evaluation/suites/schema.yaml"))

    assert suite.corpus == "docs/company/schema"
    assert len(suite.cases) > 40
    # Abstention cases are what stop the suite rewarding a model that answers
    # everything. Their absence would not fail any other assertion.
    assert any(case.must_abstain for case in suite.cases)


def test_the_preserved_faq_suite_still_loads():
    """The FAQ suite is kept runnable, not just kept on disk.

    Deleting evaluation cases because they no longer match the current corpus is
    the habit that makes a benchmark dishonest, so the promise that this suite is
    still usable is asserted rather than stated in a comment.
    """
    suite = load_golden_set(Path("evaluation/suites/faq.yaml"))

    assert suite.corpus == "docs/company/faq"
    assert len(suite.cases) == 86
    # Paths are relative to this suite's own corpus root, not to docs/company.
    assert not any(
        path.startswith("faq/") for case in suite.cases for path in case.relevant_documents
    )


def test_the_two_suites_are_scored_against_different_corpora():
    """Their numbers are not comparable, and the files say so themselves."""
    schema = load_golden_set(Path("evaluation/suites/schema.yaml"))
    faq = load_golden_set(Path("evaluation/suites/faq.yaml"))

    assert schema.corpus != faq.corpus
    assert not (schema.referenced_documents & faq.referenced_documents)
