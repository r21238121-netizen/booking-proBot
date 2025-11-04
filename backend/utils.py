# backend/utils.py
from datetime import datetime, timedelta

def generate_slots_for_week():
    """Генерирует все возможные слоты на 14 дней вперёд (10, 12, 15, 18)"""
    slots = []
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    start_date = now.replace(hour=0)

    for day in range(14):  # 14 дней вперёд
        date = start_date + timedelta(days=day)
        for hour in [10, 12, 15, 18]:
            slot = date.replace(hour=hour)
            if slot > now:
                slots.append(slot.isoformat())
    return slots

def get_next_hour_exact(dt: datetime, hours: int) -> datetime:
    """Возвращает точное время через N часов (округлённое до часа)"""
    return (dt + timedelta(hours=hours)).replace(minute=0, second=0, microsecond=0)