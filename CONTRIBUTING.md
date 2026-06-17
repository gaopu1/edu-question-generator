# Contributing

Thanks for helping improve `edu-question-generator`.

This project is intentionally simple and beginner-friendly. Contributions that keep it readable are especially welcome.

## Good First Contributions

- Add new JSON question templates.
- Improve wording in generated answers.
- Add tests for new topics or edge cases.
- Improve README or docs.
- Report confusing setup steps.

## Local Development

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest
```

Try the CLI:

```bash
python -m edu_question_generator.cli --list-options
python -m edu_question_generator.cli --subject math --topic algebra --difficulty easy --count 5
```

## Template Guidelines

- Keep prompts short and classroom-friendly.
- Use clear variable names such as `length`, `time`, or `mass`.
- Keep formulas to simple arithmetic.
- Make answers explain the steps, not only the final result.
- Prefer values that produce clean whole-number answers.

## Pull Request Checklist

- Tests pass with `python -m pytest`.
- New templates have unique `id` values.
- Documentation is updated when behavior changes.
- Changes remain small and easy to review.

## Code Style

- Use readable Python.
- Prefer dataclasses and simple functions.
- Avoid adding large dependencies unless they clearly help teachers use the tool.
