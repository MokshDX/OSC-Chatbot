# ADR 0011 — The schema corpus is the authoritative knowledge source

**Status:** Accepted · **Date:** Phase 6 · **Supersedes the corpus scope of** [ADR 0007](0007-knowledge-corpus-layout.md)

---

## Context

ADR 0007 made `docs/company/` the corpus, holding the OSCP Wholesale B2B merchant FAQ
(17 topic files) and four scenario documents. Phase 6 added `docs/company/schema/`:
eleven module persistence-schema documents — metafield inventories, metaobject field
tables, Prisma models, sample payloads and ownership notes for the OSCP modules.

These two bodies of content describe the same product to different readers. The FAQ
answers *"why is my discount not showing on the cart page?"* for a merchant. The schema
documents answer *"which namespace and key holds the add-on tier pricing payload?"* for
an engineer.

The instruction for this phase was that the schema corpus is the authoritative
knowledge source, and that the assistant should no longer rely on the FAQ material as
its production corpus.

That is not a small edit. The 86-case golden set and both committed baselines were
built entirely against the FAQ. Making the schema corpus authoritative invalidates
every one of those numbers — not because they were wrong, but because they measure a
different system.

## Decision

**The production ingest root is `docs/company/schema/`.**

`corpus.root` (ADR 0010) is set to it in the default profile. The FAQ and scenario
documents remain on disk, unmodified, and are no longer indexed.

**The FAQ golden set is preserved as a second, runnable suite** rather than deleted or
migrated. `evaluation/suites/faq.yaml` keeps all 86 cases verbatim; only the
`relevant_documents` paths changed, because they are relative to a suite's own corpus
root and that root moved from `docs/company` to `docs/company/faq`. It runs in its own
workspace:

```
OSC_WORKSPACE_ID=faq ./osc ingest docs/company/faq
OSC_WORKSPACE_ID=faq ./osc eval --golden-set evaluation/suites/faq.yaml
```

**A new 61-case suite was written against the schema corpus**, plus an 18-case
conversational suite, and new baselines were measured for both.

Golden sets now declare the corpus they are scored against. That field is recorded
rather than enforced — the harness cannot know which corpus is indexed, only which
documents are — but it turns the commonest failure from "every case scored zero" into
a message naming the directory to ingest.

## Alternatives considered

**Index both, with the schema corpus merely added.** The lowest-risk option, and it
keeps the 86-case baseline comparable. Rejected because it does not do what was asked,
and because the two bodies overlap enough to be a real retrieval hazard: `faq/
add-on-tier-pricing.md` and `schema/schema.md` describe the same feature, and a
developer asking for the metafield key would compete against a merchant-facing answer
that does not contain one. The corpus boundary is exactly the mechanism for preventing
that, and it only works if it is drawn.

**Delete the FAQ suite.** Rejected outright. Deleting evaluation cases because they no
longer match the current corpus is the habit that makes a benchmark dishonest, and the
project's own rule says so. It is also the only suite over *prose* documents, which
makes it the natural control when a retrieval change is suspected of being specific to
the schema corpus's tables and JSON — a use that arrived immediately (ADR 0012).

**Migrate the FAQ cases onto the schema corpus.** Nonsensical on inspection: the
questions are merchant questions and the schema documents do not answer them. It would
have produced 86 abstention cases wearing the costume of a golden set.

## Consequences

**The recorded quality baseline resets.** The Phase 5 numbers (recall@5 0.932,
`fact_match` 0.90, `abstention_accuracy` 0.80) are FAQ-suite numbers and are not
comparable to the schema-suite numbers that replace them. `PROJECT_STATUS.md` reports
both, labelled, rather than quietly overwriting one with the other.

**The corpus got harder in a way the metrics show.** These documents are markdown
tables, JSON payloads and field inventories rather than prose. `abstention_accuracy`
fell to 0.667 and `fact_match` to 0.782 against the FAQ suite's 0.80 and 0.90. Some of
that is the corpus, some is that the schema suite's expected facts are stricter
(`registractionForm`, `cartTransformId` — exact identifiers rather than words like
"collection"). The two are not separable from these numbers alone, and claiming
otherwise would be a guess dressed as analysis.

**It immediately exposed a chunker mismatch.** `recursive` splits these documents
mid-table-row and mid-word; one chunk of `schema.md` began `ormId`. That was invisible
on prose and cost 7 points of recall here. See ADR 0012.

**Two corpora now share one database**, separated by `workspace_id`. That partition
key already existed on every table and is doing real work for the first time. The cost
is that running the FAQ suite requires remembering the workspace; the suite file's
header carries the command.

**The scenario documents (`.docx`, `.xlsx`) are now unindexed and untested by any
suite.** They were 82 of the old index's 193 chunks. The `.xlsx` and `.docx` parsers
are still exercised by the E2E suite against generated fixtures, so parser coverage is
intact, but no golden case scores retrieval over a spreadsheet any more. Recorded as
open debt rather than fixed here, because writing scenario cases is corpus work, not
engineering work.
