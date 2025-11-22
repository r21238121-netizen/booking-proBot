#!/usr/bin/env python3
"""
Скрипт для запуска FloraBot
"""
import os
import sys
from pathlib import Path

def main():
    # Добавляем директорию проекта в путь Python
    project_dir = Path(__file__).parent
    sys.path.insert(0, str(project_dir))
    
    # Проверяем наличие .env файла
    env_file = project_dir / ".env"
    if not env_file.exists():
        print("⚠️  Файл .env не найден!")
        print("Создайте файл .env с содержимым:")
        print("BOT_TOKEN=ваш_токен_бота_из_Telegram_BotFather")
        print("ADMIN_IDS=123456789,987654321")
        print("DATABASE_URL=sqlite:///./florabot.db")
        return
    
    # Импортируем и запускаем основной модуль бота
    try:
        from bot.main import main as bot_main
        print("🌸 Запуск FloraBot...")
        print("Для остановки бота нажмите Ctrl+C")
        bot_main()
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь, что вы запускаете скрипт из директории проекта")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main()