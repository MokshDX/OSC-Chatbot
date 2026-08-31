"""The commands that do work: serve, ingest, ask, search.

Ingestion and ad-hoc querying live here rather than behind HTTP because they are
operator actions, and keeping them off the API means the service exposes no
unauthenticated write endpoint.

Every command that runs a pipeline accepts `--explain`, which prints the execution
trace as a waterfall. That is the intended debugging loop: run the thing, see which
stage was slow or wrong, without adding a log statement or attaching a debugger.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Annotated

import typer

from ..api import create_app
from ..container import Container
from ..ingestion import FilesystemLoader
from ..types import Answer
from ._shared import (
    RUNNING,
    ExplainOption,
    JsonOption,
    ProfileOption,
    VerboseOption,
    console,
    load,
    print_trace,
    run,
    traced_command,
)

app = typer.Typer()


@app.command(rich_help_panel=RUNNING)
def serve(
    profile: ProfileOption = None,
    host: Annotated[str | None, typer.Option(help="Override the configured host.")] = None,
    port: Annotated[int | None, typer.Option(help="Override the configured port.")] = None,
    reload: Annotated[bool, typer.Option(help="Reload on source changes.")] = False,
) -> None:
    """Run the HTTP service and chat UI."""
    import uvicorn

    # The service keeps its configured structured logging: JSON on stdout is the
    # right output for something a log collector reads. The human summary the
    # banner prints goes to stderr, so redirecting stdout still yields a clean log.
    settings = load(profile, quiet_logs=False)
    if host or port:
        # uvicorn is told the real values so its own bind matches what the banner
        # prints; without this an overridden port would be advertised wrongly.
        settings = settings.model_copy(
            update={
                "server": settings.server.model_copy(
                    update={
                        "host": host or settings.server.host,
                        "port": port or settings.server.port,
                    }
                )
            }
        )

    if reload:
        # Reload needs an import string: the worker is a fresh process that cannot
        # be handed a closure. It re-reads settings from the environment, which is
        # why --host/--port are exported rather than passed.
        os.environ["OSC_SERVER__HOST"] = settings.server.host
        os.environ["OSC_SERVER__PORT"] = str(settings.server.port)
        target: object = "osc_assistant.api.app:create_app"
    else:
        target = lambda: create_app(settings, banner=True)  # noqa: E731

    uvicorn.run(
        target,  # type: ignore[arg-type]
        factory=True,
        host=settings.server.host,
        port=settings.server.port,
        reload=reload,
        log_config=None,  # Our own structured logging is already configured.
    )


@app.command(rich_help_panel=RUNNING)
def ingest(
    path: Annotated[
        Path | None,
        typer.Argument(
            help="Directory to index. Defaults to the configured `corpus.root`.",
        ),
    ] = None,
    profile: ProfileOption = None,
    prune: Annotated[
        bool,
        typer.Option(help="Delete indexed documents no longer present. Correct for a full sync."),
    ] = True,
    reindex: Annotated[
        bool,
        typer.Option(
            "--reindex",
            help=(
                "Re-chunk and re-embed every document even if unchanged. Required "
                "after changing the chunker or its settings, which the content hash "
                "does not cover."
            ),
        ),
    ] = False,
    explain: ExplainOption = False,
    verbose: VerboseOption = False,
) -> None:
    """Index a directory of documents."""
    settings = load(profile, verbose=verbose)
    # Naming the root here rather than defaulting the argument to a literal keeps
    # exactly one definition of "what the corpus is" in the system. A second literal
    # is how an ingest root and a doctor root drift apart without either being wrong.
    root = path or settings.corpus.root

    async def _run() -> None:
        async with Container(settings) as container:
            loader = FilesystemLoader(root)
            report = await container.ingestion.ingest(
                loader.load(), prune=prune, reindex=reindex, source_failures=loader.failures
            )

            console.print(
                f"processed={report.processed} indexed={report.indexed} "
                f"skipped={report.skipped} deleted={report.deleted} "
                f"chunks={report.chunks} unreadable={report.unreadable} "
                f"in {report.duration_seconds:.1f}s"
            )
            for failure in report.failures:
                console.print(f"  [red]failed:[/red] {failure}")
            if report.trace_id:
                console.print(f"[dim]trace {report.trace_id}[/dim]")

            print_trace(explain)
            if not report.succeeded:
                raise typer.Exit(code=1)

    with traced_command():
        run(_run())


@app.command(rich_help_panel=RUNNING)
def ask(
    question: Annotated[str, typer.Argument(help="The question to answer.")],
    profile: ProfileOption = None,
    explain: ExplainOption = False,
    as_json: JsonOption = False,
    verbose: VerboseOption = False,
) -> None:
    """Ask a question and print the grounded answer."""
    settings = load(profile, verbose=verbose)

    async def _run() -> None:
        async with Container(settings) as container:
            answer = await container.answerer.answer(question)
            if as_json:
                console.print_json(json.dumps(_answer_payload(answer)))
            else:
                _print_answer(answer)
            print_trace(explain)

    with traced_command():
        run(_run())


@app.command(rich_help_panel=RUNNING)
def search(
    query: Annotated[str, typer.Argument(help="The retrieval query.")],
    profile: ProfileOption = None,
    explain: ExplainOption = False,
    as_json: JsonOption = False,
    verbose: VerboseOption = False,
) -> None:
    """Run retrieval only, without generating an answer.

    The first place to look when an answer is wrong: it separates "the model
    misread the passage" from "the passage was never retrieved", which are
    different bugs with different fixes.
    """
    settings = load(profile, verbose=verbose)

    async def _run() -> None:
        async with Container(settings) as container:
            result = await container.retrieval.retrieve(query)

            if as_json:
                console.print_json(
                    json.dumps(
                        {
                            "query": result.query,
                            "original_query": result.original_query,
                            "candidates_considered": result.candidates_considered,
                            "duration_seconds": result.duration_seconds,
                            "trace_id": result.trace_id,
                            "results": [
                                {
                                    "chunk_id": hit.chunk.id,
                                    "document_id": hit.chunk.document_id,
                                    "title": hit.chunk.title,
                                    "source_uri": hit.chunk.source_uri,
                                    "score": hit.score,
                                    "match_source": hit.source.value,
                                    "text": hit.chunk.text,
                                }
                                for hit in result.chunks
                            ],
                        }
                    )
                )
            else:
                console.print(
                    f"query: {result.query}  "
                    f"([bold]{result.candidates_considered}[/bold] candidates, "
                    f"{result.duration_seconds * 1000:.0f}ms)"
                )
                for position, hit in enumerate(result.chunks, start=1):
                    console.print(
                        f"\n[bold]{position}.[/bold] [{hit.score:.4f}] "
                        f"{hit.chunk.title}  [dim]({hit.source.value})[/dim]"
                    )
                    console.print(f"   [dim]{hit.chunk.source_uri}[/dim]")
                    console.print(f"   [dim]{hit.chunk.id}[/dim]")
                    console.print(f"   {hit.chunk.text[:200].strip()}...")
                if result.trace_id:
                    console.print(f"\n[dim]trace {result.trace_id}[/dim]")

            print_trace(explain)

    with traced_command():
        run(_run())


def _print_answer(answer: Answer) -> None:
    console.print(answer.text)
    if answer.citations:
        console.print("\n[bold]Sources:[/bold]")
        for citation in answer.citations:
            console.print(
                f"  [{citation.index}] {citation.title} — "
                f"[dim]{citation.source_uri}[/dim]"
            )
    console.print(
        f"\n[dim]model={answer.model} "
        f"tokens={answer.usage.input_tokens}/{answer.usage.output_tokens} "
        f"chunks={len(answer.retrieved)} abstained={answer.abstained} "
        f"trace={answer.trace_id}[/dim]"
    )


def _answer_payload(answer: Answer) -> dict[str, object]:
    return {
        "text": answer.text,
        "abstained": answer.abstained,
        "model": answer.model,
        "trace_id": answer.trace_id,
        "citations": [
            {
                "index": citation.index,
                "chunk_id": citation.chunk_id,
                "document_id": citation.document_id,
                "title": citation.title,
                "source_uri": citation.source_uri,
            }
            for citation in answer.citations
        ],
        "usage": {
            "input_tokens": answer.usage.input_tokens,
            "output_tokens": answer.usage.output_tokens,
            "cached_input_tokens": answer.usage.cached_input_tokens,
        },
    }
