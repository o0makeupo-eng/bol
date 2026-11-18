
from sqlalchemy import Column, Integer, String, ForeignKey
from .connection import Base


class Teacher(Base):
    """Преподаватели."""
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


class Group(Base):
    """Учебные группы."""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)


class Discipline(Base):
    """Учебные дисциплины."""
    __tablename__ = "disciplines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)


class Room(Base):
    """Аудитории."""
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(20), nullable=False, unique=True)


class Request(Base):
    """Заявки преподавателей."""
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    discipline_id = Column(Integer, ForeignKey("disciplines.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    lesson_type = Column(String(50), nullable=False)
    pairs_per_week = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"))


class Lesson(Base):
    """Сформированные занятия."""
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    day = Column(String(20), nullable=False)
    pair = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"))
