# edu-question-generator

An open-source Python tool for tutors and teachers to generate middle-school math and physics practice worksheets from structured JSON templates.

The project creates two DOCX files for each worksheet:

- a student worksheet without answers
- a teacher version with detailed answers

It does not use paid APIs. Questions are generated locally from editable templates.

## Features

- Middle-school math and physics sample templates
- Choose subject, topic, difficulty, and number of questions
- Generate repeatable worksheets with an optional random seed
- Export student and teacher versions to DOCX
- Simple command-line interface
- Beginner-friendly dataclass models and JSON templates
- Basic tests

## Project Structure

```text
edu_question_generator/
  __init__.py
  cli.py
  generator.py
  models.py
  exporter.py
  templates/
examples/
tests/
README.md
LICENSE
requirements.txt
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## See Available Templates

```bash
python -m edu_question_generator.cli --list-options
```

## Create a Sample Worksheet

Generate a 5-question algebra worksheet:

```bash
python -m edu_question_generator.cli --subject math --topic algebra --difficulty easy --count 5 --seed 42
```

The generated files will be saved to:

```text
examples/output/math_algebra_easy_student.docx
examples/output/math_algebra_easy_teacher.docx
```

You can choose another output folder:

```bash
python -m edu_question_generator.cli --subject physics --topic motion --difficulty easy --count 10 --output-dir my_worksheets
```

## Editing Templates

Templates are JSON files in `edu_question_generator/templates/`.

Each template has:

- `prompt`: what the student sees
- `answer`: the teacher explanation
- `variables`: random values to generate
- `formulas`: calculated values used in the prompt or answer

Example:

```json
{
  "id": "math-geometry-rectangle-easy",
  "subject": "math",
  "topic": "geometry",
  "difficulty": "easy",
  "prompt": "A rectangle has length {length} cm and width {width} cm. Find its area.",
  "answer": "Area = length x width = {length} x {width} = {area} square cm.",
  "variables": [
    {"name": "length", "min": 4, "max": 18},
    {"name": "width", "min": 2, "max": 12}
  ],
  "formulas": {
    "area": "length * width"
  }
}
```

Formula expressions intentionally support only simple arithmetic so templates stay safe and easy to understand.

## Run Tests

```bash
pytest
```

## License

MIT
