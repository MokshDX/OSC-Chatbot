"""The golden set: the questions an evaluation run is scored against.

A golden set is data, not code, and it is edited by people who are not going to
open a Python file — so it is YAML, it is validated at load time with Pydantic (the
project's rule is that validation belongs at the trust boundary), and every failure
is reported as a message naming the case that is wrong.

The format is deliberately small. A case is a question, the documents that answer
it, and optionally the facts the answer must contain:

```yaml
version: 1
cases:
  - id: tiered-pricing-collection-level
    question: Can I apply tiered pricing at collection level?
    relevant_documents: [faq/faq.md]
    expected_facts: ["customer tag"]
    tags: [tiered-pricing]
```

`relevant_documents` are **corpus-relative paths** — the same string the ingestion
loader records as `relative_path` on every chunk. That choice is what keeps a
golden set readable, diffable in review, and stable across a re-index: document ids
are SHA-256 digests of an absolute file URI, so they are opaque to a curator and
differ between two developers' machines.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

from ..errors import EvaluationError
from ..types import Chunk


def document_key(chunk: Chunk) -> str:
    """The identity a golden set refers to a retrieved chunk's document by.

    `relative_path` is set by the filesystem loader and travels with the chunk into
    the store, which makes it available here without a second lookup. The fall back
    to `source_uri` covers chunks that came from a connector with no filesystem
    behind it; such a corpus is scored by URI, which is less readable but still
    stable.
    """
    relative = chunk.metadata.get("relative_path")
    if isinstance(relative, str) and relative:
        return PurePosixPath(relative).as_posix()
    return chunk.source_uri


class GoldenCase(BaseModel):
    """One question and what a correct system does with it."""

    id: str = Field(min_length=1)
    question: str = Field(min_length=1)

    relevant_documents: list[str] = Field(
        default_factory=list,
        description="Corpus-relative paths of the documents that answer the question.",
    )
    expected_facts: list[str] = Field(
        default_factory=list,
        description=(
            "Substrings the answer must contain, matched case-insensitively. Kept to "
            "short distinctive phrases — a number, a limit, a product name — because "
            "anything longer scores the model's phrasing rather than its correctness."
        ),
    )
    must_abstain: bool = Field(
        default=False,
        description=(
            "The corpus does not answer this question and the system must say so. "
            "Abstention cases are what stop an evaluation from rewarding a model that "
            "answers everything confidently."
        ),
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Free-form labels for slicing a report, e.g. by product area.",
    )

    @model_validator(mode="after")
    def _check_expectations(self) -> GoldenCase:
        # A case with neither a relevant document nor an abstention expectation
        # cannot be scored at all, and would silently drag the mean towards zero
        # while looking like a retrieval failure.
        if not self.must_abstain and not self.relevant_documents:
            raise ValueError(
                f"case {self.id!r} names no relevant_documents and is not must_abstain, "
                f"so nothing about it can be scored"
            )
        if self.must_abstain and self.relevant_documents:
            raise ValueError(
                f"case {self.id!r} is must_abstain but also names relevant_documents; "
                f"an abstention case asserts the corpus cannot answer it"
            )
        return self

    @field_validator("relevant_documents")
    @classmethod
    def _normalise_paths(cls, value: list[str]) -> list[str]:
        return [PurePosixPath(entry.strip().lstrip("./")).as_posix() for entry in value]


class GoldenSet(BaseModel):
    """A named, versioned collection of cases."""

    version: int = 1
    description: str = ""
    cases: list[GoldenCase]

    @field_validator("cases")
    @classmethod
    def _unique_ids(cls, value: list[GoldenCase]) -> list[GoldenCase]:
        seen: set[str] = set()
        for case in value:
            if case.id in seen:
                # Ids key the per-case results and the baseline comparison; a
                # duplicate would make one run's case silently overwrite another's.
                raise ValueError(f"duplicate case id {case.id!r}")
            seen.add(case.id)
        return value

    @property
    def referenced_documents(self) -> set[str]:
        """Every document any case expects to be retrievable."""
        return {path for case in self.cases for path in case.relevant_documents}


def load_golden_set(path: Path) -> GoldenSet:
    """Read and validate a golden set file.

    Raises:
        EvaluationError: The file is missing, is not valid YAML, or does not
            describe a usable golden set. Every message names the file and, where
            the validator could determine it, the case at fault.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise EvaluationError(f"Could not read golden set {path}: {exc}") from exc

    try:
        parsed: Any = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise EvaluationError(f"Golden set {path} is not valid YAML: {exc}") from exc

    if not isinstance(parsed, dict):
        raise EvaluationError(
            f"Golden set {path} must be a YAML mapping with a 'cases' key, "
            f"got {type(parsed).__name__}."
        )

    try:
        golden = GoldenSet.model_validate(parsed)
    except ValidationError as exc:
        raise EvaluationError(f"Golden set {path} is invalid:\n{exc}") from exc

    if not golden.cases:
        raise EvaluationError(f"Golden set {path} contains no cases.")
    return golden


def unresolvable_documents(golden: GoldenSet, indexed: set[str]) -> set[str]:
    """Documents a golden set expects that are not in the index.

    Checked before a run because the failure is otherwise indistinguishable from
    the thing being measured: a mistyped path and a genuine retrieval miss both
    score recall 0, and only one of them is a bug in the search stack.
    """
    return golden.referenced_documents - indexed
