"""Question template loading and worksheet generation."""

from __future__ import annotations

import ast
import json
import operator
import random
from importlib import resources
from pathlib import Path
from typing import Any

from .models import GeneratedQuestion, QuestionTemplate, VariableSpec, Worksheet


class TemplateError(ValueError):
    """Raised when a template cannot be loaded or evaluated."""


class SafeExpressionEvaluator:
    """Evaluate simple arithmetic formulas from trusted template files."""

    _binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    _unary_operators = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }
    _functions = {
        "abs": abs,
        "round": round,
        "int": int,
        "float": float,
    }

    def evaluate(self, expression: str, values: dict[str, Any]) -> Any:
        tree = ast.parse(expression, mode="eval")
        return self._eval_node(tree.body, values)

    def _eval_node(self, node: ast.AST, values: dict[str, Any]) -> Any:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.Name):
            if node.id not in values:
                raise TemplateError(f"Unknown variable in formula: {node.id}")
            return values[node.id]

        if isinstance(node, ast.BinOp):
            operator_type = type(node.op)
            if operator_type not in self._binary_operators:
                raise TemplateError(f"Unsupported operator: {operator_type.__name__}")
            left = self._eval_node(node.left, values)
            right = self._eval_node(node.right, values)
            return self._binary_operators[operator_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operator_type = type(node.op)
            if operator_type not in self._unary_operators:
                raise TemplateError(f"Unsupported operator: {operator_type.__name__}")
            return self._unary_operators[operator_type](self._eval_node(node.operand, values))

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id not in self._functions:
                raise TemplateError(f"Unsupported function: {node.func.id}")
            args = [self._eval_node(arg, values) for arg in node.args]
            return self._functions[node.func.id](*args)

        raise TemplateError(f"Unsupported formula expression: {ast.dump(node)}")


class QuestionGenerator:
    """Generate worksheet questions from JSON template files."""

    def __init__(
        self,
        templates: list[QuestionTemplate] | None = None,
        random_seed: int | None = None,
    ) -> None:
        self.templates = templates if templates is not None else load_default_templates()
        self.random = random.Random(random_seed)
        self.evaluator = SafeExpressionEvaluator()

    def list_options(self) -> dict[str, dict[str, list[str]]]:
        """Return available subjects, topics, and difficulties."""

        options: dict[str, dict[str, set[str]]] = {}
        for template in self.templates:
            subject_options = options.setdefault(
                template.subject,
                {"topics": set(), "difficulties": set()},
            )
            subject_options["topics"].add(template.topic)
            subject_options["difficulties"].add(template.difficulty)

        return {
            subject: {
                "topics": sorted(values["topics"]),
                "difficulties": sorted(values["difficulties"]),
            }
            for subject, values in sorted(options.items())
        }

    def generate(
        self,
        subject: str,
        topic: str,
        difficulty: str,
        count: int,
        title: str | None = None,
    ) -> Worksheet:
        """Generate a complete worksheet."""

        if count < 1:
            raise ValueError("count must be at least 1")

        matching_templates = [
            template
            for template in self.templates
            if template.subject.lower() == subject.lower()
            and template.topic.lower() == topic.lower()
            and template.difficulty.lower() == difficulty.lower()
        ]
        if not matching_templates:
            raise TemplateError(
                "No templates found for "
                f"subject={subject!r}, topic={topic!r}, difficulty={difficulty!r}."
            )

        questions = [
            self._generate_question(self.random.choice(matching_templates))
            for _ in range(count)
        ]
        worksheet_title = title or f"{subject.title()} - {topic.title()} Practice"
        return Worksheet(
            title=worksheet_title,
            subject=subject,
            topic=topic,
            difficulty=difficulty,
            questions=questions,
        )

    def _generate_question(self, template: QuestionTemplate) -> GeneratedQuestion:
        values: dict[str, Any] = {}
        for variable in template.variables:
            values[variable.name] = self._random_value(variable)

        for name, expression in template.formulas.items():
            values[name] = self.evaluator.evaluate(expression, values)

        display_values = {key: _format_value(value) for key, value in values.items()}
        prompt = template.prompt.format(**display_values)
        answer = template.answer.format(**display_values)
        return GeneratedQuestion(
            prompt=prompt,
            answer=answer,
            template_id=template.id,
            values=values,
        )

    def _random_value(self, variable: VariableSpec) -> int:
        if variable.step <= 0:
            raise TemplateError(f"Variable {variable.name} has a non-positive step.")
        choices = list(range(variable.min, variable.max + 1, variable.step))
        if not choices:
            raise TemplateError(f"Variable {variable.name} has no possible values.")
        return self.random.choice(choices)


def load_default_templates() -> list[QuestionTemplate]:
    """Load bundled templates from the package."""

    template_root = resources.files("edu_question_generator.templates")
    templates: list[QuestionTemplate] = []
    for template_file in sorted(template_root.glob("*.json")):
        templates.extend(load_templates_from_file(Path(str(template_file))))
    return templates


def load_templates_from_file(path: Path) -> list[QuestionTemplate]:
    """Load question templates from a JSON file."""

    with path.open("r", encoding="utf-8") as file:
        raw_templates = json.load(file)
    if not isinstance(raw_templates, list):
        raise TemplateError(f"Template file must contain a list: {path}")
    return [_parse_template(item, path) for item in raw_templates]


def _parse_template(data: dict[str, Any], path: Path) -> QuestionTemplate:
    try:
        variables = [
            VariableSpec(
                name=item["name"],
                min=int(item["min"]),
                max=int(item["max"]),
                step=int(item.get("step", 1)),
            )
            for item in data.get("variables", [])
        ]
        return QuestionTemplate(
            id=data["id"],
            subject=data["subject"],
            topic=data["topic"],
            difficulty=data["difficulty"],
            prompt=data["prompt"],
            answer=data["answer"],
            variables=variables,
            formulas=dict(data.get("formulas", {})),
        )
    except KeyError as exc:
        raise TemplateError(f"Missing required template field {exc} in {path}") from exc


def _format_value(value: Any) -> str:
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return str(value)
