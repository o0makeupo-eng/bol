
from src.conflicts import find_conflicts, has_conflicts, print_conflicts


def test_no_conflicts():
    """Проверка расписания без конфликтов."""

    schedule = [
        {
            "discipline": "Python",
            "day": "Понедельник",
            "pair": 1,
            "room": "101",
            "teacher": "Иванов"
        },
        {
            "discipline": "Математика",
            "day": "Понедельник",
            "pair": 2,
            "room": "101",
            "teacher": "Петров"
        }
    ]

    assert find_conflicts(schedule) == []
    assert has_conflicts(schedule) is False


def test_room_conflict():
    """Проверка конфликта одной аудитории."""

    schedule = [
        {
            "day": "Понедельник",
            "pair": 1,
            "room": "101",
            "teacher": "Иванов"
        },
        {
            "day": "Понедельник",
            "pair": 1,
            "room": "101",
            "teacher": "Петров"
        }
    ]

    conflicts = find_conflicts(schedule)

    assert len(conflicts) == 1
    assert conflicts[0]["type"] == "room"


def test_teacher_conflict():
    """Проверка конфликта одного преподавателя."""

    schedule = [
        {
            "day": "Понедельник",
            "pair": 1,
            "room": "101",
            "teacher": "Иванов"
        },
        {
            "day": "Понедельник",
            "pair": 1,
            "room": "102",
            "teacher": "Иванов"
        }
    ]

    conflicts = find_conflicts(schedule)

    assert len(conflicts) == 1
    assert conflicts[0]["type"] == "teacher"


def test_two_conflicts_at_once():
    """Проверка одновременного конфликта аудитории и преподавателя."""

    schedule = [
        {
            "day": "Понедельник",
            "pair": 1,
            "room": "101",
            "teacher": "Иванов"
        },
        {
            "day": "Понедельник",
            "pair": 1,
            "room": "101",
            "teacher": "Иванов"
        }
    ]

    conflicts = find_conflicts(schedule)

    assert len(conflicts) == 2
    assert {c["type"] for c in conflicts} == {"room", "teacher"}


def test_different_days():
    """Проверка одинаковой аудитории в разные дни."""

    schedule = [
        {
            "day": "Понедельник",
            "pair": 1,
            "room": "101"
        },
        {
            "day": "Вторник",
            "pair": 1,
            "room": "101"
        }
    ]

    assert find_conflicts(schedule) == []


def test_has_conflicts():
    """Проверка функции определения конфликтов."""

    schedule = [
        {"day": "Понедельник", "pair": 1, "room": "101"},
        {"day": "Понедельник", "pair": 1, "room": "101"}
    ]

    assert has_conflicts(schedule) is True


def test_empty_schedule():
    """Проверка пустого расписания."""

    assert find_conflicts([]) == []
    assert has_conflicts([]) is False


def test_print_conflicts(capsys):
    """Проверка вывода конфликтов."""

    schedule = [
        {"day": "Понедельник", "pair": 1, "room": "101"},
        {"day": "Понедельник", "pair": 1, "room": "101"}
    ]

    conflicts = print_conflicts(schedule)

    captured = capsys.readouterr()

    assert len(conflicts) == 1
    assert "Конфликт аудитории 101" in captured.out


def test_print_without_conflicts(capsys):
    """Проверка вывода при отсутствии конфликтов."""

    schedule = []

    conflicts = print_conflicts(schedule)

    captured = capsys.readouterr()

    assert conflicts == []
    assert "Конфликтов не найдено." in captured.out
