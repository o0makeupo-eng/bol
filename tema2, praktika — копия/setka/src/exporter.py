"""
Экспорт готового расписания в CSV-файл.
"""

import csv
from pathlib import Path


FIELDNAMES = [
    "Дисциплина",
    "Тип занятия",
    "День",
    "Пара",
    "Аудитория",
    "Преподаватель",
]


def _get(lesson, *names, default=""):
    """Получить значение из словаря или объекта."""
    for name in names:
        if isinstance(lesson, dict) and name in lesson:
            value = lesson[name]
            return "" if value is None else value
        if hasattr(lesson, name):
            value = getattr(lesson, name)
            return "" if value is None else value
    return default


def export_schedule(schedule, file_path):
    """
    Сохранить расписание в CSV.

    Args:
        schedule: список занятий (словари или объекты).
        file_path: путь к выходному CSV-файлу.

    Returns:
        Path: путь к созданному файлу.
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open(
        mode="w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for lesson in schedule:
            writer.writerow({
                "Дисциплина": _get(lesson, "discipline", "subject"),
                "Тип занятия": _get(lesson, "lesson_type", "type"),
                "День": _get(lesson, "day", "weekday"),
                "Пара": _get(lesson, "pair", "time_slot"),
                "Аудитория": _get(lesson, "classroom", "room"),
                "Преподаватель": _get(lesson, "teacher", "teacher_name"),
            })

    return file_path
