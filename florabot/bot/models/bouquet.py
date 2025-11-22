from sqlmodel import SQLModel, Field
from typing import Optional


class Bouquet(SQLModel, table=True):
    """Модель букета"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: int  # Цена в копейках (для избежания проблем с плавающей точкой)
    image_url: Optional[str] = None
    available: bool = True
    category: Optional[str] = None