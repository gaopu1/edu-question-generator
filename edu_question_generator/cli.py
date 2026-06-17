"""Command-line interface for edu-question-generator."""

from __future__ import annotations

import argparse
from pathlib import Path

from .exporter import export_student_docx, export_teacher_docx
from .generator import QuestionGenerator, TemplateError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="edu-question-generator",
        description="Generate math and physics practice worksheets as DOCX files.",
    )
    parser.add_argument("--subject", help="Subject, for example: math or physics")
    parser.add_argument("--topic", help="Topic, for example: algebra or motion")
    parser.add_argument("--difficulty", help="Difficulty: easy, medium, or hard")
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of questions to generate. Default: 10",
    )
    parser.add_argument(
        "--output-dir",
        default="examples/output",
        help="Directory where DOCX files will be saved.",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Optional worksheet title.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for repeatable worksheets.",
    )
    parser.add_argument(
        "--list-options",
        action="store_true",
        help="Show available subjects, topics, and difficulties.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    generator = QuestionGenerator(random_seed=args.seed)

    if args.list_options:
        _print_options(generator)
        return 0

    missing = [
        name
        for name in ("subject", "topic", "difficulty")
        if getattr(args, name) is None
    ]
    if missing:
        parser.error("Missing required arguments: " + ", ".join(f"--{x}" for x in missing))

    try:
        worksheet = generator.generate(
            subject=args.subject,
            topic=args.topic,
            difficulty=args.difficulty,
            count=args.count,
            title=args.title,
        )
    except (TemplateError, ValueError) as exc:
        parser.exit(2, f"Error: {exc}\n")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    file_base = f"{args.subject}_{args.topic}_{args.difficulty}".replace(" ", "_").lower()
    student_path = export_student_docx(worksheet, output_dir / f"{file_base}_student.docx")
    teacher_path = export_teacher_docx(worksheet, output_dir / f"{file_base}_teacher.docx")

    print(f"Created student worksheet: {student_path}")
    print(f"Created teacher version:   {teacher_path}")
    return 0


def _print_options(generator: QuestionGenerator) -> None:
    print("Available template options:")
    for subject, values in generator.list_options().items():
        print(f"- {subject}")
        print(f"  topics: {', '.join(values['topics'])}")
        print(f"  difficulties: {', '.join(values['difficulties'])}")


if __name__ == "__main__":
    raise SystemExit(main())
