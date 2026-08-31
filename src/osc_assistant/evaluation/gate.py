"""The regression gate: does this run still clear the trusted baseline?

`--fail-under recall@5=0.90` was the previous mechanism and it has two problems
that matter once anyone relies on it. The thresholds are typed on the command line,
so they are round numbers chosen by hand rather than anything derived from the
measurement; and a metric can pass while the property it trades against collapses,
because each threshold is checked alone.

This module replaces both with policies that are derived, and with explicit
trade-off guards.

## Where the tolerances come from

Nothing here is a round number someone liked. Every tolerance is computed from the
run it is applied to, and each kind of metric gets the treatment its noise
behaviour actually warrants.

**Retrieval metrics are deterministic.** Given one index and one configuration, the
same query returns the same ranking; there is no sampling to average over. Their
tolerance is therefore not a noise allowance but a *materiality* threshold, set to
`1 / n` — one case's worth of quality on a suite of `n` scored cases. The gate fires
when more than a single case has been lost. That unit is interpretable in the only
terms that matter when someone is looking at a red build: "this change broke two
questions."

**Generation metrics are not deterministic.** The model samples, so the same commit
scores differently twice. Their tolerance is two standard errors of a binomial
proportion at the baseline value, `2 * sqrt(p(1-p)/n)` — the conventional
approximate 95% interval. A drop inside it is not distinguishable from resampling,
and a gate that fires on noise is one people learn to re-run until it passes, which
is worse than having no gate. `n` is the number of cases that actually contributed
to that metric, not the suite size, because `abstention_accuracy` computed over six
abstention cases is a far noisier number than `fact_match` over forty.

  Standard error of a proportion: Brown, Cai & DasGupta, "Interval Estimation for a
  Binomial Proportion", *Statistical Science* 16(2), 2001.
  https://doi.org/10.1214/ss/1009213286

**Latency is heavy-tailed and machine-dependent**, so it gets a relative tolerance
(25%) and is a **warning, never blocking**. A developer's laptop compiling something
else while `make eval` runs is not a quality regression, and failing a build for it
would be a lie. It is still reported, because a genuine 3x is worth seeing.

## Trade-off guards

A metric that improves while its counterpart collapses is not an improvement, and
checking thresholds one at a time cannot see it. Three pairings are guarded, each
naming a real and easy way to game this suite:

  precision@k ↑ / recall@k ↓         return fewer results
  abstention_accuracy ↑ / citation_coverage ↓   abstain more often
  latency ↓ / recall@k ↓             retrieve fewer candidates

When both halves move beyond their own tolerances in opposite directions, the gate
reports a `trade_off` finding and blocks, regardless of how good the improving half
looks on its own.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

from .metrics import numeric_summary, scored_records

Direction = Literal["higher", "lower"]
Severity = Literal["blocking", "warning"]

# Relative tolerance for latency, and the reason it is not a noise estimate: p50 and
# p95 on a laptop move with whatever else the machine is doing, and no sample-size
# correction models that.
LATENCY_TOLERANCE_FRACTION = 0.25

# Floor on any derived tolerance. Below this the gate is reacting to the fourth
# decimal place of a rounded summary value, which is arithmetic, not quality.
MINIMUM_TOLERANCE = 0.005

_LOWER_IS_BETTER = re.compile(r"latency|tokens|pollution")


@dataclass(frozen=True, slots=True)
class Finding:
    """One metric's verdict, with everything needed to act on it.

    Carries the numbers *and* the reasoning. A gate that prints "recall@5 failed" is
    a gate someone overrides; one that prints the tolerance it used, where that
    tolerance came from, and which four cases regressed, is one they fix.
    """

    metric: str
    baseline: float
    current: float
    tolerance: float
    direction: Direction
    severity: Severity
    status: Literal["pass", "regressed", "improved"]
    rationale: str
    affected_cases: list[str] = field(default_factory=list)
    affected_categories: list[str] = field(default_factory=list)

    @property
    def delta(self) -> float:
        return self.current - self.baseline

    @property
    def failed(self) -> bool:
        return self.status == "regressed" and self.severity == "blocking"

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric": self.metric,
            "baseline": round(self.baseline, 4),
            "current": round(self.current, 4),
            "delta": round(self.delta, 4),
            "tolerance": round(self.tolerance, 4),
            "direction": self.direction,
            "severity": self.severity,
            "status": self.status,
            "rationale": self.rationale,
            "affected_cases": self.affected_cases,
            "affected_categories": self.affected_categories,
        }


@dataclass(frozen=True, slots=True)
class GateReport:
    """The gate's decision and the evidence for it."""

    passed: bool
    findings: list[Finding]
    trade_offs: list[str]
    baseline_name: str
    configuration_differences: dict[str, tuple[Any, Any]] = field(default_factory=dict)

    @property
    def regressions(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.status == "regressed"]

    @property
    def improvements(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.status == "improved"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "baseline": self.baseline_name,
            "findings": [finding.to_dict() for finding in self.findings],
            "trade_offs": self.trade_offs,
            "configuration_differences": {
                key: {"baseline": before, "current": after}
                for key, (before, after) in self.configuration_differences.items()
            },
        }


@dataclass(frozen=True, slots=True)
class _CaseOutcome:
    """The comparable skeleton of one case or turn, from either report shape."""

    id: str
    tags: list[str]
    hit: bool
    recall: float
    answered_correctly: bool


# Metrics that are deterministic given an index and a configuration, and therefore
# get the materiality tolerance rather than a noise allowance.
_DETERMINISTIC = re.compile(r"recall@|precision@|ndcg@|hit_rate@|mrr|follow_up|context_")

# Metrics deliberately excluded from gating. Counts and totals describe the size of
# the run, not its quality, and a suite that grew by ten cases would otherwise fail
# for having more input tokens.
_NOT_QUALITY = frozenset(
    {
        "cases_scored",
        "turns_scored",
        "input_tokens_total",
        "output_tokens_total",
        "throughput_per_second",
    }
)

# (improving metric, metric it must not be bought with). See the module docstring.
_TRADE_OFFS: tuple[tuple[str, str, str], ...] = (
    ("precision@", "recall@", "returning fewer results raises precision and lowers recall"),
    (
        "abstention_accuracy",
        "citation_coverage",
        "abstaining more often raises abstention accuracy and lowers answer coverage",
    ),
    (
        "latency_p50_seconds",
        "recall@",
        "retrieving fewer candidates lowers latency and lowers recall",
    ),
)


def evaluate_gate(
    baseline: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    baseline_name: str = "baseline",
) -> GateReport:
    """Compare `current` against `baseline` and decide whether it may ship.

    Both arguments are the `to_dict()` form of a report — single-turn or
    conversational; the shapes differ only in whether the per-case list is called
    `cases` or `turns`, and both are handled.
    """
    before = numeric_summary(baseline.get("summary", {}))
    after = numeric_summary(current.get("summary", {}))
    shared = sorted(set(before) & set(after) - _NOT_QUALITY)

    baseline_cases = _outcomes(baseline)
    current_cases = _outcomes(current)

    findings = [
        _judge_metric(
            name,
            before[name],
            after[name],
            sample_size=_sample_size(name, current),
            baseline_cases=baseline_cases,
            current_cases=current_cases,
        )
        for name in shared
    ]
    trade_offs = _detect_trade_offs(findings)

    return GateReport(
        passed=not any(finding.failed for finding in findings) and not trade_offs,
        findings=findings,
        trade_offs=trade_offs,
        baseline_name=baseline_name,
        configuration_differences=_configuration_differences(baseline, current),
    )


def _judge_metric(
    name: str,
    baseline: float,
    current: float,
    *,
    sample_size: int,
    baseline_cases: Mapping[str, _CaseOutcome],
    current_cases: Mapping[str, _CaseOutcome],
) -> Finding:
    direction: Direction = "lower" if _LOWER_IS_BETTER.search(name) else "higher"
    tolerance, severity, rationale = _tolerance_for(name, baseline, sample_size)

    movement = current - baseline
    regressed = (movement < -tolerance) if direction == "higher" else (movement > tolerance)
    improved = (movement > tolerance) if direction == "higher" else (movement < -tolerance)
    status: Literal["pass", "regressed", "improved"] = (
        "regressed" if regressed else "improved" if improved else "pass"
    )

    cases, categories = (
        _regressed_cases(baseline_cases, current_cases) if regressed else ([], [])
    )
    return Finding(
        metric=name,
        baseline=baseline,
        current=current,
        tolerance=tolerance,
        direction=direction,
        severity=severity,
        status=status,
        rationale=rationale,
        affected_cases=cases,
        affected_categories=categories,
    )


def _tolerance_for(name: str, baseline: float, sample_size: int) -> tuple[float, Severity, str]:
    """Derive this metric's tolerance, its severity, and the sentence explaining both."""
    if "latency" in name:
        return (
            abs(baseline) * LATENCY_TOLERANCE_FRACTION,
            "warning",
            f"{LATENCY_TOLERANCE_FRACTION:.0%} of the baseline; latency is "
            f"machine-dependent and heavy-tailed, so it is reported and never blocking",
        )

    if _DETERMINISTIC.search(name):
        # Deterministic given the index: no noise to absorb, so the tolerance is the
        # smallest change worth a red build — one case.
        tolerance = max(1.0 / sample_size, MINIMUM_TOLERANCE) if sample_size else MINIMUM_TOLERANCE
        return (
            tolerance,
            "blocking",
            f"one case in {sample_size}; retrieval is deterministic for a fixed "
            f"index, so any movement is a real change and the only question is "
            f"whether it is material",
        )

    standard_error = (
        math.sqrt(max(baseline * (1.0 - baseline), 0.0) / sample_size) if sample_size else 0.0
    )
    return (
        max(2.0 * standard_error, MINIMUM_TOLERANCE),
        "blocking",
        f"two standard errors at p={baseline:.3g}, n={sample_size}; generation is "
        f"sampled, and a drop inside this interval is indistinguishable from "
        f"re-running the same commit",
    )


def _sample_size(name: str, report: Mapping[str, Any]) -> int:
    """How many cases actually contributed to `name`.

    Using the suite size for everything would understate the noise on the metrics
    computed over a subset — `abstention_accuracy` over six abstention cases is far
    noisier than `fact_match` over forty, and giving them the same tolerance would
    make one of the two wrong.
    """
    records = scored_records(report)
    if not records:
        return 0

    if "abstention" in name:
        return sum(1 for record in records if record.get("must_abstain"))
    if "fact_match" in name:
        return sum(1 for record in records if record.get("expected_facts"))
    if "citation" in name or "groundedness" in name or "faithful" in name:
        return sum(
            1 for record in records if not record.get("abstained") and record.get("answer")
        )
    if "follow_up" in name:
        return sum(1 for record in records if record.get("requires_context"))
    if "context_" in name:
        return sum(1 for record in records if record.get("context_switch"))
    if name.startswith(("recall@", "precision@", "ndcg@", "hit_rate@", "mrr", "multi_turn_")):
        return sum(1 for record in records if record.get("relevant_documents"))
    return len(records)



def _outcomes(report: Mapping[str, Any]) -> dict[str, _CaseOutcome]:
    """Reduce per-case records to what a regression diff needs.

    Keyed by case id, or by `case_id:ordinal` for a conversational turn, so a
    regression can name the exact turn rather than the conversation it sat in.
    """
    outcomes: dict[str, _CaseOutcome] = {}
    for record in scored_records(report):
        identifier = (
            f"{record['case_id']}:turn{record['ordinal']}"
            if "ordinal" in record
            else str(record.get("id", ""))
        )
        if not identifier:
            continue
        must_abstain = bool(record.get("must_abstain"))
        abstained = bool(record.get("abstained"))
        outcomes[identifier] = _CaseOutcome(
            id=identifier,
            tags=[str(tag) for tag in record.get("tags", [])],
            hit=bool(record.get("hit")),
            recall=float(record.get("recall", 0.0)),
            answered_correctly=(
                abstained if must_abstain else not record.get("missing_facts", [])
            ),
        )
    return outcomes


def _regressed_cases(
    baseline: Mapping[str, _CaseOutcome], current: Mapping[str, _CaseOutcome]
) -> tuple[list[str], list[str]]:
    """Cases that were right before and are wrong now, and the categories they span.

    Deliberately not "every case that scores below one" — that list is the same on
    a good run and a bad one, and reading it teaches nothing about what this change
    did. Only cases that *moved* are the change's responsibility.
    """
    regressed = sorted(
        identifier
        for identifier, was in baseline.items()
        if (now := current.get(identifier)) is not None
        and (
            (was.hit and not now.hit)
            or (now.recall < was.recall)
            or (was.answered_correctly and not now.answered_correctly)
        )
    )
    categories = sorted(
        {tag for identifier in regressed for tag in current[identifier].tags}
    )
    return regressed, categories


def _detect_trade_offs(findings: Sequence[Finding]) -> list[str]:
    """Improvements that were bought with a regression elsewhere."""
    by_name = {finding.metric: finding for finding in findings}

    def _match(prefix: str) -> list[Finding]:
        return [
            finding
            for name, finding in by_name.items()
            if name.startswith(prefix) or name == prefix
        ]

    detected: list[str] = []
    for gained, lost, explanation in _TRADE_OFFS:
        improvements = [finding for finding in _match(gained) if finding.status == "improved"]
        regressions = [finding for finding in _match(lost) if finding.status == "regressed"]
        for improvement in improvements:
            for regression in regressions:
                detected.append(
                    f"{improvement.metric} improved {improvement.delta:+.4g} while "
                    f"{regression.metric} regressed {regression.delta:+.4g} — "
                    f"{explanation}"
                )
    return detected


def _configuration_differences(
    baseline: Mapping[str, Any], current: Mapping[str, Any]
) -> dict[str, tuple[Any, Any]]:
    """Configuration keys that differ, so a comparison cannot silently span two systems."""
    before = baseline.get("configuration", {})
    after = current.get("configuration", {})
    return {
        key: (before.get(key), value)
        for key, value in after.items()
        if before.get(key) != value
    }

