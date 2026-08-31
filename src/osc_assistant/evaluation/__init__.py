"""Measurement for the retrieval, generation and conversation stack.

The project's rule is that a retrieval change ships with a measured improvement.
This package is what makes that rule enforceable rather than aspirational: it runs
curated sets of real questions against the live pipelines and reports recall, nDCG,
MRR, precision, citation groundedness, fact coverage, follow-up resolution, latency
and token cost as numbers that can be committed, diffed and gated on.

Seven modules, one dependency direction — `dataset` and `metrics` know nothing
about the rest of the system, `judge` needs only a `ChatModel`, and the runners
compose them with the real pipelines:

    dataset.py         the golden sets: schema, loading, validation
    metrics.py         pure scoring functions — no clock, no I/O, no model
    judge.py           optional LLM-as-judge faithfulness scoring
    runner.py          executes a single-turn golden set
    conversational.py  executes a multi-turn golden set, with cold controls
    gate.py            compares a run against a baseline and decides pass/fail
    report.py          renders a run as the human-readable quality report

Read `docs/engineering/architecture/evaluation.md` for how to use it,
`docs/engineering/architecture/evaluation-methodology.md` for what every metric
means and why it was chosen, and
`docs/engineering/decisions/0005-evaluation-framework.md` for why the framework is
shaped this way.
"""

from __future__ import annotations

from .conversational import (
    ConversationalEvaluator,
    ConversationalReport,
    TurnResult,
    summarise_conversation,
)
from .dataset import (
    ConversationalCase,
    ConversationalSet,
    ConversationalTurn,
    GoldenCase,
    GoldenSet,
    document_key,
    load_conversational_set,
    load_golden_set,
    unresolvable_documents,
)
from .judge import FaithfulnessJudge
from .runner import CaseResult, EvaluationReport, Evaluator, compare, configuration_snapshot

__all__ = [
    "CaseResult",
    "ConversationalCase",
    "ConversationalEvaluator",
    "ConversationalReport",
    "ConversationalSet",
    "ConversationalTurn",
    "EvaluationReport",
    "Evaluator",
    "FaithfulnessJudge",
    "GoldenCase",
    "GoldenSet",
    "TurnResult",
    "compare",
    "configuration_snapshot",
    "document_key",
    "load_conversational_set",
    "load_golden_set",
    "summarise_conversation",
    "unresolvable_documents",
]
