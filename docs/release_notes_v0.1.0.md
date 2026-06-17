# Release Notes: v0.1.0

`edu-question-generator` v0.1.0 is the first polished open-source release.

## Highlights

- Generate middle-school math and physics practice worksheets from JSON templates.
- Export a student worksheet without answers.
- Export a teacher version with worked answers.
- Use a simple command-line interface.
- Run fully locally with no paid APIs.
- Install with standard Python project metadata in `pyproject.toml`.

## Included Templates

The release includes sample templates for:

- math algebra
- math geometry
- math ratios
- math fractions
- math percentages
- physics motion
- physics density
- physics electricity
- physics forces
- physics energy
- physics pressure

## Documentation

- English README
- Chinese README
- Beginner usage guide
- Contribution guide
- Changelog
- GitHub issue templates

## Testing

The test suite covers:

- worksheet generation
- default template loading
- JSON template file loading
- safe formula evaluation
- DOCX student and teacher exports

GitHub Actions now runs `python -m pytest` automatically on push and pull request.
