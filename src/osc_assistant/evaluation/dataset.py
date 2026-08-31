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
    corpus: str = Field(
        default="",
        description=(
            "The corpus root this set is scored against, e.g. `docs/company/schema`. "
            "Recorded rather than enforced — the harness cannot know which corpus is "
            "indexed, only which documents are — but it turns the resulting failure "
            "from 'every case scored zero' into a message naming the directory to "
            "ingest. Two suites over two corpora are not comparable, and this is what "
            "says so on the result file."
        ),
    )
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


def _read_yaml_mapping(path: Path) -> dict[str, Any]:
    """Read a suite file, reporting the three ways it can fail to be one.

    Shared by both loaders so that a missing file, malformed YAML and a top-level
    scalar produce the same message whichever kind of suite was being loaded — the
    reader of the error does not yet know which kind it is.
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
    return parsed


class ConversationalTurn(BaseModel):
    """One question inside a multi-turn case.

    Carries the same expectations as a `GoldenCase` — this is deliberate, so that a
    turn is scored by exactly the arithmetic a single-turn case is scored by and the
    two suites' retrieval numbers mean the same thing — plus two flags that only
    make sense in a conversation.
    """

    question: str = Field(min_length=1)
    relevant_documents: list[str] = Field(default_factory=list)
    expected_facts: list[str] = Field(default_factory=list)
    must_abstain: bool = False

    requires_context: bool = Field(
        default=False,
        description=(
            "This question is not answerable standalone. Enrolls the turn in the "
            "cold control run, whose difference from the in-session run is the only "
            "evidence that memory contributed anything."
        ),
    )
    context_switch: bool = Field(
        default=False,
        description=(
            "This question is standalone and about a different document from the "
            "turns before it. Measures the opposite failure: history dragging "
            "retrieval back to the previous topic."
        ),
    )

    @field_validator("relevant_documents")
    @classmethod
    def _normalise_paths(cls, value: list[str]) -> list[str]:
        return [PurePosixPath(entry.strip().lstrip("./")).as_posix() for entry in value]

    @model_validator(mode="after")
    def _check_expectations(self) -> ConversationalTurn:
        if not self.must_abstain and not self.relevant_documents:
            raise ValueError(
                f"turn {self.question!r} names no relevant_documents and is not "
                f"must_abstain, so nothing about it can be scored"
            )
        if self.must_abstain and self.relevant_documents:
            raise ValueError(
                f"turn {self.question!r} is must_abstain but also names "
                f"relevant_documents"
            )
        if self.requires_context and self.context_switch:
            # They are opposites. `requires_context` says the turn should score
            # *better* with history; `context_switch` says it should score the same.
            # A turn flagged both would be counted in two aggregates that disagree
            # about what a good result looks like.
            raise ValueError(
                f"turn {self.question!r} is both requires_context and "
                f"context_switch; a turn cannot depend on the conversation and be "
                f"independent of it"
            )
        return self


class ConversationalCase(BaseModel):
    """One session: an ordered sequence of turns scored as a conversation."""

    id: str = Field(min_length=1)
    description: str = ""
    turns: list[ConversationalTurn] = Field(min_length=2)
    tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _first_turn_stands_alone(self) -> ConversationalCase:
        # A case whose opening question already contains a reference measures the
        # abstention policy and nothing else — there is no conversation yet for it
        # to resolve against.
        opening = self.turns[0]
        if opening.requires_context:
            raise ValueError(
                f"case {self.id!r} opens with a turn marked requires_context; "
                f"there is no prior turn for it to resolve against"
            )
        return self


class ConversationalSet(BaseModel):
    """A named, versioned collection of multi-turn cases."""

    version: int = 1
    description: str = ""
    corpus: str = ""
    cases: list[ConversationalCase]

    @field_validator("cases")
    @classmethod
    def _unique_ids(cls, value: list[ConversationalCase]) -> list[ConversationalCase]:
        seen: set[str] = set()
        for case in value:
            if case.id in seen:
                raise ValueError(f"duplicate case id {case.id!r}")
            seen.add(case.id)
        return value

    @property
    def referenced_documents(self) -> set[str]:
        return {
            path for case in self.cases for turn in case.turns for path in turn.relevant_documents
        }

    @property
    def turn_count(self) -> int:
        return sum(len(case.turns) for case in self.cases)


def load_conversational_set(path: Path) -> ConversationalSet:
    """Read and validate a multi-turn golden set.

    Raises:
        EvaluationError: The file is missing, is not valid YAML, or does not
            describe a usable set.
    """
    parsed = _read_yaml_mapping(path)
    try:
        conversational = ConversationalSet.model_validate(parsed)
    except ValidationError as exc:
        raise EvaluationError(f"Conversational set {path} is invalid:\n{exc}") from exc

    if not conversational.cases:
        raise EvaluationError(f"Conversational set {path} contains no cases.")
    return conversational


def load_golden_set(path: Path) -> GoldenSet:
    """Read and validate a golden set file.

    Raises:
        EvaluationError: The file is missing, is not valid YAML, or does not
            describe a usable golden set. Every message names the file and, where
            the validator could determine it, the case at fault.
    """
    parsed = _read_yaml_mapping(path)
    try:
        golden = GoldenSet.model_validate(parsed)
    except ValidationError as exc:
        raise EvaluationError(f"Golden set {path} is invalid:\n{exc}") from exc

    if not golden.cases:
        raise EvaluationError(f"Golden set {path} contains no cases.")
    return golden


def unresolvable_documents(golden: GoldenSet | ConversationalSet, indexed: set[str]) -> set[str]:
    """Documents a suite expects that are not in the index.

    Checked before a run because the failure is otherwise indistinguishable from
    the thing being measured: a mistyped path and a genuine retrieval miss both
    score recall 0, and only one of them is a bug in the search stack.

    Takes either suite type — both expose `referenced_documents`, and the check is
    identical for a question and for a turn. The conversational runner briefly had
    its own set-difference helper, which was this function with a worse name.
    """
    return golden.referenced_documents - indexed
