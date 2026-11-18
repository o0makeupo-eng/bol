
"""
Главный модуль проекта «Сетка».

Запуск из корневой папки проекта:
    python -m src.main

Также можно запустить напрямую:
    python src/main.py
"""

import argparse
import csv
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

# Поддержка запуска как пакета и напрямую.
try:
    from .parser import read_requests
    from .validator import validate_requests
    from .scheduler import generate_schedule
    from .conflicts import find_conflicts
    from .exporter import export_schedule, export_schedule_txt

    from .database.connection import Base, engine, SessionLocal
    from .database import db_models
    from .database.repository import (
        get_requests_for_scheduler,
        save_schedule,
    )
except ImportError:
    from parser import read_requests
    from validator import validate_requests
    from scheduler import generate_schedule
    from conflicts import find_conflicts
    from exporter import export_schedule, export_schedule_txt

    from database.connection import Base, engine, SessionLocal
    from database import db_models
    from database.repository import (
        get_requests_for_scheduler,
        save_schedule,
    )


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_DIR / "data" / "requests.csv"
DEFAULT_OUTPUT = PROJECT_DIR / "data" / "output.csv"
DEFAULT_TXT_OUTPUT = PROJECT_DIR / "data" / "output.txt"


def print_unplaced_report(unplaced):
    """Вывести отчёт о неразмещённых занятиях."""
    if not unplaced:
        print("Все занятия успешно распределены.")
        return

    print("\nОтчёт о неразмещённых занятиях:")
    print(f"Неразмещённых занятий: {len(unplaced)}")

    for index, item in enumerate(unplaced, start=1):
        print(f"\n{index}. Дисциплина: {item['discipline']}")
        print(f"   Тип занятия: {item.get('lesson_type')}")
        print(f"   Преподаватель: {item.get('teacher') or 'Не указан'}")
        print(f"   Группа: {item.get('group') or 'Не указана'}")
        print(f"   Причина: {item['reason']}")


def main():
    cli_parser = argparse.ArgumentParser(
        description="Сетка — генератор расписания занятий"
    )

    cli_parser.add_argument(
        "--input",
        default=None,
        help="CSV-файл с заявками. Если не указан, заявки загружаются из БД",
    )

    cli_parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Путь для сохранения расписания CSV",
    )

    cli_parser.add_argument(
        "--txt-output",
        default=str(DEFAULT_TXT_OUTPUT),
        help="Путь для сохранения расписания TXT",
    )

    cli_parser.add_argument(
        "--version",
        action="version",
        version="Сетка 1.0.0",
    )

    args = cli_parser.parse_args()
    db = None

    try:
        # 1. Загружаем заявки.
        if args.input:
            print("Чтение заявок из CSV...")
            requests = read_requests(args.input)
        else:
            print("Подключение к базе данных...")
            Base.metadata.create_all(bind=engine)
            db = SessionLocal()

            print("Загрузка заявок из базы данных...")
            requests = get_requests_for_scheduler(db)

        print(f"Загружено заявок: {len(requests)}")

        # 2. Проверяем входные данные.
        print("Проверка заявок...")
        errors = validate_requests(requests)

        if errors:
            print("Обнаружены ошибки:")
            for error in errors:
                print(f"- {error}")
            return 1

        print("Ошибок во входных данных не найдено.")

        # 3. Генерируем расписание.
        print("Составление расписания...")
        schedule, unplaced = generate_schedule(
            requests,
            return_report=True,
        )

        print(f"Распределено занятий: {len(schedule)}")
        print(f"Не удалось распределить: {len(unplaced)}")

        # 4. Проверяем конфликты.
        print("Проверка конфликтов...")
        conflicts = find_conflicts(schedule)

        if conflicts:
            print("Обнаружены конфликты:")
            for conflict in conflicts:
                print(f"- {conflict['message']}")
            return 1

        print("Конфликтов не найдено.")

        # 5. Выводим отчёт.
        print_unplaced_report(unplaced)

        # 6. Сохраняем расписание в базе данных.
        if db is not None:
            print("Сохранение расписания в базу данных...")
            saved_count = save_schedule(db, schedule)
            print(f"Сохранено занятий в базе данных: {saved_count}")

        # 7. Экспортируем в CSV.
        export_schedule(schedule, args.output)
        print(f"Расписание сохранено в CSV: {args.output}")

        # 8. Экспортируем в TXT.
        export_schedule_txt(schedule, args.txt_output)
        print(f"Расписание сохранено в TXT: {args.txt_output}")

        if unplaced:
            print(
                "\nРасписание сформировано частично. "
                "Проверьте отчёт о неразмещённых занятиях."
            )
        else:
            print("Готово! Расписание успешно создано.")

        return 0

    except (OSError, ValueError, csv.Error, SQLAlchemyError) as error:
        print(f"Ошибка: {error}")
        return 1

    finally:
        if db is not None:
            db.close()


if __name__ == "__main__":
    raise SystemExit(main())