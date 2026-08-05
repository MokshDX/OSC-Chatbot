"""Measurement for the retrieval and generation stack.

The project's rule is that a retrieval change ships with a measured improvement.
This package is what makes that rule enforceable rather than aspirational: it runs
a curated set of real questions against the live pipelines and reports recall, MRR,
precision, citation groundedness, fact coverage, latency and token cost as numbers
that can be committed, diffed and gated on.

Four modules, one dependency direction — `dataset` and `metrics` know nothing about
the rest of the system, `judge` needs only a `ChatModel`, and `runner` composes all
three with the real pipelines:

    dataset.py   the golden set: schema, loading, validation
    metrics.py   pure scoring functions — no clock, no I/O, no model
    judge.py     optional LLM-as-judge faithfulness scoring
    runner.py    executes a golden set and produces a comparable report

Read `docs/engineering/architecture/evaluation.md` for how to use it, and
`docs/engineering/decisions/0005-evaluation-framework.md` for why it is shaped this
way.
"""

from __future__ import annotations

from .dataset import GoldenCase, GoldenSet, document_key, load_golden_set, unresolvable_documents
from .judge import FaithfulnessJudge
from .runner import CaseResult, EvaluationReport, Evaluator, compare, configuration_snapshot

__all__ = [
    "CaseResult",
    "EvaluationReport",
    "Evaluator",
    "FaithfulnessJudge",
    "GoldenCase",
    "GoldenSet",
    "compare",
    "configuration_snapshot",
    "document_key",
    "load_golden_set",
    "unresolvable_documents",
]
