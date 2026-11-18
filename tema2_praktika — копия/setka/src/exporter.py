"""
Модуль экспорта расписания в CSV и TXT.
"""

import csv
from pathlib import Path


def export_schedule(schedule, file_path):
    """Экспорт расписания в CSV."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "Дисциплина",
        "Тип занятия",
        "День",
        "Пара",
        "Аудитория",
        "Преподаватель",
        "Группа",
    ]

    with file_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for lesson in schedule:
            writer.writerow({
                "Дисциплина": lesson.get("discipline", ""),
                "Тип занятия": lesson.get("lesson_type", ""),
                "День": lesson.get("day", ""),
                "Пара": lesson.get("pair", ""),
                "Аудитория": lesson.get("room", ""),
                "Преподаватель": lesson.get("teacher", ""),
                "Группа": lesson.get("group", ""),
            })


def export_schedule_txt(schedule, file_path):
    """Экспорт расписания в удобный текстовый файл."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        file.write("РАСПИСАНИЕ ЗАНЯТИЙ\n")
        file.write("=" * 50 + "\n\n")

        if not schedule:
            file.write("Расписание пустое.\n")
            return

        for lesson in schedule:
            file.write(
                f"Дисциплина: {lesson.get('discipline', '')}\n"
                f"Тип занятия: {lesson.get('lesson_type', '')}\n"
                f"День: {lesson.get('day', '')}\n"
                f"Пара: {lesson.get('pair', '')}\n"
                f"Аудитория: {lesson.get('room', '')}\n"
                f"Преподаватель: {lesson.get('teacher', '')}\n"
                f"Группа: {lesson.get('group', '')}\n"
            )
            file.write("-" * 50 + "\n")