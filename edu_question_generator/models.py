"""Data models used by the worksheet generator."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class VariableSpec:
    """A numeric variable that can be randomly generated."""

    name: str
    min: int
    max: int
    step: int = 1


@dataclass(frozen=True)
class QuestionTemplate:
    """A reusable question pattern loaded from JSON."""

    id: str
    subject: str
    topic: str
    difficulty: str
    prompt: str
    answer: str
    variables: list[VariableSpec] = field(default_factory=list)
    formulas: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class GeneratedQuestion:
    """One concrete generated question and its detailed answer."""

    prompt: str
    answer: str
    template_id: str
    values: dict[str, Any]


@dataclass(frozen=True)
class Worksheet:
    """A complete worksheet containing generated questions."""

    title: str
    subject: str
    topic: str
    difficulty: str
    questions: list[GeneratedQuestion]
