
import pytest
from src.scheduler import generate_schedule


def test_generate_schedule():
    """Проверка создания расписания."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "pairs_per_week": 2
        }
    ]

    schedule = generate_schedule(requests)

    assert len(schedule) == 2
    assert schedule[0]["discipline"] == "Python"


def test_schedule_contains_required_fields():
    """Проверка наличия необходимых полей."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "pairs_per_week": 1
        }
    ]

    schedule = generate_schedule(requests)

    lesson = schedule[0]

    assert "discipline" in lesson
    assert "lesson_type" in lesson
    assert "day" in lesson
    assert "pair" in lesson
    assert "room" in lesson
    assert "teacher" in lesson


def test_different_lessons_do_not_conflict():
    """Проверка отсутствия конфликтов аудиторий."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "pairs_per_week": 1
        },
        {
            "discipline": "Математика",
            "lesson_type": "Практика",
            "pairs_per_week": 1
        }
    ]

    schedule = generate_schedule(requests)

    first = schedule[0]
    second = schedule[1]

    assert not (
        first["day"] == second["day"]
        and first["pair"] == second["pair"]
        and first["room"] == second["room"]
    )


def test_teacher_cannot_have_two_lessons_at_once():
    """Проверка отсутствия пересечения занятий преподавателя."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "pairs_per_week": 1,
            "teacher": "Иванов"
        },
        {
            "discipline": "Базы данных",
            "lesson_type": "Практика",
            "pairs_per_week": 1,
            "teacher": "Иванов"
        }
    ]

    schedule = generate_schedule(requests)

    first = schedule[0]
    second = schedule[1]

    assert not (
        first["day"] == second["day"]
        and first["pair"] == second["pair"]
    )


def test_zero_pairs():
    """Проверка заявки с нулевым количеством пар."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "pairs_per_week": 0
        }
    ]

    schedule = generate_schedule(requests)

    assert schedule == []


def test_negative_pairs():
    """Проверка отрицательного количества пар."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "pairs_per_week": -1
        }
    ]

    with pytest.raises(ValueError):
        generate_schedule(requests)


def test_invalid_pairs_count():
    """Проверка некорректного количества пар."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "pairs_per_week": "abc"
        }
    ]

    with pytest.raises(ValueError):
        generate_schedule(requests)


def test_missing_discipline():
    """Проверка отсутствия названия дисциплины."""

    requests = [
        {
            "lesson_type": "Лекция",
            "pairs_per_week": 1
        }
    ]

    with pytest.raises(ValueError):
        generate_schedule(requests)
