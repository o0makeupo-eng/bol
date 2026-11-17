"""
Модуль составления расписания занятий.

На данном этапе используется простой алгоритм:
каждая заявка размещается в первой свободной паре и аудитории.
Занятия не должны пересекаться по аудитории или преподавателю.

Ожидаемые поля заявки:
    discipline — название дисциплины;
    lesson_type — тип занятия;
    pairs_per_week — количество пар в неделю;
    room — желаемая аудитория (необязательно);
    teacher — преподаватель (необязательно).

При необходимости названия полей можно адаптировать под models.py и parser.py.
"""

DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
PAIRS_PER_DAY = 6
ROOMS = ["101", "102", "103", "205", "206"]


def _get(item, *names, default=None):
    """Получить значение из словаря или объекта."""
    for name in names:
        if isinstance(item, dict) and name in item:
            return item[name]
        if hasattr(item, name):
            return getattr(item, name)
    return default


def _is_slot_free(schedule, day, pair, room, teacher):
    """Проверить, свободны ли аудитория и преподаватель в это время."""
    for lesson in schedule:
        if lesson["day"] != day or lesson["pair"] != pair:
            continue

        if lesson["room"] == room:
            return False

        if teacher is not None and lesson.get("teacher") == teacher:
            return False

    return True


def generate_schedule(requests):
    """
    Составить расписание по списку заявок.

    Args:
        requests: список заявок в виде словарей или объектов.

    Returns:
        list[dict]: список размещённых занятий.

    Raises:
        ValueError: если одну из заявок невозможно разместить.
    """
    schedule = []

    for request in requests:
        discipline = _get(request, "discipline", "subject", "name")
        lesson_type = _get(request, "lesson_type", "type")
        pairs_count = _get(
            request, "pairs_per_week", "pairs", "lessons_per_week", default=1
        )
        preferred_room = _get(request, "room", "classroom")
        teacher = _get(request, "teacher", "teacher_name")

        if discipline is None:
            raise ValueError("В заявке не указана дисциплина.")

        try:
            pairs_count = int(pairs_count)
        except (TypeError, ValueError):
            raise ValueError(
                f"Некорректное количество пар для дисциплины «{discipline}»."
            )

        if pairs_count < 0:
            raise ValueError(
                f"Количество пар для дисциплины «{discipline}» "
                "не может быть отрицательным."
            )

        available_rooms = (
            [str(preferred_room)] if preferred_room is not None else ROOMS
        )

        for _ in range(pairs_count):
            placed = False

            for day in DAYS:
                for pair in range(1, PAIRS_PER_DAY + 1):
                    for room in available_rooms:
                        if _is_slot_free(
                            schedule, day, pair, room, teacher
                        ):
                            schedule.append({
                                "discipline": discipline,
                                "lesson_type": lesson_type,
                                "day": day,
                                "pair": pair,
                                "room": room,
                                "teacher": teacher,
                            })
                            placed = True
                            break

                    if placed:
                        break
                if placed:
                    break

            if not placed:
                raise ValueError(
                    f"Не удалось разместить занятие «{discipline}». "
                    "Свободных пар или аудиторий не осталось."
                )

    return schedule
