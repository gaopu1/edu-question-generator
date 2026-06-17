from edu_question_generator.generator import QuestionGenerator


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
