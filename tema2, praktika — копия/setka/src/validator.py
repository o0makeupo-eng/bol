"""
Проверка корректности заявок преподавателей перед составлением расписания.
"""


def validate_requests(requests):
    """
    Проверяет список заявок.

    Поддерживает словари с полями:
    discipline, lesson_type, lessons_per_week / pairs_per_week,
    classroom / room.

    Возвращает список сообщений об ошибках.
    Если список пустой, все заявки прошли проверку.
    """
    errors = []

    if not requests:
        errors.append("Список заявок пуст.")
        return errors

    for index, request in enumerate(requests, start=1):
        if not isinstance(request, dict):
            errors.append(
                f"Заявка №{index}: данные должны быть представлены словарём."
            )
            continue

        discipline = request.get("discipline")
        lesson_type = request.get("lesson_type")
        pairs = request.get(
            "lessons_per_week",
            request.get("pairs_per_week")
        )
        classroom = request.get("classroom", request.get("room"))

        if not isinstance(discipline, str) or not discipline.strip():
            errors.append(
                f"Заявка №{index}: не указана дисциплина."
            )

        if not isinstance(lesson_type, str) or not lesson_type.strip():
            errors.append(
                f"Заявка №{index}: не указан тип занятия."
            )

        try:
            pairs_number = int(pairs)
            if isinstance(pairs, bool) or pairs_number < 0:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(
                f"Заявка №{index}: количество пар должно быть "
                "целым неотрицательным числом."
            )

        if classroom is None or not str(classroom).strip():
            errors.append(
                f"Заявка №{index}: не указана аудитория."
            )

    return errors


def is_valid(requests):
    """Вернуть True, если все заявки корректны."""
    return len(validate_requests(requests)) == 0
