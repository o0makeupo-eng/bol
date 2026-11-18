
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Корневая папка проекта
BASE_DIR = Path(__file__).resolve().parents[2]

# Путь к базе данных
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_DIR / 'setka.db'}"

# Создание подключения к базе данных
engine = create_engine(
    DATABASE_URL,
    echo=False
)

# Создание фабрики сессий
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Базовый класс для моделей таблиц
Base = declarative_base()


def get_db():
    """Создаёт сессию для работы с базой данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
