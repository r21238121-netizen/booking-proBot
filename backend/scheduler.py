# backend/scheduler.py
import asyncio
import sqlite3
from datetime import datetime, timedelta
from bot.main import bot
from .utils import get_next_hour_exact

DB_FILE = "data.db"

def get_db():
    return sqlite3.connect(DB_FILE)

async def send_reminders():
    """Отправляет напоминания за 3 часа до записи"""
    while True:
        now = datetime.now()
        target = get_next_hour_exact(now, 3)
        target_str = target.strftime("%Y-%m-%dT%H:00")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT client_id, master_id, slot FROM bookings
            WHERE slot LIKE ? AND reminder_sent = 0
        """, (target_str + "%",))
        bookings = cur.fetchall()

        for client_id, master_id, slot in bookings:
            try:
                # Получаем имя мастера
                cur.execute("SELECT name FROM masters WHERE user_id = ?", (master_id,))
                master = cur.fetchone()
                master_name = master[0] if master else "Мастер"
                slot_time = datetime.fromisoformat(slot).strftime("%d.%m в %H:%M")
                await bot.send_message(
                    client_id,
                    f"⏱️ Напоминаем!\n"
                    f"Вы записаны к {master_name} сегодня {slot_time}.\n"
                    f"Адрес уточнит мастер."
                )
                # Отмечаем, что напоминание отправлено
                cur.execute("UPDATE bookings SET reminder_sent = 1 WHERE client_id = ? AND slot = ?", (client_id, slot))
                conn.commit()
            except Exception as e:
                print(f"Ошибка отправки напоминания: {e}")
        conn.close()
        await asyncio.sleep(60)  # проверка раз в минуту

async def send_review_requests():
    """Отправляет запрос на оценку через 1 час после записи"""
    while True:
        now = datetime.now()
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT client_id, master_id FROM bookings
            WHERE datetime(slot) < datetime(?) 
            AND review_asked = 0
        """, (now.isoformat(),))
        bookings = cur.fetchall()

        for client_id, master_id in bookings:
            try:
                await bot.send_message(
                    client_id,
                    "Спасибо, что были у нас! ❤️\n"
                    "Пожалуйста, оцените визит от 1 до 5 ⭐\n"
                    "(Просто отправьте число: 1, 2, 3, 4 или 5)"
                )
                cur.execute("UPDATE bookings SET review_asked = 1 WHERE client_id = ?", (client_id,))
                conn.commit()
            except Exception as e:
                print(f"Ошибка запроса отзыва: {e}")
        conn.close()
        await asyncio.sleep(300)  # раз в 5 минут

async def start_scheduler():
    """Запуск всех фоновых задач"""
    await asyncio.gather(
        send_reminders(),
        send_review_requests()
    )