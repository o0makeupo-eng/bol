"""
Проверка конфликтов в расписании.

Модуль поддерживает занятия в виде словарей или объектов с атрибутами.
Для каждого занятия используются поля:
    day       — день недели;
    pair      — номер пары (или time_slot);
    room      — аудитория;
    teacher   — преподаватель (необязательное поле).

Два занятия конфликтуют, если проходят в один день и одну пару и при этом
занимают одну аудиторию или у них совпадает преподаватель.
"""


def _get(item, *names, default=None):
    """Получить значение из словаря или объекта по одному из имён полей."""
    for name in names:
        if isinstance(item, dict) and name in item:
            return item[name]
        if hasattr(item, name):
            return getattr(item, name)
    return default


def _same_time(first, second):
    first_day = _get(first, "day", "weekday")
    second_day = _get(second, "day", "weekday")

    first_pair = _get(first, "pair", "time_slot", "lesson")
    second_pair = _get(second, "pair", "time_slot", "lesson")

    return first_day == second_day and first_pair == second_pair


def find_conflicts(schedule):
    """
    Найти все конфликты в расписании.

    Args:
        schedule: список занятий (словари или объекты).

    Returns:
        list[dict]: найденные конфликты. Каждый элемент содержит:
            type — 'room' или 'teacher';
            first, second — два конфликтующих занятия;
            message — понятное описание конфликта.
    """
    conflicts = []

    for i, first in enumerate(schedule):
        for second in schedule[i + 1:]:
            if not _same_time(first, second):
                continue

            day = _get(first, "day", "weekday", default="неизвестный день")
            pair = _get(first, "pair", "time_slot", "lesson",
                        default="неизвестная пара")

            first_room = _get(first, "room", "classroom")
            second_room = _get(second, "room", "classroom")

            if first_room is not None and first_room == second_room:
                conflicts.append({
                    "type": "room",
                    "first": first,
                    "second": second,
                    "message": (
                        f"Конфликт аудитории {first_room}: "
                        f"{day}, пара {pair}"
                    ),
                })

            first_teacher = _get(first, "teacher", "teacher_name")
            second_teacher = _get(second, "teacher", "teacher_name")

            if (
                first_teacher is not None
                and first_teacher == second_teacher
            ):
                conflicts.append({
                    "type": "teacher",
                    "first": first,
                    "second": second,
                    "message": (
                        f"Конфликт преподавателя {first_teacher}: "
                        f"{day}, пара {pair}"
                    ),
                })

    return conflicts


def has_conflicts(schedule):
    """Вернуть True, если в расписании есть хотя бы один конфликт."""
    return bool(find_conflicts(schedule))


def print_conflicts(schedule):
    """Напечатать найденные конфликты; вернуть их список."""
    conflicts = find_conflicts(schedule)

    if not conflicts:
        print("Конфликтов не найдено.")
        return conflicts

    for conflict in conflicts:
        print(conflict["message"])

    return conflicts
