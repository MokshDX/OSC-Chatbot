"""Human-facing startup and shutdown reporting for the service.

The structured JSON on stdout is correct for a log collector and close to
unreadable for a person starting the server on their laptop. Rather than
compromise one audience for the other, they get two streams: machine-readable
records continue to stdout untouched, and a short human summary goes to **stderr**.

That split is not cosmetic. `osc-assistant serve > run.log` still produces a clean,
parseable log file while the developer watching the terminal still sees where the
service is listening and what it is configured with.

The banner also runs one cheap check that catches the most common confusion on a
fresh machine: a service that starts perfectly and abstains from every question
because nothing has been ingested. That is indistinguishable from a broken model
unless somebody thinks to look, so the service says it up front.

Lives beside the app rather than in `cli` because the app owns its own lifecycle:
`serve` hands control to uvicorn and never sees the container again, and `api`
importing from `cli` would invert the dependency between an interface and the
service it starts.
"""

from __future__ import annotations

from rich.console import Console

from ..container import Container
from ..protocols import StoreInspector
from ..settings import Settings

# Its own console rather than a shared one, so this module depends on nothing but
# the service it describes.
_human = Console(stderr=True)


async def describe_startup(container: Container, settings: Settings) -> None:
    """Print where the service is listening and what it is running.

    Failures are swallowed: this is a courtesy for a human, and it must never be
    the reason a service fails to start.
    """
    base = f"http://{settings.server.host}:{settings.server.port}"
    lines = [
        "",
        "  [bold]OSC Knowledge Assistant[/bold]",
        f"  API   {base}/api",
        f"  UI    {base}/",
        f"  docs  {base}/docs",
        "",
        f"  environment  {settings.environment}   workspace {settings.workspace_id}",
        f"  llm          {settings.llm.provider}/{settings.llm.model}",
        f"  embeddings   {settings.embeddings.provider}/{settings.embeddings.model}",
        f"  store        {settings.vector_store.provider}   "
        f"retrieval {settings.retrieval.strategy}   chunker {settings.chunking.strategy}",
    ]

    for note in await startup_notes(container, settings):
        lines.append(f"  [yellow]note[/yellow]         {note}")

    if settings.traces_are_exposed:
        lines.append("  [dim]traces       ./osc traces   ·   GET /api/traces[/dim]")
    else:
        lines.append("  [dim]traces       ./osc traces (local log)[/dim]")
    lines.append("")

    for line in lines:
        _human.print(line, highlight=False)


async def startup_notes(container: Container, settings: Settings) -> list[str]:
    """Conditions worth telling a developer about before their first request.

    Returned rather than printed so they are testable without capturing a console,
    and so the same list can be logged as structured fields.
    """
    notes: list[str] = []

    store = container.vector_store
    if isinstance(store, StoreInspector):
        try:
            stats = await store.statistics()
        except Exception:  # pragma: no cover - startup has already succeeded
            stats = None
        if stats is not None and stats.documents == 0:
            notes.append(
                "the index is empty — every question will abstain. "
                "Run `./osc ingest ./docs`."
            )
        elif stats is not None and len(stats.embedding_models) > 1:
            notes.append(
                f"chunks are embedded by {len(stats.embedding_models)} different "
                f"models; only one is reachable by search. Re-index with --reindex."
            )

    # A chat UI on an unauthenticated service is the state most likely to be
    # mistaken for something deployable, so it is said out loud at every start
    # rather than left in a README.
    if settings.environment != "development":
        notes.append(
            f"environment is {settings.environment!r} and no authentication is "
            f"implemented; this service must sit behind an identity proxy."
        )

    return notes


def describe_shutdown() -> None:
    _human.print("\n  [dim]OSC Knowledge Assistant stopped.[/dim]\n", highlight=False)
