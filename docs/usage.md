# Usage Guide

[English](../README.md) | [简体中文](../README_zh.md)

This guide walks through the project from a teacher's point of view.

## 1. Install the Project

From the project folder, install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 2. See What You Can Generate

Run:

```bash
python -m edu_question_generator.cli --list-options
```

You will see subjects such as `math` and `physics`, with available topics and difficulty levels.

## 3. Generate a Worksheet

Run:

```bash
python -m edu_question_generator.cli --subject math --topic geometry --difficulty easy --count 8
```

This creates two files:

- `examples/output/math_geometry_easy_student.docx`
- `examples/output/math_geometry_easy_teacher.docx`

## 4. Make Output Repeatable

Use `--seed` when you want the same questions again:

```bash
python -m edu_question_generator.cli --subject physics --topic motion --difficulty easy --count 6 --seed 100
```

## 5. Save Files Somewhere Else

Use `--output-dir`:

```bash
python -m edu_question_generator.cli --subject math --topic ratio --difficulty medium --count 10 --output-dir worksheets
```

## 6. Add a New Template

Open a JSON file in `edu_question_generator/templates/` and add a new object:

```json
{
  "id": "math-example-addition-easy",
  "subject": "math",
  "topic": "arithmetic",
  "difficulty": "easy",
  "prompt": "Calculate: {a} + {b}",
  "answer": "{a} + {b} = {sum}.",
  "variables": [
    {"name": "a", "min": 1, "max": 20},
    {"name": "b", "min": 1, "max": 20}
  ],
  "formulas": {
    "sum": "a + b"
  }
}
```

Run tests after editing templates:

```bash
python -m pytest
```

## 7. Common CLI Options

- `--subject`: `math` or `physics`
- `--topic`: a topic from `--list-options`
- `--difficulty`: `easy`, `medium`, or `hard`
- `--count`: number of questions
- `--seed`: optional value for repeatable output
- `--output-dir`: folder for DOCX files
- `--title`: custom worksheet title
