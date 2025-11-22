from telegram import Update
from telegram.ext import ContextTypes
from bot.models import User
from bot.keyboards import get_main_menu_keyboard, get_admin_menu_keyboard
from bot.config import ADMIN_IDS
from datetime import datetime


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    user_id = user.id
    
    # Проверяем, есть ли пользователь в базе, если нет - создаем
    # Здесь в реальном приложении нужно подключить базу данных
    
    # Определяем, является ли пользователь администратором
    is_admin = user_id in ADMIN_IDS
    
    # Отправляем приветственное сообщение
    welcome_text = (
        f"🌸 Добро пожаловать в FloraBot, {user.first_name}!\n\n"
        "Здесь вы можете:\n"
        "• Просмотреть наш каталог цветов\n"
        "• Сделать заказ с доставкой\n"
        "• Отследить статус ваших заказов\n\n"
        "Для навигации используйте кнопки внизу экрана."
    )
    
    if is_admin:
        await update.message.reply_text(
            welcome_text + "\n\nВы авторизованы как администратор.",
            reply_markup=get_admin_menu_keyboard()
        )
    else:
        await update.message.reply_text(
            welcome_text,
            reply_markup=get_main_menu_keyboard()
        )