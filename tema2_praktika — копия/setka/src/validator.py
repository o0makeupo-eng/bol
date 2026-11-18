
"""
Проверка корректности заявок преподавателей
перед составлением расписания.
"""


def validate_requests(requests):
    """
    Проверяет список заявок.

    Обязательные поля:
    discipline, lesson_type, pairs_per_week,
    room, teacher, group.

    Возвращает список ошибок.
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
            "pairs_per_week",
            request.get("lessons_per_week")
        )

        classroom = request.get(
            "room",
            request.get("classroom")
        )

        teacher = request.get("teacher")
        group = request.get("group")

        # Проверка дисциплины
        if not isinstance(discipline, str) or not discipline.strip():
            errors.append(
                f"Заявка №{index}: не указана дисциплина."
            )

        # Проверка типа занятия
        if not isinstance(lesson_type, str) or not lesson_type.strip():
            errors.append(
                f"Заявка №{index}: не указан тип занятия."
            )

        # Проверка количества пар
        try:
            pairs_number = int(pairs)

            if isinstance(pairs, bool) or pairs_number <= 0:
                raise ValueError

        except (TypeError, ValueError):
            errors.append(
                f"Заявка №{index}: количество пар должно быть "
                "положительным целым числом."
            )

        # Проверка аудитории
        if classroom is None or not str(classroom).strip():
            errors.append(
                f"Заявка №{index}: не указана аудитория."
            )

        # Проверка преподавателя
        if not isinstance(teacher, str) or not teacher.strip():
            errors.append(
                f"Заявка №{index}: не указан преподаватель."
            )

        # Проверка учебной группы
        if not isinstance(group, str) or not group.strip():
            errors.append(
                f"Заявка №{index}: не указана учебная группа."
            )

    return errors


def is_valid(requests):
    """Вернуть True, если все заявки корректны."""

    return len(validate_requests(requests)) == 0
