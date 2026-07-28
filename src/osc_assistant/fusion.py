"""Reciprocal Rank Fusion.

Combining a lexical and a vector ranking cannot be done by adding their scores:
a cosine similarity and a BM25 score are on unrelated scales, and normalising them
requires knowing each distribution up front. RRF sidesteps this by discarding the
scores entirely and combining ranks:

    score(d) = sum over rankings of  1 / (k + rank(d))

`k` damps the influence of the very top positions; 60 is the value from the
original paper and a sane default. The pgvector store implements the same formula
in SQL so both stores rank identically — this module is the reference and is what
the in-memory store and the tests use.
"""

from __future__ import annotations

from collections.abc import Sequence

from .types import MatchSource, ScoredChunk


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[ScoredChunk]], k: int = 60, limit: int | None = None
) -> list[ScoredChunk]:
    """Fuse several rankings of the same corpus into one.

    Args:
        rankings: Rankings to combine, each ordered most relevant first.
        k: Damping constant. Larger values flatten the weight given to top ranks.
        limit: Truncate the fused result to this many chunks.

    Returns:
        Chunks ordered by fused score, deduplicated by chunk id.
    """
    scores: dict[str, float] = {}
    chunks: dict[str, ScoredChunk] = {}

    for ranking in rankings:
        for position, scored in enumerate(ranking, start=1):
            chunk_id = scored.chunk.id
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (k + position)
            chunks.setdefault(chunk_id, scored)

    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    fused = [
        ScoredChunk(chunk=chunks[chunk_id].chunk, score=score, source=MatchSource.HYBRID)
        for chunk_id, score in ordered
    ]
    return fused[:limit] if limit is not None else fused
