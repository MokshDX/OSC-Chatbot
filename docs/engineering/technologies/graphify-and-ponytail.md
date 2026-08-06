# Graphify and Ponytail

*Two development-time tools. Neither ships; both shape the codebase.*

---

# Graphify

## What it is

A tool that builds a persistent **knowledge graph** from a repository: nodes for
symbols, files and concepts; edges for the relationships between them; community
detection to group them; and query, path and explain operations over the result.

Output lives in `graphify-out/` — `graph.json`, `graph.html`, `GRAPH_REPORT.md`, and a
`wiki/` of generated per-node pages.

## Why OSC uses it

**Navigation without recursive reading.** The instruction to a new AI session is
explicit: *do not recursively read the repository; use Graphify as the primary
navigation mechanism and expand only the parts necessary for the current task.* For a
63-file codebase that is a large difference in how much context is spent before any work
starts.

**It answers structural questions the code cannot.** `graphify affected "X"` gives the
blast radius of a change. `graphify god-nodes` names what the system routes through.
Both are questions about the *shape* of the codebase, and reading files one at a time
answers them slowly and unreliably.

**It is a check on the architecture.** This is the underrated use. The graph is an
outside observer, and when it disagrees with the intended design it is usually right.

## What it has actually told us

Latest build (2026-08-06, incremental update after the logging work): **2124 nodes,
4952 edges, 105 communities**; 90% EXTRACTED / 10% INFERRED at 0.71 average
confidence.

Betweenness identifies `MemoryVectorStore` (72 edges), `Document` (70),
`StubEmbeddingModel` (69), `ComponentConfig` (65) and `Container` (60) as the
architectural hubs — configuration, the corpus record and the composition root are what
the system routes through, which matches the intended design.

**The finding worth recording:** an earlier build reported `StubEmbeddingModel` — a
*test double* — as the single most connected node in the codebase, ahead of every real
component. That is the graph's way of saying that the test suite, not production wiring,
was what exercised every seam. It has since been displaced by `MemoryVectorStore` and
`Document`. The doubles are still central, and should be: they are how the protocol
layer is proven. But real components now lead.

No architecture document would have surfaced that. It came from measuring the graph.

**The second finding: fewer nodes, more edges.** An earlier build was 2086/4572; the
2026-08-05 rebuild was 1981/4624 — density 2.19 → 2.33. The earlier build derived
document nodes structurally (heading stubs); the rebuild extracted them semantically,
replacing 429 stubs with 324 concepts carrying rationale, citations and hyperedges.
When a rebuild shrinks, check the edge count before assuming loss — `to_json`'s
shrink guard exists to force exactly that check.

**The third finding came from the corpus, not the code.** The graph surfaced that
`OSCP_B2B_Scenario_Document.docx` and `OSCP_B2B_Scenario_Document-1.docx` extract to
byte-identical text — 34 duplicate chunks in the production index. See ADR 0008.

## Caveats

- **Rebuilding needs the extras**: `uv tool install "graphifyy[office,sql]"`. Without
  `office`, the four scenario documents are reported as `skipped_sensitive` and
  silently dropped — that hid ~42% of the real corpus from the graph for two phases.
  Without `sql`, `migrations/001_init.sql` contributes nothing.
- **Dangling-endpoint edges are mostly not a defect.** A full rebuild's diagnostic
  counted 273; 245 were `imports`/`imports_from` pointing at third-party packages and
  stdlib (`pkg_pydantic`, `pathlib`, `typing`). The graph is declining to invent nodes
  for things outside the corpus, not losing them. Only ~17 were genuine unresolved
  cross-chunk references. The current build reports **0**, because `build_merge`
  resolves against the graph it is merging into rather than against one chunk.
- **Community labels are hand-written for every community in the current build**,
  hub-derived only when a rebuild changes the community set and a label has not yet
  been rewritten. `graphify label --backend=ollama` needs the `openai` package.
- **`docs/company/` is a corpus**, so a graph query can return an OSCP FAQ answer rather
  than code.

## Keeping it current

```bash
graphify update .                      # code-only changes; no API cost, no LLM
/graphify .                            # full rebuild incl. semantic doc extraction
graphify export wiki                   # refresh wiki/ after any rebuild
git rev-parse HEAD                     # compare with GRAPH_REPORT.md's build commit
```

`graphify update` is AST-only: it will **not** pick up changed prose in `docs/`. After
editing documentation, a full `/graphify .` is what refreshes the concept layer — and
`graphify export wiki` afterwards, or `wiki/` silently describes the previous graph.

`GRAPH_REPORT.md` records the commit it was built from, which is the freshness check.

## What is committed, and what is not

Only what a fresh clone needs to navigate without paying for a rebuild: `graph.json`,
`GRAPH_REPORT.md`, `wiki/`, `manifest.json`, the labels, `converted/`. Gitignored: the
content-addressed AST cache (~3 MB, rebuilt in seconds), the dated backup directories
graphify writes before each overwrite, `graph.html` (2 MB, regenerable), the per-run
scratch files, and `.graphify_python` / `.graphify_root` — which hold absolute paths to
whoever ran graphify last and were being committed, so a teammate's clone inherited a
path to a virtualenv that did not exist on their machine.

---

# Ponytail

## What it is

A development discipline, applied as an assistant mode, that forces the **laziest
solution that actually works**. Its central claim: the best code is the code never
written.

It runs as a ladder, stopping at the first rung that holds:

1. Does this need to exist at all? (YAGNI)
2. Is it already in this codebase?
3. Does the standard library do it?
4. Does a native platform feature cover it?
5. Does an already-installed dependency solve it?
6. Can it be one line?
7. Only then: the minimum code that works.

## Why OSC uses it

The project's own engineering handbook already says *avoid unnecessary abstractions*,
*prefer simple over clever*, *no overengineering*. Ponytail is that instruction made
operational — a checklist that runs before code is written rather than a principle
invoked during review, when the code already exists and deleting it feels like waste.

The failure mode it targets is specific to this kind of project. A RAG platform invites
speculative structure: a plugin system for retrievers, a rules engine for chunking, an
abstraction layer over the abstraction layer. Each looks reasonable in isolation and
none of it is needed.

## Where its influence is visible

| Decision | The lazy answer that won |
|---|---|
| Trace persistence | An append-only JSONL file, not a database table, a daemon, or a collector |
| Structured logging | A JSON formatter on stdlib `logging`, not a logging framework |
| Parser selection | `PARSERS: dict[str, Parser]`, not a registry — a parser takes no options |
| Metrics | Set arithmetic in one pure module, not RAGAS |
| CLI grouping | Three `--help` panels, not sub-command nesting |
| Faithfulness judge | One frozen prompt through the existing `ChatModel`, not a judging framework |

## Where it is deliberately *not* applied

The discipline has an explicit exclusion list, and it matters as much as the ladder:
**input validation at trust boundaries, error handling that prevents data loss, security
measures, and anything explicitly requested** are never simplified away.

That is why `settings.py`, `api/schemas.py` and `evaluation/dataset.py` all use full
Pydantic validation while `types.py` uses bare frozen dataclasses. The domain types are
constructed internally; the other three parse untrusted input. Lazy at the core, strict
at the edges.

## The `ponytail:` comment convention

A deliberate simplification that cuts a real corner with a known ceiling is marked in
the source, naming the ceiling and the upgrade path:

```python
# ponytail: whole-file read, seek-from-end if max_trace_file_bytes rises
```

This is the part that makes the discipline safe rather than merely fast. A shortcut with
a named upgrade path is a decision; an unmarked one is technical debt nobody remembers
taking on. `/ponytail-debt` harvests them into a ledger.

Currently one such marker exists, in `observability/store.py`.

---

## Related

- [../architecture/overview.md](../architecture/overview.md) — the structure Graphify maps
- [../decisions/README.md](../decisions/README.md) — where "should this exist?" gets recorded
