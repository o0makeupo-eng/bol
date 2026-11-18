
from sqlalchemy.orm import Session
from .db_models import Teacher, Group, Discipline, Room, Request, Lesson


# -------------------------
# Преподаватели
# -------------------------

def add_teacher(db: Session, name: str):
    teacher = Teacher(name=name)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


def get_teachers(db: Session):
    return db.query(Teacher).all()


def delete_teacher(db: Session, teacher_id: int):
    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id
    ).first()

    if teacher is None:
        return False

    db.delete(teacher)
    db.commit()
    return True


# -------------------------
# Учебные группы
# -------------------------

def add_group(db: Session, name: str):
    group = Group(name=name)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def get_groups(db: Session):
    return db.query(Group).all()


# -------------------------
# Дисциплины
# -------------------------

def add_discipline(db: Session, name: str):
    discipline = Discipline(name=name)
    db.add(discipline)
    db.commit()
    db.refresh(discipline)
    return discipline


def get_disciplines(db: Session):
    return db.query(Discipline).all()


# -------------------------
# Аудитории
# -------------------------

def add_room(db: Session, number: str):
    room = Room(number=number)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


def get_rooms(db: Session):
    return db.query(Room).all()

import csv
from pathlib import Path

from .db_models import Request


def import_requests_from_csv(db: Session, file_path):
    """Импортирует заявки из CSV в базу данных."""

    imported = 0

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "Дисциплина",
            "Тип занятия",
            "Пар в неделю",
            "Аудитория",
            "Преподаватель",
            "Группа"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("В CSV отсутствуют необходимые столбцы")

        for row in reader:
            discipline_name = row["Дисциплина"].strip()
            teacher_name = row["Преподаватель"].strip()
            group_name = row["Группа"].strip()
            room_number = row["Аудитория"].strip()
            lesson_type = row["Тип занятия"].strip()
            pairs_per_week = int(row["Пар в неделю"])

            if not all([
                discipline_name,
                teacher_name,
                group_name,
                room_number,
                lesson_type
            ]) or pairs_per_week <= 0:
                raise ValueError("Обнаружена некорректная заявка")

            # Находим или создаём преподавателя
            teacher = db.query(Teacher).filter_by(
                name=teacher_name
            ).first()

            if teacher is None:
                teacher = Teacher(name=teacher_name)
                db.add(teacher)
                db.flush()

            # Находим или создаём дисциплину
            discipline = db.query(Discipline).filter_by(
                name=discipline_name
            ).first()

            if discipline is None:
                discipline = Discipline(name=discipline_name)
                db.add(discipline)
                db.flush()

            # Находим или создаём группу
            group = db.query(Group).filter_by(
                name=group_name
            ).first()

            if group is None:
                group = Group(name=group_name)
                db.add(group)
                db.flush()

            # Находим или создаём аудиторию
            room = db.query(Room).filter_by(
                number=room_number
            ).first()

            if room is None:
                room = Room(number=room_number)
                db.add(room)
                db.flush()

            # Проверяем, не импортирована ли заявка ранее
            existing = db.query(Request).filter_by(
                teacher_id=teacher.id,
                discipline_id=discipline.id,
                group_id=group.id,
                room_id=room.id,
                lesson_type=lesson_type,
                pairs_per_week=pairs_per_week
            ).first()

            if existing is not None:
                continue

            request = Request(
                teacher_id=teacher.id,
                discipline_id=discipline.id,
                group_id=group.id,
                room_id=room.id,
                lesson_type=lesson_type,
                pairs_per_week=pairs_per_week
            )

            db.add(request)
            imported += 1

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return imported


def get_requests(db: Session):
    """Возвращает все заявки из базы данных."""
    return db.query(Request).all()



def get_requests_for_scheduler(db: Session):
    """Преобразует заявки из БД в формат планировщика."""

    requests = db.query(Request).all()
    result = []

    for request in requests:
        teacher = db.get(Teacher, request.teacher_id)
        discipline = db.get(Discipline, request.discipline_id)
        group = db.get(Group, request.group_id)
        room = db.get(Room, request.room_id)

        if not all([teacher, discipline, group, room]):
            raise ValueError(
                f"Заявка №{request.id} содержит отсутствующие связи."
            )

        result.append({
            "discipline": discipline.name,
            "lesson_type": request.lesson_type,
            "pairs_per_week": request.pairs_per_week,
            "room": room.number,
            "teacher": teacher.name,
            "group": group.name
        })

    return result


def save_schedule(db: Session, schedule):
    """Сохраняет новое расписание в базе данных."""

    requests = db.query(Request).all()

    # Создаём соответствие между заявками и их параметрами.
    request_map = {}

    for request in requests:
        teacher = db.get(Teacher, request.teacher_id)
        discipline = db.get(Discipline, request.discipline_id)
        group = db.get(Group, request.group_id)
        room = db.get(Room, request.room_id)

        if not all([teacher, discipline, group, room]):
            raise ValueError(
                f"Заявка №{request.id} содержит отсутствующие связи."
            )

        key = (
            discipline.name,
            request.lesson_type,
            teacher.name,
            group.name,
            room.number
        )

        request_map[key] = request

    try:
        # Удаляем предыдущее расписание.
        db.query(Lesson).delete(synchronize_session=False)

        for lesson in schedule:
            key = (
                lesson["discipline"],
                lesson["lesson_type"],
                lesson["teacher"],
                lesson["group"],
                str(lesson["room"])
            )

            request = request_map.get(key)

            if request is None:
                raise ValueError(
                    f"Не найдена заявка для занятия "
                    f"«{lesson['discipline']}»."
                )

            db.add(Lesson(
                request_id=request.id,
                day=lesson["day"],
                pair=int(lesson["pair"]),
                room_id=request.room_id
            ))

        db.commit()

    except Exception:
        db.rollback()
        raise

    return len(schedule)
