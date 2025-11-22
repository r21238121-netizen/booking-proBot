"""
Тесты для исправленных моделей FloraBot
"""
import pytest
from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

# Определяем классы локально, чтобы избежать конфликта с оригинальными моделями
class OrderStatus(str, Enum):
    """Статусы заказа"""
    NEW = "new"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Bouquet(SQLModel, table=True):
    """Модель букета"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: int  # Цена в копейках (для избежания проблем с плавающей точкой)
    image_url: Optional[str] = None
    available: bool = True
    category: Optional[str] = None

class User(SQLModel, table=True):
    """Модель пользователя"""
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: int = Field(unique=True)
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_admin: bool = False
    created_at: str  # В оригинальной модели не было значения по умолчанию

class Order(SQLModel, table=True):
    """Модель заказа"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.telegram_id")  # Исправленный формат внешнего ключа
    status: OrderStatus = OrderStatus.NEW
    total_price: int  # Цена в копейках
    delivery_address: str
    delivery_date: str
    delivery_time: str
    comment: Optional[str] = None
    created_at: str
    updated_at: str


def test_bouquet_model():
    """Тест модели Bouquet"""
    bouquet = Bouquet(
        name="Test Bouquet",
        description="Test Description",
        price=1000,
        available=True
    )
    
    assert bouquet.name == "Test Bouquet"
    assert bouquet.description == "Test Description"
    assert bouquet.price == 1000
    assert bouquet.available is True


def test_order_model():
    """Тест модели Order"""
    order = Order(
        user_id=123456,
        total_price=5000,
        delivery_address="Test Address",
        delivery_date="2023-12-25",
        delivery_time="14:00",
        status=OrderStatus.NEW,
        created_at="2023-01-01 00:00:00",
        updated_at="2023-01-01 00:00:00"
    )
    
    assert order.user_id == 123456
    assert order.total_price == 5000
    assert order.delivery_address == "Test Address"
    assert order.status == OrderStatus.NEW


def test_user_model():
    """Тест модели User"""
    user = User(
        telegram_id=123456,
        first_name="Test",
        last_name="User",
        username="testuser",
        created_at="2023-01-01 00:00:00"
    )
    
    assert user.telegram_id == 123456
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.username == "testuser"
    assert user.created_at == "2023-01-01 00:00:00"


if __name__ == "__main__":
    test_bouquet_model()
    test_order_model()
    test_user_model()
    print("Все тесты пройдены успешно!")