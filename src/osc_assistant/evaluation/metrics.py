"""Retrieval and generation metrics.

Every function here is pure: same inputs, same output, no clock, no I/O, no model.
That is deliberate and it is the reason this module is separate from `runner`. A
metric that cannot be reproduced from a recorded run cannot be used to gate a pull
request, and a metric whose definition lives inside the code that also performs the
retrieval cannot be unit-tested against a worked example.

It also holds the small pure helpers that the two summarisers (`runner`,
`conversational`) and the two result-file readers (`gate`, `report`) all need —
`mean_of`, `ratio`, `numeric_summary`, `scored_records`. They live here because
every one of those four modules already imports this one, so a shared home costs no
new dependency edge, and because each had begun to exist in two copies that would
have drifted.

**Retrieval metrics are computed over documents, not chunks.** A golden set names
the documents that answer a question, because that is what a human curator can
actually verify. Chunk ids are derived from chunk boundaries, so the moment the
chunker or its size changes, every chunk id in the corpus changes — which would
invalidate the golden set on precisely the experiment the golden set exists to run
(`recursive` vs `langchain_recursive` vs `markdown`). Document identity survives
that change; chunk identity does not.

References for the definitions used here:
  - Manning, Raghavan & Schütze, *Introduction to Information Retrieval* (2008),
    ch. 8 — precision, recall and MRR over ranked results.
    https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html
  - Järvelin & Kekäläinen, "Cumulated gain-based evaluation of IR techniques",
    *ACM TOIS* 20(4), 2002 — the definition of DCG and its normalised form.
    https://doi.org/10.1145/582415.582418
"""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any


def dedupe(items: Iterable[str]) -> list[str]:
    """Collapse repeats while preserving rank order.

    Retrieval returns chunks and several may come from one document. For a
    document-level metric the second chunk of an already-seen document is not a
    second hit; it occupies no new rank. Without this, `precision@5` for a query
    answered perfectly by one document would read 0.2 rather than 1.0.
    """
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def recall_at_k(relevant: Iterable[str], ranked: Sequence[str], k: int) -> float:
    """Fraction of the relevant documents that appear in the top `k`.

    The headline retrieval number: it answers "could the model possibly have got
    this right?". Generation cannot recover from a passage that was never fetched,
    so recall bounds every downstream metric.
    """
    expected = set(relevant)
    if not expected:
        return 0.0
    retrieved = set(ranked[:k])
    return len(expected & retrieved) / len(expected)


def precision_at_k(relevant: Iterable[str], ranked: Sequence[str], k: int) -> float:
    """Fraction of the top `k` results that are relevant.

    Divided by `k` rather than by the number actually returned: returning three
    results where five were asked for is a real cost, because the unfilled slots
    were context the model could have had. Averaged over a golden set this is the
    conventional P@k.
    """
    if k <= 0:
        return 0.0
    expected = set(relevant)
    return sum(1 for item in ranked[:k] if item in expected) / k


def reciprocal_rank(relevant: Iterable[str], ranked: Sequence[str]) -> float:
    """1 / (rank of the first relevant result), or 0.0 if none is present.

    Averaged over a golden set this is MRR. It measures *ordering* where recall
    measures presence, which matters because the prompt budget is finite: a correct
    passage ranked eighth in a top-5 retrieval is a passage the model never saw.
    """
    expected = set(relevant)
    for position, item in enumerate(ranked, start=1):
        if item in expected:
            return 1.0 / position
    return 0.0


def hit_at_k(relevant: Iterable[str], ranked: Sequence[str], k: int) -> bool:
    """Whether any relevant document appears in the top `k`.

    The binary form of recall. Reported alongside it because a mean recall of 0.7
    is ambiguous — every question partly answered, or seven answered and three
    missed entirely — and those two corpora need completely different work.
    """
    return bool(set(relevant) & set(ranked[:k]))


def ndcg_at_k(relevant: Iterable[str], ranked: Sequence[str], k: int) -> float:
    """Normalised discounted cumulative gain over the top `k`.

    Recall asks whether the right documents were fetched and MRR asks where the
    *first* one landed. Neither distinguishes a query with three relevant documents
    at ranks 1, 2, 3 from the same three at 3, 4, 5 — both score recall 1.0, and
    both score MRR 1.0 and 0.33 respectively while saying nothing about the other
    two. nDCG is the standard answer: every relevant document contributes, and each
    contributes less the further down it sits.

    Binary relevance, because that is what a golden set of "these documents answer
    this question" actually asserts. A curator can verify that a document is
    relevant; asking them to grade it 0-3 would produce numbers with a precision the
    judgement behind them does not have. With binary gains the standard
    `(2^rel - 1)` and plain `rel` formulations coincide, so this is
    `sum(1/log2(i+1))` over the relevant hits, divided by the same sum for a perfect
    ranking.

    The ideal is capped at `k`: with four relevant documents and `k = 3` the best
    achievable ranking holds three, and normalising against four would make a
    perfect result score 0.79 and look like a defect in retrieval.
    """
    if k <= 0:
        return 0.0
    expected = set(relevant)
    if not expected:
        return 0.0

    gain = sum(
        1.0 / math.log2(position + 1)
        for position, item in enumerate(ranked[:k], start=1)
        if item in expected
    )
    ideal = sum(1.0 / math.log2(position + 1) for position in range(1, min(len(expected), k) + 1))
    return gain / ideal if ideal else 0.0


def mean_of[T](items: Sequence[T], extract: Callable[[T], float]) -> float:
    """Mean of `extract` over `items`, rounded to 4 places, 0.0 when there are none.

    Here rather than in a runner because both summarisers use it and both must round
    identically — a metric reported by the single-turn and the conversational report
    that differed in its last decimal would be a difference no reader could explain.
    It also satisfies this module's rule, which the runners do not: same inputs, same
    output, no clock, no I/O, no model.
    """
    return round(mean([extract(item) for item in items]), 4)


def mean(values: Sequence[float]) -> float:
    """Arithmetic mean, defined as 0.0 on an empty sequence.

    Returning 0.0 rather than raising keeps an empty or fully-filtered run
    reportable: an evaluation that produced no cases should print zeros and a case
    count of zero, not a traceback that hides which stage went wrong.
    """
    return sum(values) / len(values) if values else 0.0


def ratio(numerator: int, denominator: int) -> float:
    """`numerator / denominator`, rounded, and 0.0 rather than an error at zero.

    Used for the metrics computed over a *pool* rather than per case — citations are
    counted across every answer, not averaged per answer, because one answer with ten
    citations should weigh ten times an answer with one.
    """
    return round(numerator / denominator, 4) if denominator else 0.0


def numeric_summary(summary: Mapping[str, Any]) -> dict[str, float]:
    """The numeric entries of a result file's `summary`, as floats.

    Booleans are excluded explicitly: `bool` is a subclass of `int` in Python, so a
    flag would otherwise be compared as 0.0/1.0 and reported as a metric that
    regressed.
    """
    return {
        name: float(value)
        for name, value in summary.items()
        if isinstance(value, int | float) and not isinstance(value, bool)
    }


def scored_records(report: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """The per-case records of a result file that actually produced a measurement.

    Reads either report shape — the single-turn one calls the list `cases`, the
    conversational one calls it `turns` — and drops the entries carrying an `error`,
    because a provider timeout is not a score.
    """
    raw = report.get("cases") or report.get("turns") or []
    return [record for record in raw if isinstance(record, dict) and not record.get("error")]


def percentile(values: Sequence[float], fraction: float) -> float:
    """Nearest-rank percentile of `values`.

    Nearest-rank rather than interpolated: every value reported is a latency that
    was actually observed, which is what makes "p95 was 8.1s" a statement about a
    request that happened rather than about an average of two that did not.
    """
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, round(fraction * len(ordered) + 0.5) - 1))
    return ordered[index]
