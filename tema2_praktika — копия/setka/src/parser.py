
import csv
from pathlib import Path


def read_requests(file_path):
    """
    Читает заявки преподавателей из CSV-файла.

    Обязательные поля:
    - discipline — дисциплина;
    - lesson_type — тип занятия;
    - pairs_per_week — количество пар в неделю;
    - room — аудитория;
    - teacher — преподаватель;
    - group — учебная группа.
    """

    requests = []

    file_path = Path(file_path)

    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = [
            "Дисциплина",
            "Тип занятия",
            "Пар в неделю",
            "Аудитория",
            "Преподаватель",
            "Группа"
        ]

        if not reader.fieldnames:
            raise ValueError("CSV-файл пустой или не содержит заголовков")

        missing_columns = [
            column for column in required_columns
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                f"В CSV-файле отсутствуют столбцы: {', '.join(missing_columns)}"
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                request = {
                    "discipline": row["Дисциплина"].strip(),
                    "lesson_type": row["Тип занятия"].strip(),
                    "pairs_per_week": int(row["Пар в неделю"]),
                    "room": row["Аудитория"].strip(),
                    "teacher": row["Преподаватель"].strip(),
                    "group": row["Группа"].strip()
                }

                requests.append(request)

            except (ValueError, AttributeError, KeyError) as error:
                raise ValueError(
                    f"Ошибка в строке {row_number}: {error}"
                )

    return requests