
import pytest
from src.parser import read_requests


def test_read_requests(tmp_path):
    """Проверяет правильное чтение CSV-файла."""

    csv_file = tmp_path / "requests.csv"

    csv_file.write_text(
        "Дисциплина,Тип занятия,Пар в неделю,Аудитория\n"
        "Python,Лекция,2,101\n"
        "Базы данных,Практика,2,205\n",
        encoding="utf-8"
    )

    result = read_requests(csv_file)

    assert len(result) == 2
    assert result[0]["discipline"] == "Python"
    assert result[0]["lesson_type"] == "Лекция"
    assert result[0]["lessons_per_week"] == 2
    assert result[0]["classroom"] == "101"


def test_invalid_csv_structure(tmp_path):
    """Проверяет обработку неправильных заголовков CSV."""

    csv_file = tmp_path / "wrong.csv"

    csv_file.write_text(
        "Название,Количество\nPython,2\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError):
        read_requests(csv_file)


def test_invalid_lessons_count(tmp_path):
    """Проверяет обработку некорректного количества пар."""

    csv_file = tmp_path / "wrong_number.csv"

    csv_file.write_text(
        "Дисциплина,Тип занятия,Пар в неделю,Аудитория\n"
        "Python,Лекция,abc,101\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError):
        read_requests(csv_file)
