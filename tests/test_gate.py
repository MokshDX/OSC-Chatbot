"""Regression gate tests.

The gate is the only part of this system that can stop a change from shipping, so
the tests care most about the two ways a gate loses its authority: firing on noise
(which teaches people to re-run it until it passes) and staying silent on a real
regression (which is worse).

Reports are built as plain dicts here rather than by running an `Evaluator`. That
is deliberate — the gate's contract is "given two result files, decide" — and it is
what lets a case like "recall fell by exactly one case out of forty" be expressed
directly instead of engineered out of a live retrieval run.
"""

from __future__ import annotations

from typing import Any

from osc_assistant.evaluation.gate import (
    LATENCY_TOLERANCE_FRACTION,
    evaluate_gate,
)


def _report(
    summary: dict[str, float],
    cases: list[dict[str, Any]] | None = None,
    configuration: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "summary": summary,
        "cases": cases if cases is not None else _cases(40, hit=True),
        "configuration": configuration or {"llm": "ollama/qwen3:8b"},
    }


def _cases(count: int, *, hit: bool, missing: int = 0) -> list[dict[str, Any]]:
    """`count` retrieval cases, the last `missing` of which now fail."""
    return [
        {
            "id": f"case-{index}",
            "tags": ["retrieval"],
            "relevant_documents": ["a.md"],
            "recall": 0.0 if index >= count - missing else 1.0,
            "hit": hit and index < count - missing,
            "expected_facts": 1,
            "missing_facts": [],
            "answer": "an answer",
        }
        for index in range(count)
    ]


# ------------------------------------------------------------------- tolerances


def test_a_deterministic_metric_tolerates_less_than_one_case() -> None:
    """Retrieval is deterministic, so the tolerance is materiality, not noise.

    On 40 cases one case is worth 0.025. A drop of 0.02 is under that and passes.
    """
    gate = evaluate_gate(
        _report({"recall@5": 0.90}),
        _report({"recall@5": 0.88}),
    )
    assert gate.passed


def test_a_deterministic_metric_fails_when_more_than_one_case_is_lost() -> None:
    gate = evaluate_gate(
        _report({"recall@5": 0.90}, _cases(40, hit=True)),
        _report({"recall@5": 0.83}, _cases(40, hit=True, missing=3)),
    )

    assert not gate.passed
    finding = next(f for f in gate.findings if f.metric == "recall@5")
    assert finding.status == "regressed"
    assert finding.severity == "blocking"
    assert finding.tolerance == 1 / 40


def test_the_tolerance_rationale_explains_where_the_number_came_from() -> None:
    """A gate that says only "failed" is a gate people override."""
    gate = evaluate_gate(
        _report({"recall@5": 0.90}),
        _report({"recall@5": 0.70}),
    )
    finding = next(f for f in gate.findings if f.metric == "recall@5")
    assert "one case in 40" in finding.rationale
    assert "deterministic" in finding.rationale


def test_a_sampled_metric_tolerates_movement_inside_two_standard_errors() -> None:
    """Generation is sampled; a drop inside the interval is not a regression.

    At p=0.9 over 40 answered cases, 2*sqrt(.9*.1/40) is about 0.095. A drop of
    0.05 is well inside it and must not fail a build.
    """
    gate = evaluate_gate(
        _report({"fact_match": 0.90}),
        _report({"fact_match": 0.85}),
    )

    assert gate.passed
    finding = next(f for f in gate.findings if f.metric == "fact_match")
    assert finding.status == "pass"
    assert "standard error" in finding.rationale


def test_a_sampled_metric_fails_on_movement_outside_the_interval() -> None:
    gate = evaluate_gate(
        _report({"fact_match": 0.90}),
        _report({"fact_match": 0.60}),
    )
    assert not gate.passed


def test_a_smaller_sample_earns_a_wider_tolerance() -> None:
    """Six abstention cases are far noisier than forty fact cases.

    Giving both the same tolerance would necessarily make one of them wrong.
    """
    few = evaluate_gate(
        _report({"abstention_accuracy": 0.8}, _abstention_cases(6)),
        _report({"abstention_accuracy": 0.8}, _abstention_cases(6)),
    ).findings[0]
    many = evaluate_gate(
        _report({"abstention_accuracy": 0.8}, _abstention_cases(60)),
        _report({"abstention_accuracy": 0.8}, _abstention_cases(60)),
    ).findings[0]

    assert few.tolerance > many.tolerance


def _abstention_cases(count: int) -> list[dict[str, Any]]:
    return [
        {"id": f"abstain-{i}", "tags": ["abstention"], "must_abstain": True, "abstained": True}
        for i in range(count)
    ]


# ----------------------------------------------------------------------- latency


def test_latency_is_reported_but_never_blocking() -> None:
    """A laptop under load is not a quality regression."""
    gate = evaluate_gate(
        _report({"latency_p50_seconds": 10.0}),
        _report({"latency_p50_seconds": 30.0}),
    )

    finding = next(f for f in gate.findings if f.metric == "latency_p50_seconds")
    assert finding.status == "regressed"
    assert finding.severity == "warning"
    assert not finding.failed
    assert gate.passed


def test_latency_uses_a_relative_tolerance() -> None:
    gate = evaluate_gate(
        _report({"latency_p95_seconds": 8.0}),
        _report({"latency_p95_seconds": 8.0}),
    )
    finding = gate.findings[0]
    assert finding.tolerance == 8.0 * LATENCY_TOLERANCE_FRACTION


def test_a_faster_run_is_an_improvement_not_a_regression() -> None:
    """Direction matters: without it a latency win would be reported in red."""
    gate = evaluate_gate(
        _report({"latency_p50_seconds": 10.0}),
        _report({"latency_p50_seconds": 4.0}),
    )
    assert gate.findings[0].status == "improved"


def test_context_pollution_is_read_as_lower_is_better() -> None:
    """Named metrics whose good direction is down must not be reported backwards."""
    gate = evaluate_gate(
        _report({"context_pollution": 0.30}),
        _report({"context_pollution": 0.05}),
    )
    assert gate.findings[0].status == "improved"


# -------------------------------------------------------------------- trade-offs


def test_precision_bought_with_recall_is_blocked() -> None:
    """Returning fewer results raises precision and lowers recall.

    Each metric alone might look defensible; the pair is the tell, and a gate that
    checks thresholds one at a time cannot see it.
    """
    gate = evaluate_gate(
        _report({"precision@5": 0.20, "recall@5": 0.95}, _cases(40, hit=True)),
        _report({"precision@5": 0.60, "recall@5": 0.60}, _cases(40, hit=True, missing=14)),
    )

    assert not gate.passed
    assert any("precision@5" in note and "recall@5" in note for note in gate.trade_offs)


def test_abstaining_more_to_raise_abstention_accuracy_is_blocked() -> None:
    gate = evaluate_gate(
        _report({"abstention_accuracy": 0.60, "citation_coverage": 0.98}),
        _report({"abstention_accuracy": 1.00, "citation_coverage": 0.40}),
    )

    assert not gate.passed
    assert any("abstention_accuracy" in note for note in gate.trade_offs)


def test_an_honest_improvement_is_not_flagged_as_a_trade_off() -> None:
    """Both halves improving is the case that must stay quiet."""
    gate = evaluate_gate(
        _report({"precision@5": 0.20, "recall@5": 0.85}),
        _report({"precision@5": 0.40, "recall@5": 0.95}),
    )

    assert gate.passed
    assert gate.trade_offs == []
    assert {finding.status for finding in gate.findings} == {"improved"}


# ------------------------------------------------------------------- attribution


def test_a_regression_names_the_cases_that_changed() -> None:
    """Not every failing case — only the ones this change broke.

    A list of everything currently below 1.0 is the same on a good run and a bad
    one, and reading it teaches nothing about what moved.
    """
    gate = evaluate_gate(
        _report({"recall@5": 1.0}, _cases(40, hit=True)),
        _report({"recall@5": 0.85}, _cases(40, hit=True, missing=6)),
    )

    finding = next(f for f in gate.findings if f.metric == "recall@5")
    assert finding.affected_cases == [f"case-{index}" for index in range(34, 40)]
    assert finding.affected_categories == ["retrieval"]


def test_a_conversational_regression_names_the_turn_not_just_the_conversation() -> None:
    # Eight turns across two conversations, two of which break. Sized past the
    # one-turn tolerance on purpose: this test is about *attribution*, and at the
    # threshold it would be testing the threshold instead.
    turns = [
        {
            "case_id": f"convo-{case}",
            "ordinal": ordinal,
            "tags": ["reference-resolution"],
            "relevant_documents": ["a.md"],
            "recall": 1.0,
            "hit": True,
        }
        for case in ("a", "b")
        for ordinal in (1, 2, 3, 4)
    ]
    broken = [
        {**turn, "recall": 0.0, "hit": False}
        if (turn["case_id"], turn["ordinal"]) in {("convo-a", 3), ("convo-b", 2)}
        else dict(turn)
        for turn in turns
    ]

    gate = evaluate_gate(
        {"summary": {"multi_turn_recall@5": 1.0}, "turns": turns, "configuration": {}},
        {"summary": {"multi_turn_recall@5": 0.75}, "turns": broken, "configuration": {}},
    )

    finding = next(f for f in gate.findings if f.metric == "multi_turn_recall@5")
    assert finding.status == "regressed"
    # The turn, not the conversation it sat in: "convo-a regressed" sends someone
    # to read four questions to find the one that changed.
    assert finding.affected_cases == ["convo-a:turn3", "convo-b:turn2"]


# ------------------------------------------------------------------------ hygiene


def test_counts_and_totals_are_not_gated() -> None:
    """A suite that grew by ten cases must not fail for using more input tokens."""
    gate = evaluate_gate(
        _report({"cases_scored": 40.0, "input_tokens_total": 1000.0, "recall@5": 0.9}),
        _report({"cases_scored": 50.0, "input_tokens_total": 9000.0, "recall@5": 0.9}),
    )

    assert gate.passed
    assert {finding.metric for finding in gate.findings} == {"recall@5"}


def test_only_metrics_present_in_both_runs_are_compared() -> None:
    """A metric that appeared or vanished is a harness change, not a quality change."""
    gate = evaluate_gate(
        _report({"recall@5": 0.9, "removed_metric": 0.5}),
        _report({"recall@5": 0.9, "new_metric": 0.5}),
    )
    assert {finding.metric for finding in gate.findings} == {"recall@5"}


def test_configuration_differences_are_surfaced() -> None:
    """Comparing two runs must not silently compare two different systems."""
    gate = evaluate_gate(
        _report({"recall@5": 0.9}, configuration={"llm": "ollama/qwen3:8b", "reranker": "noop"}),
        _report(
            {"recall@5": 0.9},
            configuration={"llm": "ollama/qwen3:8b", "reranker": "cross_encoder"},
        ),
    )

    assert gate.configuration_differences == {"reranker": ("noop", "cross_encoder")}


def test_an_unchanged_run_passes_with_nothing_to_report() -> None:
    summary = {"recall@5": 0.9091, "mrr": 0.8545, "fact_match": 0.9}
    gate = evaluate_gate(_report(summary), _report(dict(summary)))

    assert gate.passed
    assert gate.regressions == []
    assert gate.improvements == []


def test_the_report_serialises_with_its_reasoning_intact() -> None:
    """CI reads the JSON; it must carry the same explanation the terminal shows."""
    gate = evaluate_gate(
        _report({"recall@5": 0.95}, _cases(40, hit=True)),
        _report({"recall@5": 0.70}, _cases(40, hit=True, missing=10)),
    )
    payload = gate.to_dict()

    assert payload["passed"] is False
    finding = next(f for f in payload["findings"] if f["metric"] == "recall@5")
    assert finding["status"] == "regressed"
    assert finding["rationale"]
    assert finding["tolerance"] == round(1 / 40, 4)
    assert finding["affected_cases"]
