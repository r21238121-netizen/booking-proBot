from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum


class OrderStatus(str, Enum):
    """Статусы заказа"""
    NEW = "new"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


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