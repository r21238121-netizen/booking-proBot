from sqlmodel import SQLModel, create_engine, Session
from .config import DATABASE_URL

# Создание движка базы данных
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Создание таблиц в базе данных"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Получение сессии базы данных"""
    with Session(engine) as session:
        yield session