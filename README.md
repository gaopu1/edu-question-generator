# edu-question-generator

[English](README.md) | [简体中文](README_zh.md)

`edu-question-generator` is a small open-source Python project for tutors, teachers, and learning centers that need printable middle-school math and physics worksheets.

Current release: `v0.1.0`.

The project generates questions from simple JSON templates, then exports two DOCX files:

- a student worksheet without answers
- a teacher version with worked answers

Everything runs locally. No paid APIs, accounts, or internet connection are required after dependencies are installed.

## Features

- Middle-school math and physics template bank
- Subject, topic, difficulty, and question count selection
- Repeatable generation with an optional random seed
- Student and teacher DOCX export using `python-docx`
- Beginner-friendly dataclass models
- Editable JSON templates with safe arithmetic formulas
- Command-line interface for quick worksheet creation
- Tests for generation, template loading, formula evaluation, and DOCX export

## Installation

Clone the repository:

```bash
git clone https://github.com/gaopu1/edu-question-generator.git
cd edu-question-generator
```

Create and activate a virtual environment.

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

For editable local development, you can also install the project metadata:

```bash
python -m pip install -e ".[dev]"
```

## Quick Start

List the available subjects, topics, and difficulty levels:

```bash
python -m edu_question_generator.cli --list-options
```

Create a five-question algebra worksheet:

```bash
python -m edu_question_generator.cli --subject math --topic algebra --difficulty easy --count 5 --seed 42
```

## Example Command

Generate a physics worksheet about motion and save it in a custom folder:

```bash
python -m edu_question_generator.cli --subject physics --topic motion --difficulty easy --count 10 --output-dir worksheets
```

## Sample Output

The default output folder is `examples/output/`.

For this command:

```bash
python -m edu_question_generator.cli --subject math --topic algebra --difficulty easy --count 5 --seed 42
```

the project creates:

```text
examples/output/math_algebra_easy_student.docx
examples/output/math_algebra_easy_teacher.docx
```

The student file contains numbered practice questions and blank space for answers. The teacher file contains the same questions plus a short worked solution for each one.

## Editing Templates

Templates are JSON files in `edu_question_generator/templates/`.

Each template includes:

- `prompt`: the question shown to students
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

Formula expressions intentionally support only simple arithmetic, so templates stay safe and easy to understand.

## Run Tests

```bash
python -m pytest
```

## Roadmap

- Add more middle-school topics and difficulty levels
- Support optional worksheet headers such as class, date, and student name
- Add YAML template support
- Add answer-only review sheets
- Add simple template validation reports for non-programmers
- Package the CLI for installation with `pip`

## Contributing

Contributions are welcome. Good first contributions include adding templates, improving documentation, and adding tests for edge cases.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).
