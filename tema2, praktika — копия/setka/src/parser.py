import csv
from pathlib import Path


def read_requests(file_path):
    """
    Читает заявки преподавателей из CSV-файла.
    Возвращает список заявок.
    """

    requests = []

    file_path = Path(file_path)

    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "Дисциплина",
            "Тип занятия",
            "Пар в неделю",
            "Аудитория"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("Неверная структура CSV-файла")

        for row in reader:
            request = {
                "discipline": row["Дисциплина"],
                "lesson_type": row["Тип занятия"],
                "lessons_per_week": int(row["Пар в неделю"]),
                "classroom": row["Аудитория"]
            }

            requests.append(request)

    return requests