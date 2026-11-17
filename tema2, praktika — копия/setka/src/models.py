from dataclasses import dataclass


@dataclass
class LessonRequest:
    """Заявка преподавателя."""

    discipline: str
    lesson_type: str
    lessons_per_week: int
    classroom: str


@dataclass
class Lesson:
    """Занятие в расписании."""

    discipline: str
    lesson_type: str
    day: str
    pair: int
    classroom: str