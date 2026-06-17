import pytest

from edu_question_generator.generator import (
    QuestionGenerator,
    SafeExpressionEvaluator,
    TemplateError,
    load_default_templates,
    load_templates_from_file,
)


def test_generate_worksheet_count_and_answers():
    generator = QuestionGenerator(random_seed=7)

    worksheet = generator.generate(
        subject="math",
        topic="algebra",
        difficulty="easy",
        count=3,
    )

    assert worksheet.subject == "math"
    assert len(worksheet.questions) == 3
    assert all("Solve for x" in question.prompt for question in worksheet.questions)
    assert all("x =" in question.answer for question in worksheet.questions)


def test_list_options_contains_sample_subjects():
    generator = QuestionGenerator()

    options = generator.list_options()

    assert "math" in options
    assert "physics" in options
    assert "algebra" in options["math"]["topics"]
    assert "motion" in options["physics"]["topics"]


def test_load_default_templates_has_unique_ids():
    templates = load_default_templates()
    template_ids = [template.id for template in templates]

    assert len(templates) >= 10
    assert len(template_ids) == len(set(template_ids))
    assert {"math", "physics"} <= {template.subject for template in templates}


def test_load_templates_from_file(tmp_path):
    template_file = tmp_path / "templates.json"
    template_file.write_text(
        """
[
  {
    "id": "math-test-addition-easy",
    "subject": "math",
    "topic": "arithmetic",
    "difficulty": "easy",
    "prompt": "Calculate {a} + {b}.",
    "answer": "{a} + {b} = {total}.",
    "variables": [
      {"name": "a", "min": 1, "max": 3},
      {"name": "b", "min": 1, "max": 3}
    ],
    "formulas": {
      "total": "a + b"
    }
  }
]
""",
        encoding="utf-8",
    )

    templates = load_templates_from_file(template_file)

    assert len(templates) == 1
    assert templates[0].id == "math-test-addition-easy"
    assert templates[0].variables[0].name == "a"


def test_formula_evaluator_supports_simple_arithmetic():
    evaluator = SafeExpressionEvaluator()

    result = evaluator.evaluate("round((a + b) / c, 2)", {"a": 7, "b": 5, "c": 4})

    assert result == 3


def test_formula_evaluator_rejects_unknown_variables():
    evaluator = SafeExpressionEvaluator()

    with pytest.raises(TemplateError, match="Unknown variable"):
        evaluator.evaluate("a + missing", {"a": 1})


def test_formula_evaluator_rejects_unsafe_calls():
    evaluator = SafeExpressionEvaluator()

    with pytest.raises(TemplateError, match="Unsupported"):
        evaluator.evaluate("__import__('os')", {})


def test_generator_rejects_missing_template_combination():
    generator = QuestionGenerator()

    with pytest.raises(TemplateError, match="No templates found"):
        generator.generate("math", "unknown-topic", "easy", 1)


def test_generator_rejects_zero_count():
    generator = QuestionGenerator()

    with pytest.raises(ValueError, match="count"):
        generator.generate("math", "algebra", "easy", 0)
