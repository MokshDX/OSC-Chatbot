# ADR 0003 — Hybrid retrieval with RRF fused in SQL

**Status:** Accepted · **Date:** Phase 1

---

## Context

Retrieval bounds everything downstream: generation cannot recover from a passage that
was never fetched. The choice of retrieval method is therefore the highest-consequence
decision in the pipeline.

Two methods were available, with complementary blind spots.

**Vector search** embeds the query and finds chunks nearest by cosine similarity. It
handles paraphrase well — a merchant asking *"how do I stop customers seeing the full
price?"* finds a passage about cart page display without sharing a content word with it.
It handles **exact tokens badly**: acronyms, error strings, product codenames and
literal identifiers like `oscp-order-processing` have no meaningful semantic
neighbourhood, and an embedding model will place a fabricated identifier next to a real
one without hesitation.

**Keyword search** is exactly the reverse. It finds `oscp-order-processing` immediately
and misses every paraphrase.

An internal corpus is dense with both. OSC's is a product FAQ full of feature names,
Shopify admin paths and CSS selectors — *and* full of merchants asking in their own
words. Choosing one method means accepting a known failure mode on half the corpus.

The project's rules forbid premature optimisation, so the distinction matters:
**this is avoiding a known failure mode, not speculatively optimising a measured one.**

## Decision

**Hybrid retrieval by default**, fusing a pgvector cosine ranking and a PostgreSQL
`tsvector` ranking with **Reciprocal Rank Fusion**, computed **in SQL, in one round
trip**.

$$\text{RRF}(d) = \sum_{r} \frac{1}{k + \text{rank}_r(d)}, \quad k = 60$$

`fusion.py` holds the reference implementation in Python for the in-memory store, so
**both stores rank identically** — which is what makes the in-memory store a legitimate
test double for ranking behaviour and not only for plumbing.

`min_score` is applied to **first-stage** scores, before reranking. Reranking defaults
to `noop`.

> Cormack, Clarke & Buettcher, *Reciprocal Rank Fusion outperforms Condorcet and
> individual Rank Learning Methods*, SIGIR 2009.
> https://dl.acm.org/doi/10.1145/1571941.1572114

## Alternatives considered

**Vector search only.** Simpler, one index, and silently bad at exactly the queries a
support FAQ attracts — someone pasting an error string or a tag.

**Keyword search only.** Simpler still, and useless for the paraphrase case that is the
main reason to build a semantic assistant at all.

**Weighted score combination instead of RRF.** Requires normalising a cosine similarity
in [-1, 1] against an unbounded `ts_rank`, and then tuning a weight — a tuning parameter
that would have to be re-derived every time the embedding model changed. RRF merges by
*rank*, so there is nothing to calibrate.

**Fusion in application code, over two queries.** The obvious implementation, and it
costs two round trips and puts ranking logic in the layer that is hardest to test
against real data. This is also the specific reason LangChain's `PGVector` was not
adopted — it cannot fuse in SQL.

**Threshold after reranking** rather than before. Rejected after a real defect: a
cross-encoder returns an unbounded logit that is routinely *negative* for a genuinely
relevant passage, so applying the same configured `min_score` to its output discards the
entire result set the moment a reranker is enabled — presenting as *"the cross-encoder
is useless"* rather than as a misapplied threshold. `test_retrieval.py` holds the
regression.

**Cross-encoder reranking on by default.** Strictly more informative and strictly more
expensive. Off because its value on OSC's corpus has never been measured, and the
project's rule is that a retrieval change ships with a measured improvement.

## Consequences

**What it buys.**

- Measured on the current corpus: `recall@5` 0.932, `mrr` 0.860 over 81 golden cases
  (`evaluation/baselines/retrieval-default.json`).
- No tuning parameter between the two methods. Changing the embedding model does not
  require re-deriving a weight.
- One round trip, one datastore, one backup.
- Both stores rank identically, so ranking is testable without a database.

**What it costs.**

- **`rrf_k = 60` is unexplained by anything in this corpus.** It is the paper's value,
  adopted on authority. It has never been tuned here and probably should be, now that
  the harness exists.
- **Two indexes to maintain** — an HNSW index and a GIN index over a generated
  `tsvector` column. Ingestion writes both.
- **RRF discards score magnitude.** A document ranked first by a hair and one ranked
  first by a mile contribute identically. That is what makes it robust; it is also
  information thrown away.
- **`min_score` is nearly useless in hybrid mode**, because an RRF score has no
  intuitive scale. It defaults to 0.0 and is effectively inert.
- **The lexical side is English-configured.** A non-English corpus needs a different
  text search configuration, and nothing currently detects that.

**What was deferred.** Whether the cross-encoder reranker earns its cost, and whether
`candidates: 30` is the right working set for it. Both are now two-command experiments —
see [evaluation.md](../architecture/evaluation.md).
