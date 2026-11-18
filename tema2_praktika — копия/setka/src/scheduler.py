
"""
Модуль составления расписания занятий.

Учитывает конфликты:
- аудиторий;
- преподавателей;
- учебных групп.

Поддерживает отчёт о неразмещённых занятиях.
"""

DAYS = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
]

PAIRS_PER_DAY = 5

ROOMS = ["101", "102", "103", "205", "206"]


def _get(item, *names, default=None):
    """Получить значение из словаря или объекта."""
    for name in names:
        if isinstance(item, dict) and name in item:
            return item[name]

        if hasattr(item, name):
            return getattr(item, name)

    return default


def _is_slot_free(schedule, day, pair, room, teacher, group):
    """
    Проверить, свободны ли аудитория,
    преподаватель и группа в указанное время.
    """
    for lesson in schedule:
        if lesson["day"] != day or lesson["pair"] != pair:
            continue

        # Проверка аудитории
        if lesson["room"] == room:
            return False

        # Проверка преподавателя
        if teacher and lesson.get("teacher") == teacher:
            return False

        # Проверка учебной группы
        if group and lesson.get("group") == group:
            return False

    return True


def generate_schedule(requests, return_report=False):
    """
    Составить расписание по списку заявок.

    Args:
        requests: список заявок в виде словарей или объектов.
        return_report: если True, вернуть также отчёт
                      о неразмещённых занятиях.

    Returns:
        list[dict]: расписание, если return_report=False.
        tuple: (расписание, отчёт), если return_report=True.

    Raises:
        ValueError: если занятие невозможно разместить
                    и return_report=False.
    """

    schedule = []
    unplaced = []

    for request in requests:

        discipline = _get(request, "discipline", "subject", "name")
        lesson_type = _get(request, "lesson_type", "type")

        pairs_count = _get(
            request,
            "pairs_per_week",
            "pairs",
            "lessons_per_week",
            default=1
        )

        preferred_room = _get(request, "room", "classroom")
        teacher = _get(request, "teacher", "teacher_name")
        group = _get(request, "group", "group_name")

        # Проверка дисциплины
        if not discipline:
            raise ValueError("В заявке не указана дисциплина.")

        # Проверка количества пар
        try:
            pairs_count = int(pairs_count)
        except (TypeError, ValueError):
            raise ValueError(
                f"Некорректное количество пар "
                f"для дисциплины «{discipline}»."
            )

        if pairs_count <= 0:
            raise ValueError(
                f"Количество пар для дисциплины «{discipline}» "
                "должно быть положительным."
            )

        # Очистка значений преподавателя и группы
        teacher = str(teacher).strip() if teacher else None
        group = str(group).strip() if group else None

        if not teacher:
            teacher = None

        if not group:
            group = None

        # Выбор аудитории
        available_rooms = (
            [str(preferred_room)]
            if preferred_room
            else ROOMS
        )

        placed_count = 0

        # Размещение занятий
        for _ in range(pairs_count):

            placed = False

            for day in DAYS:

                for pair in range(1, PAIRS_PER_DAY + 1):

                    for room in available_rooms:

                        if _is_slot_free(
                            schedule,
                            day,
                            pair,
                            room,
                            teacher,
                            group
                        ):
                            schedule.append({
                                "discipline": discipline,
                                "lesson_type": lesson_type,
                                "day": day,
                                "pair": pair,
                                "room": room,
                                "teacher": teacher,
                                "group": group
                            })

                            placed = True
                            placed_count += 1
                            break

                    if placed:
                        break

                if placed:
                    break

            # Если занятие не удалось разместить
            if not placed:
                unplaced.append({
                    "discipline": discipline,
                    "lesson_type": lesson_type,
                    "teacher": teacher,
                    "group": group,
                    "room": str(preferred_room)
                    if preferred_room else None,
                    "reason": (
                        "Не удалось найти свободное время "
                        "и аудиторию без конфликтов."
                    )
                })

        # Сводная информация по заявке
        if placed_count < pairs_count:
            unplaced_count = pairs_count - placed_count

            # В отчёте фиксируем количество
            # неразмещённых занятий по заявке.
            for item in unplaced[-unplaced_count:]:
                item["requested_pairs"] = pairs_count
                item["placed_pairs"] = placed_count
                item["unplaced_pairs"] = unplaced_count

    # Если отчёт запрошен, возвращаем оба результата
    if return_report:
        return schedule, unplaced

    # Старое поведение сохраняется для совместимости
    if unplaced:
        first = unplaced[0]

        raise ValueError(
            f"Не удалось разместить занятие "
            f"«{first['discipline']}». "
            "Свободных пар или аудиторий не осталось."
        )

    return schedule