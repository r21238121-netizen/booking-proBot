from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    """Модель пользователя"""
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: int = Field(unique=True)
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_admin: bool = False
    created_at: str  # В оригинальной модели не было значения по умолчанию