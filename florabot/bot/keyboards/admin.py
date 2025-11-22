from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_admin_menu_keyboard():
    """Меню для администраторов"""
    keyboard = [
        [KeyboardButton("📋 Новые заказы"), KeyboardButton("📝 Управление каталогом")],
        [KeyboardButton("📊 Статистика"), KeyboardButton("⚙️ Настройки")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)