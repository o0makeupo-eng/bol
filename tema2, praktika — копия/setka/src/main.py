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

# Поддержка запуска как пакета и напрямую из папки проекта.
try:
    from .parser import read_requests
    from .validator import validate_requests
    from .scheduler import generate_schedule
    from .conflicts import find_conflicts
    from .exporter import export_schedule
except ImportError:
    from parser import read_requests
    from validator import validate_requests
    from scheduler import generate_schedule
    from conflicts import find_conflicts
    from exporter import export_schedule


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_DIR / "data" / "requests.csv"
DEFAULT_OUTPUT = PROJECT_DIR / "data" / "output.csv"


def main():
    parser = argparse.ArgumentParser(
        description="Сетка — генератор расписания занятий"
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Путь к CSV-файлу с заявками"
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Путь для сохранения готового расписания"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Сетка 1.0.0"
    )

    args = parser.parse_args()

    try:
        # 1. Читаем заявки из CSV.
        print("Чтение заявок...")
        requests = read_requests(args.input)
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

        # 3. Составляем расписание.
        print("Составление расписания...")
        schedule = generate_schedule(requests)
        print(f"Распределено занятий: {len(schedule)}")

        # 4. Проверяем расписание на конфликты.
        print("Проверка конфликтов...")
        conflicts = find_conflicts(schedule)

        if conflicts:
            print("Обнаружены конфликты:")
            for conflict in conflicts:
                print(f"- {conflict['message']}")
            return 1

        print("Конфликтов не найдено.")

        # 5. Экспортируем расписание в CSV.
        export_schedule(schedule, args.output)
        print(f"Расписание сохранено в файл: {args.output}")

        print("Готово! Расписание успешно создано.")
        return 0

    except (OSError, ValueError, csv.Error) as error:
        print(f"Ошибка: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
