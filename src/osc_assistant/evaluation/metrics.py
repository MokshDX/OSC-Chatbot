"""Retrieval and generation metrics.

Every function here is pure: same inputs, same output, no clock, no I/O, no model.
That is deliberate and it is the reason this module is separate from `runner`. A
metric that cannot be reproduced from a recorded run cannot be used to gate a pull
request, and a metric whose definition lives inside the code that also performs the
retrieval cannot be unit-tested against a worked example.

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
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence


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


def mean(values: Sequence[float]) -> float:
    """Arithmetic mean, defined as 0.0 on an empty sequence.

    Returning 0.0 rather than raising keeps an empty or fully-filtered run
    reportable: an evaluation that produced no cases should print zeros and a case
    count of zero, not a traceback that hides which stage went wrong.
    """
    return sum(values) / len(values) if values else 0.0


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
