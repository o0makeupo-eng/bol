
from src.validator import validate_requests, is_valid


def test_valid_request():
    """Проверка правильной заявки."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "lessons_per_week": 2,
            "classroom": "101"
        }
    ]

    assert validate_requests(requests) == []
    assert is_valid(requests) is True


def test_empty_requests():
    """Проверка пустого списка заявок."""

    assert "Список заявок пуст." in validate_requests([])


def test_missing_discipline():
    """Проверка отсутствующей дисциплины."""

    requests = [
        {
            "discipline": "",
            "lesson_type": "Лекция",
            "lessons_per_week": 2,
            "classroom": "101"
        }
    ]

    assert any("не указана дисциплина" in error
               for error in validate_requests(requests))


def test_missing_lesson_type():
    """Проверка отсутствующего типа занятия."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "",
            "lessons_per_week": 2,
            "classroom": "101"
        }
    ]

    assert any("не указан тип занятия" in error
               for error in validate_requests(requests))


def test_invalid_lessons_count():
    """Проверка отрицательного количества пар."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "lessons_per_week": -2,
            "classroom": "101"
        }
    ]

    assert any("количество пар" in error
               for error in validate_requests(requests))


def test_missing_classroom():
    """Проверка отсутствующей аудитории."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "lessons_per_week": 2,
            "classroom": ""
        }
    ]

    assert any("не указана аудитория" in error
               for error in validate_requests(requests))


def test_request_not_dict():
    """Проверка заявки неправильного типа."""

    requests = ["Python"]

    assert any("должны быть представлены словарём" in error
               for error in validate_requests(requests))


def test_zero_lessons_is_valid():
    """Проверка допустимого нулевого количества пар."""

    requests = [
        {
            "discipline": "Python",
            "lesson_type": "Лекция",
            "lessons_per_week": 0,
            "classroom": "101"
        }
    ]

    assert is_valid(requests) is True
