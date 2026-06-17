"""Generate practice worksheets from structured education templates."""

from .generator import QuestionGenerator
from .models import GeneratedQuestion, QuestionTemplate, Worksheet

__all__ = [
    "GeneratedQuestion",
    "QuestionGenerator",
    "QuestionTemplate",
    "Worksheet",
]

__version__ = "0.1.0"
version = "0.1.0"
