
"""
Проверка конфликтов в расписании.

Проверяет:
- совпадение аудиторий;
- совпадение преподавателей;
- совпадение учебных групп.

Конфликт возникает, если занятия проходят
в один день и одну пару.
"""


def _get(item, *names, default=None):
    """Получить значение из словаря или объекта."""

    for name in names:
        if isinstance(item, dict) and name in item:
            return item[name]

        if hasattr(item, name):
            return getattr(item, name)

    return default


def _same_time(first, second):
    """Проверить, совпадают ли день и номер пары."""

    first_day = _get(first, "day", "weekday")
    second_day = _get(second, "day", "weekday")

    first_pair = _get(first, "pair", "time_slot", "lesson")
    second_pair = _get(second, "pair", "time_slot", "lesson")

    return (
        first_day == second_day
        and first_pair == second_pair
    )


def find_conflicts(schedule):
    """
    Найти все конфликты в расписании.

    Проверяются аудитории, преподаватели и группы.
    """

    conflicts = []

    for i, first in enumerate(schedule):
        for second in schedule[i + 1:]:

            if not _same_time(first, second):
                continue

            day = _get(first, "day", "weekday")
            pair = _get(first, "pair", "time_slot", "lesson")

            first_room = _get(first, "room", "classroom")
            second_room = _get(second, "room", "classroom")

            first_teacher = _get(
                first, "teacher", "teacher_name"
            )
            second_teacher = _get(
                second, "teacher", "teacher_name"
            )

            first_group = _get(first, "group", "group_name")
            second_group = _get(second, "group", "group_name")

            # Проверка аудитории
            if (
                first_room
                and second_room
                and str(first_room).strip() == str(second_room).strip()
            ):
                conflicts.append({
                    "type": "room",
                    "first": first,
                    "second": second,
                    "message": (
                        f"Конфликт аудитории {first_room}: "
                        f"{day}, пара {pair}"
                    )
                })

            # Проверка преподавателя
            if (
                first_teacher
                and second_teacher
                and str(first_teacher).strip()
                == str(second_teacher).strip()
            ):
                conflicts.append({
                    "type": "teacher",
                    "first": first,
                    "second": second,
                    "message": (
                        f"Конфликт преподавателя {first_teacher}: "
                        f"{day}, пара {pair}"
                    )
                })

            # Проверка учебной группы
            if (
                first_group
                and second_group
                and str(first_group).strip()
                == str(second_group).strip()
            ):
                conflicts.append({
                    "type": "group",
                    "first": first,
                    "second": second,
                    "message": (
                        f"Конфликт учебной группы {first_group}: "
                        f"{day}, пара {pair}"
                    )
                })

    return conflicts


def has_conflicts(schedule):
    """Проверить, есть ли конфликты."""

    return bool(find_conflicts(schedule))


def print_conflicts(schedule):
    """Вывести найденные конфликты."""

    conflicts = find_conflicts(schedule)

    if not conflicts:
        print("Конфликтов не найдено.")
        return conflicts

    for conflict in conflicts:
        print(conflict["message"])

    return conflicts