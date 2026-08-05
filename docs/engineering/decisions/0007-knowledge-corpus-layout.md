# ADR 0007 — Corpus root is `docs/company/`; the FAQ is split by topic

**Status:** Accepted · **Date:** Phase 4

---

## Context

Two changes arrived together and interacted.

**Real company knowledge replaced the seed corpus.** The demonstration documents
(handbook policies, engineering runbooks) were removed and replaced with OSCP Wholesale
B2B product documentation: a 633-line advance FAQ, two scenario `.docx` files and two
scenario `.xlsx` workbooks. These are production knowledge assets, authoritative, and
not to be rewritten.

**An engineering knowledge base was required** — the document you are reading is part of
it. It has to live in the repository, and the obvious home was `docs/`.

That collision is the problem. The ingest root was `docs/`, and until now everything
under it was company content *by accident* rather than by design. Putting engineering
documentation there would make it retrievable: a merchant asking *"how does OSC handle
refunds?"* could be answered from an ADR about reciprocal rank fusion, with a citation,
confidently.

**The failure mode is invisible.** Retrieval would succeed, generation would be
grounded, the citation would be correct — and the answer would be from the wrong
universe. Nothing downstream catches it.

Separately, the FAQ arriving as one 633-line document created a measurement problem.
With a single-document corpus, `recall@k` is 1.0 for every answerable question,
`precision@k` is a constant and `mrr` is 1.0. The metrics exist, never move for an
actionable reason, and measure nothing.

## Decision

**Two decisions, taken together.**

**1. The corpus root is `docs/company/`.** The engineering knowledge base lives in
`docs/engineering/` and is never indexed.

```
docs/
├── company/      ← INGESTED. Authoritative company knowledge
└── engineering/  ← NOT ingested. This knowledge base
```

Named in exactly two places — `DOCS` in the `Makefile` and the `--corpus` default in
`cli/diagnose.py` — which must agree.

**2. The FAQ is split into 17 files, one per topic section.** All 89 questions preserved
verbatim; only structure changed. Each file gets an H1 naming its topic (which becomes
the citation title) and H2 per question.

Also decided in passing: `.xlsx` gets a parser (`openpyxl`, read-only, one block per
sheet, cells tab-joined per row), because two of the four scenario documents were
otherwise invisible to the assistant; and `./osc doctor` stops reporting dotfiles as
unparseable corpus, because training an operator to ignore a warning defeats the
warning.

## Alternatives considered

**Knowledge base outside `docs/`** — a top-level `knowledge-base/`. Avoids touching the
Makefile and splits documentation across two trees for no reason a reader would guess.

**An ingest-time exclusion list.** Keep everything under `docs/` and add an exclusion
setting to the loader. More code, more configuration, and a mistake *silently* leaks
internal documents into the answer index — the same invisible failure, now with a
config file between you and it. The directory boundary fails safe; an exclusion list
fails open.

**Keep the FAQ as one file.** 25 KB is not too large for the chunker, so this was
defensible on ingestion grounds alone. It was rejected on measurement grounds: it makes
document-level retrieval metrics degenerate, and the [evaluation
harness](0005-evaluation-framework.md) was the priority of this phase. It also produces
worse citations — *"Advance FAQ"* tells a user nothing; *"Tax Display"* tells them what
they are looking at.

**Split at question level** — 89 files, one per question. Rejected: retrieval would
almost always need several neighbouring questions, chunk-per-document would make overlap
meaningless, and a golden set naming one of 89 near-identical paths is harder to curate,
not easier.

**Frontmatter for metadata** on each file. Rejected: `parse_text` reads Markdown
verbatim, so frontmatter would be embedded and quotable as citation evidence. A citation
reading `tags: [pricing]` is worse than no citation.

**An index or README inside `docs/company/`.** It would be ingested and retrieved, and
it answers no question a user has.

## Consequences

**What it buys.**

- The engineering knowledge base can grow without any risk of polluting answers, and the
  boundary is a directory — the cheapest possible thing to reason about.
- Document-level retrieval metrics became meaningful, which is what makes the first
  baseline (`recall@5` 0.932 over 81 cases) a real number rather than a tautology.
- Citations name a topic.
- Chunk boundaries land inside a single subject instead of at the seam between
  *Draft Order* and *Free Gift*.
- Two scenario workbooks (82 of the index's 193 chunks) became retrievable.
- `./osc doctor` went from 8 ok / 1 warn to 9 ok / 0 warn — and the warning it no longer
  emits was noise, not a fix.

**What it costs.**

- **The corpus root is named in two places** and they must agree. A single setting would
  be better; it is currently a `Makefile` variable and a CLI default, and the comment in
  each points at the other.
- **The FAQ's original single-document form is gone.** The split is scripted and
  reversible, but anyone expecting `faq.md` will not find it.
- **A subtitle line (`*Advance FAQ*`) was added to each split file** to preserve the
  original document's identity across the split. It is the only text in the corpus that
  was not in the source, and it is provenance rather than content.
- **Two typos were corrected** while reformatting: a section heading read *"Tired
  Pricing guide"* and one answer began *"nce the country is selected"*. Both are
  transcription errors rather than content, and both are called out so they can be
  reverted if that reading is wrong.
- **`openpyxl` joins the `documents` extra.** A third parsing library, justified by two
  real documents in the live corpus.

**The constraint anyone adding content must know.** The service has no authentication,
so everything in `docs/company/` is readable by anyone who can reach it. Phase 1 was
scoped to company-wide-readable content specifically to defer per-document ACLs. Until
those land, **the directory is the access control boundary.**
