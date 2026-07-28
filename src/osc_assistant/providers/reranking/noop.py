"""Pass-through reranker: the default.

Reranking is a real accuracy gain but costs latency and adds a model dependency.
The default is therefore no reranking, so it can be switched on once the
evaluation harness can prove the delta on OSC's own golden set rather than on a
public benchmark.

This is a null object rather than an `Optional[Reranker]` everywhere: it removes a
branch from the retrieval pipeline and makes "reranking off" an explicit,
configurable choice that shows up in logs like any other component.
"""

from __future__ import annotations

from collections.abc import Sequence

from ...protocols import Reranker
from ...registries import reranker_registry
from ...registry import ComponentConfig
from ...types import ScoredChunk


class NoopReranker:
    """Truncates the candidate list without reordering it."""

    @property
    def model_id(self) -> str:
        return "noop"

    async def rerank(
        self, query: str, candidates: Sequence[ScoredChunk], top_k: int
    ) -> list[ScoredChunk]:
        return list(candidates[:top_k])


@reranker_registry.register("noop")
@reranker_registry.register("none")
def _build(config: ComponentConfig) -> Reranker:
    return NoopReranker()
