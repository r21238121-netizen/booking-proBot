"""
Тесты для FloraBot
"""
import pytest
from bot.models import Bouquet, Order, User, OrderStatus


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
        status=OrderStatus.NEW
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
        username="testuser"
    )
    
    assert user.telegram_id == 123456
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.username == "testuser"


if __name__ == "__main__":
    test_bouquet_model()
    test_order_model()
    test_user_model()
    print("Все тесты пройдены успешно!")