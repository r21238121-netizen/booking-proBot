# run.py
import asyncio
import sys
import os

# Добавляем текущую папку в PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from shared.database import init_db
from bot.main import start_bot
from backend.main import start_backend
from backend.scheduler import start_scheduler

async def main():
    # Инициализация БД
    init_db()
    print("✅ База данных готова")

    # Запуск компонентов
    await asyncio.gather(
        start_bot(),
        start_backend(),
        start_scheduler()
    )

if __name__ == "__main__":
    print("🚀 Запуск Booking Pro...")
    asyncio.run(main())