from pathlib import Path

from edu_question_generator.exporter import export_student_docx, export_teacher_docx
from edu_question_generator.generator import QuestionGenerator


def test_export_docx_files(tmp_path: Path):
    generator = QuestionGenerator(random_seed=3)
    worksheet = generator.generate("physics", "motion", "easy", 2)

    student_path = export_student_docx(worksheet, tmp_path / "student.docx")
    teacher_path = export_teacher_docx(worksheet, tmp_path / "teacher.docx")

    assert student_path.exists()
    assert teacher_path.exists()
    assert student_path.stat().st_size > 0
    assert teacher_path.stat().st_size > 0
