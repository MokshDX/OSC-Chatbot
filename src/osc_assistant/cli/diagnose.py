"""Diagnostics and inspection: understanding the system without reading its source.

The commands here answer the questions that previously required opening `psql`, a
Python REPL or the codebase itself:

    doctor      is every configured component actually reachable?
    config      what settings am I really running, and where did they come from?
    providers   what can I switch to, and is it installed?
    status      what is in the index?
    documents   which documents are indexed, and how did each one chunk?
    document    everything about one document, including its chunks
    chunk       the exact text a citation points at
    trace       what a running service did on a recent request

The organising principle is that a question an operator asks weekly should be a
command, not a procedure. Each one is read-only.
"""

from __future__ import annotations

import json
import os
import platform
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any

import typer
import yaml

from ..container import Container
from ..ingestion.parsers import SUPPORTED_EXTENSIONS
from ..observability import (
    Trace,
    active_trace_store,
    render_summary,
    render_waterfall,
    trace_from_dict,
)
from ..protocols import StoreInspector
from ..registries import (
    chunker_registry,
    embedding_registry,
    llm_registry,
    reranker_registry,
    vector_store_registry,
)
from ..registry import Registry
from ..settings import PROFILE_ENV_VAR, Settings
from ..types import ChatRequest, DocumentSummary, Message, Role
from ._shared import (
    LOOKING,
    UNDERSTANDING,
    JsonOption,
    ProfileOption,
    VerboseOption,
    console,
    fail,
    load,
    run,
    table,
)

app = typer.Typer()

_SECRET_HINTS = ("key", "token", "secret", "password", "dsn", "credential")


# ------------------------------------------------------------------------ doctor


@dataclass(slots=True)
class Check:
    """One diagnostic result.

    `status` is deliberately three-valued. A warning is a real state — a reachable
    system with an empty index, say — and collapsing it into pass or fail either
    hides a problem or blocks a pipeline over something that is merely worth
    knowing.
    """

    name: str
    status: str  # ok | warn | fail
    detail: str

    @property
    def marker(self) -> str:
        return {"ok": "[green]ok[/green]", "warn": "[yellow]warn[/yellow]"}.get(
            self.status, "[red]fail[/red]"
        )


@app.command(rich_help_panel=UNDERSTANDING)
def doctor(
    profile: ProfileOption = None,
    probe: Annotated[
        bool,
        typer.Option(help="Make one real call to the chat and embedding models."),
    ] = True,
    corpus: Annotated[
        Path | None, typer.Option(help="Corpus directory to check for readable files.")
    ] = Path("docs/company"),
    verbose: VerboseOption = False,
) -> None:
    """Check that every configured component is reachable and consistent.

    Runs the same construction path the service does, so a failure here is a
    failure the service would hit at startup — but reported as one line naming the
    component rather than as a stack trace during a request.

    Live calls are made by default. Construction alone would pass with Ollama
    stopped, the model unpulled or the credential expired, which are the three most
    common causes of "it worked yesterday".
    """
    settings = load(profile, verbose=verbose)
    checks = run(_run_checks(settings, probe=probe, corpus=corpus))

    report = table("check", "status", "detail")
    for check in checks:
        report.add_row(check.name, check.marker, check.detail)
    console.print(report)

    failures = [check for check in checks if check.status == "fail"]
    warnings = [check for check in checks if check.status == "warn"]
    console.print(
        f"\n{len(checks) - len(failures) - len(warnings)} ok, "
        f"{len(warnings)} warn, {len(failures)} fail"
    )
    if failures:
        raise typer.Exit(code=1)


async def _run_checks(settings: Settings, *, probe: bool, corpus: Path | None) -> list[Check]:
    checks = [
        Check(
            "settings",
            "ok",
            f"profile={os.environ.get(PROFILE_ENV_VAR, 'config/default.yaml')} "
            f"environment={settings.environment} workspace={settings.workspace_id}",
        ),
        _check_langchain(),
    ]

    container = Container(settings)

    embeddings = None
    try:
        embeddings = container.embeddings
        detail = f"{settings.embeddings.provider}/{embeddings.model_id} {embeddings.dimensions}d"
        if probe:
            started = time.perf_counter()
            vector = await embeddings.embed_query("health check")
            elapsed = (time.perf_counter() - started) * 1000
            detail += f" · live {len(vector)}d in {elapsed:.0f}ms"
        checks.append(Check("embeddings", "ok", detail))
    except Exception as exc:
        checks.append(Check("embeddings", "fail", f"{type(exc).__name__}: {exc}"))

    # Every later check needs the store, and the store needs the embedding width,
    # so a failed embedding check makes the rest unreportable rather than failing.
    if embeddings is None:
        checks.append(Check("vector_store", "fail", "skipped: embeddings unavailable"))
        checks.append(Check("index", "fail", "skipped: embeddings unavailable"))
    else:
        checks.extend(await _check_store(container, settings))

    checks.append(_check_chunker(container, settings))
    checks.append(_check_reranker(container, settings))
    checks.append(await _check_llm(container, settings, probe=probe))
    if corpus is not None:
        checks.append(_check_corpus(corpus))

    await container.shutdown()
    return checks


async def _check_store(container: Container, settings: Settings) -> list[Check]:
    try:
        store = container.vector_store
        # setup() applies migrations and asserts the stored vector width matches the
        # active embedding model — the check most worth running before a sync.
        await store.setup()
    except Exception as exc:
        return [
            Check("vector_store", "fail", f"{type(exc).__name__}: {exc}"),
            Check("index", "fail", "skipped: store unavailable"),
        ]

    checks = [
        Check(
            "vector_store",
            "ok",
            f"{settings.vector_store.provider} · {store.dimensions}d · migrations applied",
        )
    ]

    if not isinstance(store, StoreInspector):
        checks.append(Check("index", "warn", "store offers no inspection interface"))
        return checks

    try:
        stats = await store.statistics()
    except Exception as exc:
        checks.append(Check("index", "fail", f"{type(exc).__name__}: {exc}"))
        return checks

    if stats.documents == 0:
        checks.append(
            Check("index", "warn", "empty — run `osc-assistant ingest ./docs/company`")
        )
    elif stats.chunks == 0:
        checks.append(
            Check(
                "index",
                "fail",
                f"{stats.documents} documents but 0 chunks — nothing retrievable",
            )
        )
    else:
        checks.append(
            Check(
                "index",
                "ok",
                f"{stats.documents} documents · {stats.chunks} chunks · "
                f"median {stats.chunk_chars_p50} chars",
            )
        )

    # A corpus embedded by more than one model is the signature of an embedding
    # change without a re-index: the retrieval query only ever matches one of them,
    # so the rest of the corpus is silently unreachable.
    if len(stats.embedding_models) > 1:
        checks.append(
            Check(
                "embedding_consistency",
                "fail",
                f"chunks embedded by {len(stats.embedding_models)} models "
                f"({', '.join(stats.embedding_models)}); re-index with --reindex",
            )
        )
    return checks


def _check_chunker(container: Container, settings: Settings) -> Check:
    try:
        _ = container.chunker
    except Exception as exc:
        return Check("chunker", "fail", f"{type(exc).__name__}: {exc}")
    return Check(
        "chunker",
        "ok",
        f"{settings.chunking.strategy} · size={settings.chunking.chunk_size} "
        f"overlap={settings.chunking.chunk_overlap}",
    )


def _check_reranker(container: Container, settings: Settings) -> Check:
    try:
        reranker = container.reranker
    except Exception as exc:
        return Check("reranker", "fail", f"{type(exc).__name__}: {exc}")
    return Check("reranker", "ok", f"{settings.reranker.provider} · {reranker.model_id}")


async def _check_llm(container: Container, settings: Settings, *, probe: bool) -> Check:
    try:
        model = container.llm
    except Exception as exc:
        return Check("llm", "fail", f"{type(exc).__name__}: {exc}")

    detail = (
        f"{settings.llm.provider}/{model.model_id} · "
        f"native_citations={model.supports_citations}"
    )
    if not probe:
        return Check("llm", "ok", detail)

    try:
        started = time.perf_counter()
        response = await model.complete(
            ChatRequest(
                messages=[Message(role=Role.USER, content="Reply with the single word: ok")],
                max_tokens=16,
            )
        )
        elapsed = (time.perf_counter() - started) * 1000
    except Exception as exc:
        return Check("llm", "fail", f"{detail} · live call failed: {exc}")
    return Check("llm", "ok", f"{detail} · live {len(response.text)} chars in {elapsed:.0f}ms")


def _check_corpus(corpus: Path) -> Check:
    if not corpus.exists():
        return Check("corpus", "warn", f"{corpus} does not exist")

    supported = {extension.lower() for extension in SUPPORTED_EXTENSIONS}
    readable = 0
    ignored: dict[str, int] = {}
    for path in corpus.rglob("*"):
        # Dotfiles are never corpus content — `.DS_Store` and `.gitkeep` are the
        # ones actually seen — and reporting them as unparseable trains an operator
        # to ignore the one warning that names a format they do care about.
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix.lower() in supported:
            readable += 1
        else:
            suffix = path.suffix.lower() or "(none)"
            ignored[suffix] = ignored.get(suffix, 0) + 1

    detail = f"{corpus}: {readable} ingestible files"
    if ignored:
        # Worth surfacing: a directory of .pptx that nothing will ever index looks
        # identical to an empty corpus from the ingestion report alone.
        listed = ", ".join(
            f"{count} {extension}" for extension, count in sorted(ignored.items())
        )
        return Check("corpus", "warn", f"{detail}; no parser for {listed}")
    if readable == 0:
        return Check("corpus", "warn", f"{detail} — nothing to ingest")
    return Check("corpus", "ok", detail)


def _check_langchain() -> Check:
    """Report the LangChain versions in play. Both are core dependencies."""
    try:
        from importlib.metadata import version

        return Check(
            "langchain",
            "ok",
            f"core {version('langchain-core')} · "
            f"text-splitters {version('langchain-text-splitters')}",
        )
    except Exception as exc:
        return Check("langchain", "fail", f"not installed: {exc}")


# ------------------------------------------------------------------------ config


@app.command(rich_help_panel=UNDERSTANDING)
def config(
    profile: ProfileOption = None,
    as_json: JsonOption = False,
    show_secrets: Annotated[
        bool, typer.Option(help="Print credentials and DSNs in full.")
    ] = False,
) -> None:
    """Print the fully resolved configuration and where it came from.

    Configuration is layered — environment over `.env` over YAML profile — so the
    file on disk is not what the process is running. This prints what was actually
    resolved, alongside the `OSC_*` variables that participated, which is the fast
    answer to "production is using the wrong model".
    """
    settings = load(profile)
    payload = settings.model_dump(mode="json")
    if not show_secrets:
        payload = _redact(payload)

    overrides = sorted(name for name in os.environ if name.startswith("OSC_"))
    profile_path = os.environ.get(PROFILE_ENV_VAR, "config/default.yaml")

    if as_json:
        console.print_json(
            json.dumps(
                {
                    "profile": profile_path,
                    "environment_overrides": overrides,
                    "settings": payload,
                }
            )
        )
        return

    console.print(f"[bold]profile[/bold]  {profile_path}")
    console.print(
        "[bold]environment overrides[/bold]  "
        + (", ".join(overrides) if overrides else "(none)")
    )
    if not show_secrets:
        console.print("[dim]credentials and DSNs redacted; pass --show-secrets to reveal[/dim]")
    console.print()
    console.print(yaml.safe_dump(payload, sort_keys=False, default_flow_style=False).rstrip())


def _redact(value: Any, key: str = "") -> Any:
    """Blank anything whose key suggests a credential.

    Name-based rather than value-based: this output is pasted into tickets and chat,
    and a DSN carrying a password is the most common thing to leak that way.
    """
    if isinstance(value, dict):
        return {name: _redact(item, name) for name, item in value.items()}
    if isinstance(value, list):
        return [_redact(item, key) for item in value]
    if value and any(hint in key.lower() for hint in _SECRET_HINTS):
        return "***redacted***"
    return value


# --------------------------------------------------------------------- providers


@app.command(rich_help_panel=UNDERSTANDING)
def providers(profile: ProfileOption = None, as_json: JsonOption = False) -> None:
    """List every registered provider, marking the ones this profile uses.

    Read from the registries themselves, so it cannot drift from the code. The
    active markers turn it from a catalogue into an answer to "what am I running?".
    """
    settings = load(profile)
    active = {
        "llm": settings.llm.provider,
        "embeddings": settings.embeddings.provider,
        "reranker": settings.reranker.provider,
        "vector_store": settings.vector_store.provider,
        "chunker": settings.chunking.strategy,
    }
    # Typed explicitly: the five registries are Registry[T] over different T,
    # and only `names()` is used here, which every one of them has.
    registries: dict[str, Registry[Any]] = {
        "llm": llm_registry,
        "embeddings": embedding_registry,
        "reranker": reranker_registry,
        "vector_store": vector_store_registry,
        "chunker": chunker_registry,
    }

    if as_json:
        console.print_json(
            json.dumps(
                {
                    kind: {"active": active[kind], "available": registry.names()}
                    for kind, registry in registries.items()
                }
            )
        )
        return

    for kind, registry in registries.items():
        console.print(f"[bold]{kind}[/bold]")
        for name in registry.names():
            if name == active[kind]:
                console.print(f"  [green]●[/green] {name}  [dim](active)[/dim]")
            else:
                console.print(f"  ○ {name}")
        console.print()


# ------------------------------------------------------------------- index state


def _inspector(container: Container) -> StoreInspector:
    store = container.vector_store
    if not isinstance(store, StoreInspector):
        fail(
            f"The configured vector store ({type(store).__name__}) offers no "
            f"inspection interface."
        )
    return store  # type: ignore[return-value]


@app.command(rich_help_panel=UNDERSTANDING)
def status(profile: ProfileOption = None, as_json: JsonOption = False) -> None:
    """Summarise what is indexed: counts, chunk size distribution, formats."""
    settings = load(profile)

    async def _run() -> None:
        async with Container(settings) as container:
            stats = await _inspector(container).statistics()

        if as_json:
            console.print_json(json.dumps(_statistics_payload(stats)))
            return

        summary = table("field", "value")
        summary.add_row("workspace", stats.workspace_id)
        summary.add_row("documents", str(stats.documents))
        summary.add_row("chunks", str(stats.chunks))
        summary.add_row("embedding model", ", ".join(stats.embedding_models) or "(none)")
        summary.add_row("vector width", f"{stats.dimensions}d")
        summary.add_row(
            "chunk chars",
            f"min {stats.chunk_chars_min} · p50 {stats.chunk_chars_p50} · "
            f"p95 {stats.chunk_chars_p95} · max {stats.chunk_chars_max} "
            f"· mean {stats.chunk_chars_mean}",
        )
        summary.add_row(
            "chunks per document",
            f"{stats.chunks / stats.documents:.1f}" if stats.documents else "—",
        )
        summary.add_row(
            "by format",
            ", ".join(f"{ext} {count}" for ext, count in stats.documents_by_extension.items())
            or "(none)",
        )
        summary.add_row(
            "last indexed",
            stats.last_indexed_at.isoformat(timespec="seconds") if stats.last_indexed_at else "—",
        )
        console.print(summary)

        # The configured target and the measured result side by side: the point of
        # the percentiles is comparing them, and making the reader hold one in their
        # head while finding the other is how that comparison stops happening.
        console.print(
            f"\n[dim]configured chunk_size={settings.chunking.chunk_size} "
            f"overlap={settings.chunking.chunk_overlap} "
            f"strategy={settings.chunking.strategy}[/dim]"
        )

    run(_run())


def _statistics_payload(stats: Any) -> dict[str, Any]:
    return {
        "workspace_id": stats.workspace_id,
        "documents": stats.documents,
        "chunks": stats.chunks,
        "embedding_models": stats.embedding_models,
        "dimensions": stats.dimensions,
        "chunk_chars": {
            "min": stats.chunk_chars_min,
            "mean": stats.chunk_chars_mean,
            "p50": stats.chunk_chars_p50,
            "p95": stats.chunk_chars_p95,
            "max": stats.chunk_chars_max,
        },
        "documents_by_extension": dict(stats.documents_by_extension),
        "last_indexed_at": stats.last_indexed_at.isoformat() if stats.last_indexed_at else None,
    }


@app.command(rich_help_panel=LOOKING)
def documents(
    search: Annotated[
        str | None, typer.Argument(help="Match against title or source URI.")
    ] = None,
    profile: ProfileOption = None,
    limit: Annotated[int, typer.Option(help="Maximum documents to list.")] = 50,
    as_json: JsonOption = False,
) -> None:
    """List indexed documents with their chunk counts."""
    settings = load(profile)

    async def _run() -> None:
        async with Container(settings) as container:
            found = await _inspector(container).list_documents(limit=limit, search=search)

        if as_json:
            console.print_json(json.dumps([_document_payload(entry) for entry in found]))
            return
        if not found:
            console.print("no documents indexed" if not search else f"no match for {search!r}")
            return

        listing = table("id", "chunks", "title", "source")
        for entry in found:
            listing.add_row(
                entry.id[:12],
                str(entry.chunk_count),
                entry.title[:44],
                entry.source_uri.rsplit("/", 1)[-1],
            )
        console.print(listing)
        console.print(f"\n[dim]{len(found)} document(s). `document <id>` for detail.[/dim]")

    run(_run())


@app.command(rich_help_panel=LOOKING)
def document(
    identifier: Annotated[str, typer.Argument(help="Document id, or part of its path.")],
    profile: ProfileOption = None,
    chunks: Annotated[bool, typer.Option(help="List the document's chunks.")] = True,
    as_json: JsonOption = False,
) -> None:
    """Show one document's index record and how it chunked.

    Accepts a path fragment as well as an id, because nobody remembers a 24
    character hash and the thing an operator has in hand is the filename.
    """
    settings = load(profile)

    async def _run() -> None:
        async with Container(settings) as container:
            inspector = _inspector(container)
            found = await inspector.get_document(identifier)
            if found is None:
                matches = await inspector.list_documents(limit=10, search=identifier)
                if not matches:
                    fail(f"No indexed document matches {identifier!r}.")
                if len(matches) > 1:
                    console.print(f"[yellow]{len(matches)} documents match:[/yellow]")
                    for match in matches:
                        console.print(f"  {match.id[:12]}  {match.source_uri}")
                    raise typer.Exit(code=1)
                found = matches[0]

            document_chunks = await inspector.document_chunks(found.id) if chunks else []

        if as_json:
            console.print_json(
                json.dumps(
                    {
                        **_document_payload(found),
                        "chunks": [
                            {
                                "id": chunk.id,
                                "ordinal": chunk.ordinal,
                                "chars": len(chunk.text),
                                "text": chunk.text,
                                "metadata": dict(chunk.metadata),
                            }
                            for chunk in document_chunks
                        ],
                    }
                )
            )
            return

        detail = table("field", "value")
        detail.add_row("id", found.id)
        detail.add_row("title", found.title)
        detail.add_row("source", found.source_uri)
        detail.add_row("content hash", found.content_hash[:16] + "…")
        detail.add_row("chunks", str(found.chunk_count))
        detail.add_row("updated", found.updated_at.isoformat() if found.updated_at else "—")
        detail.add_row("indexed", found.indexed_at.isoformat() if found.indexed_at else "—")
        for key, value in sorted(found.metadata.items()):
            detail.add_row(f"metadata.{key}", str(value))
        console.print(detail)

        if document_chunks:
            console.print()
            listing = table("ord", "chars", "chunk id", "preview")
            for chunk in document_chunks:
                listing.add_row(
                    str(chunk.ordinal),
                    str(len(chunk.text)),
                    chunk.id.rsplit(":", 1)[-1],
                    chunk.text[:60].replace("\n", " ").strip(),
                )
            console.print(listing)
            console.print("\n[dim]`chunk <chunk id>` for the full text.[/dim]")

    run(_run())


@app.command(rich_help_panel=LOOKING)
def chunk(
    chunk_id: Annotated[str, typer.Argument(help="Full chunk id.")],
    profile: ProfileOption = None,
    as_json: JsonOption = False,
) -> None:
    """Print one chunk in full — exactly the text the model was shown.

    The last step of verifying a citation: a quoted answer, a chunk id, and the
    stored text side by side.
    """
    settings = load(profile)

    async def _run() -> None:
        async with Container(settings) as container:
            found = await _inspector(container).get_chunk(chunk_id)

        if found is None:
            fail(f"No chunk with id {chunk_id!r}.")
            return

        if as_json:
            console.print_json(
                json.dumps(
                    {
                        "id": found.id,
                        "document_id": found.document_id,
                        "ordinal": found.ordinal,
                        "title": found.title,
                        "source_uri": found.source_uri,
                        "text": found.text,
                        "metadata": dict(found.metadata),
                    }
                )
            )
            return

        console.print(f"[bold]{found.title}[/bold]  [dim]ordinal {found.ordinal}[/dim]")
        console.print(f"[dim]{found.source_uri}[/dim]")
        console.print(f"[dim]document {found.document_id}[/dim]\n")
        console.print(found.text)
        console.print(f"\n[dim]{len(found.text)} characters[/dim]")

    run(_run())


def _document_payload(summary: DocumentSummary) -> dict[str, Any]:
    return {
        "id": summary.id,
        "title": summary.title,
        "source_uri": summary.source_uri,
        "content_hash": summary.content_hash,
        "chunk_count": summary.chunk_count,
        "metadata": dict(summary.metadata),
        "updated_at": summary.updated_at.isoformat() if summary.updated_at else None,
        "indexed_at": summary.indexed_at.isoformat() if summary.indexed_at else None,
    }


# ------------------------------------------------------------------------ traces
#
# Two sources, one renderer. By default traces come from the persisted log, which
# is what makes them available after a one-shot command has exited. `--url` reads
# them from a running service instead, for a deployment whose filesystem is not
# this one — a container, or a colleague's machine.


def _traces_from(url: str | None, trace_id: str | None, limit: int) -> list[Trace]:
    if url:
        return _fetch_traces(url, trace_id, limit)

    store = active_trace_store()
    if store is None:
        fail(
            "Trace persistence is disabled (observability.persist_traces). "
            "Enable it, or pass --url to read from a running service."
        )
        return []
    if trace_id:
        found = store.get(trace_id)
        if found is None:
            fail(f"No trace matching {trace_id!r} in {store.path}.")
        return [found] if found else []
    return store.recent(limit=limit)


def _fetch_traces(url: str, trace_id: str | None, limit: int) -> list[Trace]:
    import httpx

    endpoint = f"{url.rstrip('/')}/api/traces" + (f"/{trace_id}" if trace_id else "")
    try:
        response = httpx.get(endpoint, params=None if trace_id else {"limit": limit}, timeout=10)
    except httpx.HTTPError as exc:
        fail(f"Could not reach {url}: {exc}. Is `osc-assistant serve` running?")
        return []

    if response.status_code == 404 and trace_id:
        fail(f"No trace {trace_id!r} in the service's buffer (it keeps only the most recent).")
    if response.status_code == 404:
        fail(
            "The service is not exposing traces. They are served only when "
            "environment is 'development' and observability.expose_traces is true."
        )
    if response.status_code >= 400:
        fail(f"{endpoint} returned {response.status_code}: {response.text[:200]}")

    payload = response.json()
    entries = [payload] if trace_id else payload.get("traces", [])
    return [trace_from_dict(entry) for entry in entries]


@app.command(rich_help_panel=LOOKING)
def traces(
    profile: ProfileOption = None,
    limit: Annotated[int, typer.Option(help="Traces to list.")] = 20,
    name: Annotated[
        str | None, typer.Option(help="Only traces with this name (answer, retrieve, ingest).")
    ] = None,
    failed: Annotated[bool, typer.Option("--failed", help="Only traces that failed.")] = False,
    slower_than: Annotated[
        float | None, typer.Option(help="Only traces slower than this many milliseconds.")
    ] = None,
    url: Annotated[
        str | None, typer.Option(help="Read from a running service instead of the local log.")
    ] = None,
    as_json: JsonOption = False,
) -> None:
    """List recent execution traces, most recent first.

    Read from the persisted trace log, so a command that has already exited is
    still explainable. The filters exist because the interesting trace is rarely
    the last one: `--failed` and `--slower-than` are how a developer finds the one
    worth expanding without reading twenty.
    """
    load(profile)
    found = _traces_from(url, None, limit)

    if name:
        found = [entry for entry in found if entry.name == name]
    if failed:
        found = [entry for entry in found if entry.failed]
    if slower_than is not None:
        found = [entry for entry in found if entry.duration_ms > slower_than]

    if as_json:
        console.print_json(json.dumps([entry.to_dict() for entry in found]))
        return
    if not found:
        console.print(
            "no matching traces yet — run `ask`, `search` or `ingest`, "
            "then try again"
        )
        return

    for entry in found:
        console.print(render_summary(entry), highlight=False)
    console.print(f"\n[dim]{len(found)} trace(s). `trace <id>` to expand one.[/dim]")


@app.command(rich_help_panel=LOOKING)
def trace(
    trace_id: Annotated[
        str | None,
        typer.Argument(help="Trace id or unique prefix. Omit for the most recent."),
    ] = None,
    profile: ProfileOption = None,
    url: Annotated[
        str | None, typer.Option(help="Read from a running service instead of the local log.")
    ] = None,
    as_json: JsonOption = False,
) -> None:
    """Expand one execution trace into a stage-by-stage waterfall.

    With no id this expands the most recent trace, which is almost always the one
    being asked about — "what just happened?" should not require copying an id
    first.
    """
    load(profile)
    found = _traces_from(url, trace_id, limit=1)
    if not found:
        console.print("no traces recorded yet")
        return

    if as_json:
        console.print_json(json.dumps(found[0].to_dict()))
        return
    console.print(render_waterfall(found[0]), highlight=False)


@app.command(rich_help_panel=UNDERSTANDING)
def version() -> None:
    """Print the installed version and the versions that shape behaviour."""
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as package_version

    packages = ("langchain-core", "langchain-text-splitters", "pydantic", "fastapi")
    # Width from the longest name, so adding a package cannot silently break the
    # alignment of every line above it.
    width = max(len(name) for name in (*packages, "python")) + 2

    console.print(f"[bold]osc-assistant[/bold] {package_version('osc-assistant')}")
    console.print(f"{'python':<{width}}{platform.python_version()}")
    for package in packages:
        try:
            console.print(f"{package:<{width}}{package_version(package)}")
        except PackageNotFoundError:  # pragma: no cover - core dependencies
            console.print(f"{package:<{width}}[red]not installed[/red]")
