"""Command line interface.

Ingestion, ad-hoc querying and provider inspection live here rather than behind
HTTP: they are operator actions, and keeping them off the API means the service
exposes no unauthenticated write endpoint.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated

import typer

from .container import Container
from .ingestion import FilesystemLoader
from .logging import configure_logging
from .registries import (
    chunker_registry,
    embedding_registry,
    llm_registry,
    reranker_registry,
    vector_store_registry,
)
from .settings import Settings, load_settings

app = typer.Typer(
    name="osc-assistant",
    help="OSC internal knowledge assistant.",
    no_args_is_help=True,
    add_completion=False,
)

ProfileOption = Annotated[
    Path | None,
    typer.Option("--profile", "-p", help="YAML profile to load instead of config/default.yaml."),
]


def _settings(profile: Path | None) -> Settings:
    import os

    if profile is not None:
        os.environ["OSC_PROFILE"] = str(profile)
    settings = load_settings()
    configure_logging(settings.log_level, settings.log_format)
    return settings


@app.command()
def serve(
    profile: ProfileOption = None,
    host: Annotated[str | None, typer.Option(help="Override the configured host.")] = None,
    port: Annotated[int | None, typer.Option(help="Override the configured port.")] = None,
    reload: Annotated[bool, typer.Option(help="Reload on source changes.")] = False,
) -> None:
    """Run the HTTP service."""
    import uvicorn

    settings = _settings(profile)
    uvicorn.run(
        "osc_assistant.api.app:create_app",
        factory=True,
        host=host or settings.server.host,
        port=port or settings.server.port,
        reload=reload,
        log_config=None,  # Our own structured logging is already configured.
    )


@app.command()
def ingest(
    path: Annotated[Path, typer.Argument(help="Directory to index.")],
    profile: ProfileOption = None,
    prune: Annotated[
        bool,
        typer.Option(
            help="Delete indexed documents no longer present. Correct for a full sync."
        ),
    ] = True,
) -> None:
    """Index a directory of documents."""
    settings = _settings(profile)

    async def run() -> None:
        async with Container(settings) as container:
            loader = FilesystemLoader(path)
            report = await container.ingestion.ingest(loader.load(), prune=prune)

            typer.echo(
                f"processed={report.processed} indexed={report.indexed} "
                f"skipped={report.skipped} deleted={report.deleted} "
                f"chunks={report.chunks} in {report.duration_seconds:.1f}s"
            )
            for failure in report.failures:
                typer.secho(f"  failed: {failure}", fg=typer.colors.RED)
            if not report.succeeded:
                raise typer.Exit(code=1)

    asyncio.run(run())


@app.command()
def ask(
    question: Annotated[str, typer.Argument(help="The question to answer.")],
    profile: ProfileOption = None,
) -> None:
    """Ask a question and print the grounded answer."""
    settings = _settings(profile)

    async def run() -> None:
        async with Container(settings) as container:
            answer = await container.answerer.answer(question)

            typer.echo(answer.text)
            if answer.citations:
                typer.echo("\nSources:")
                for citation in answer.citations:
                    typer.echo(f"  [{citation.index}] {citation.title} — {citation.source_uri}")
            typer.secho(
                f"\nmodel={answer.model} "
                f"tokens={answer.usage.input_tokens}/{answer.usage.output_tokens} "
                f"chunks={len(answer.retrieved)} abstained={answer.abstained}",
                fg=typer.colors.BRIGHT_BLACK,
            )

    asyncio.run(run())


@app.command()
def search(
    query: Annotated[str, typer.Argument(help="The retrieval query.")],
    profile: ProfileOption = None,
) -> None:
    """Run retrieval only, without generating an answer."""
    settings = _settings(profile)

    async def run() -> None:
        async with Container(settings) as container:
            result = await container.retrieval.retrieve(query)

            typer.echo(f"query: {result.query}  ({result.candidates_considered} candidates)")
            for position, hit in enumerate(result.chunks, start=1):
                typer.echo(f"\n{position}. [{hit.score:.4f}] {hit.chunk.title}")
                typer.echo(f"   {hit.chunk.source_uri}")
                typer.echo(f"   {hit.chunk.text[:200].strip()}...")

    asyncio.run(run())


@app.command()
def providers() -> None:
    """List every registered provider.

    The authoritative answer to "what can I switch to?", read from the registries
    themselves so it cannot drift from the code.
    """
    for label, registry in (
        ("llm", llm_registry),
        ("embeddings", embedding_registry),
        ("reranker", reranker_registry),
        ("vector_store", vector_store_registry),
        ("chunker", chunker_registry),
    ):
        typer.secho(f"{label}:", bold=True)
        for name in registry.names():
            typer.echo(f"  - {name}")


if __name__ == "__main__":  # pragma: no cover
    app()
