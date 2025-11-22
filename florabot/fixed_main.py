import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from bot.config import BOT_TOKEN
from bot.database import create_db_and_tables
from bot.handlers import (
    start_handler,
    catalog_handler,
    bouquet_detail_handler,
    catalog_navigation_handler,
    cart_handler,
    add_to_cart_handler,
    remove_from_cart_handler,
    checkout_handler,
    order_detail_handler
)
from bot.handlers.start import handle_my_orders, handle_support
from bot.handlers.admin import handle_new_orders, handle_manage_catalog, handle_statistics, handle_admin_settings
from bot.keyboards import get_main_menu_keyboard, get_admin_menu_keyboard
from bot.config import ADMIN_IDS


# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Основная функция запуска бота"""
    # Создание таблиц в базе данных
    create_db_and_tables()
    
    # Создание приложения
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчики команд
    application.add_handler(CommandHandler("start", start_handler))
    
    # Обработчики callback-запросов (нажатия на inline-кнопки)
    application.add_handler(CallbackQueryHandler(bouquet_detail_handler, pattern="^bouquet_"))
    application.add_handler(CallbackQueryHandler(catalog_navigation_handler, pattern="^catalog_page_"))
    application.add_handler(CallbackQueryHandler(add_to_cart_handler, pattern="^add_to_cart_"))
    application.add_handler(CallbackQueryHandler(remove_from_cart_handler, pattern="^remove_from_cart_"))
    application.add_handler(CallbackQueryHandler(checkout_handler, pattern="^checkout$"))
    application.add_handler(CallbackQueryHandler(cart_handler, pattern="^show_cart$"))
    application.add_handler(CallbackQueryHandler(catalog_handler, pattern="^show_catalog$"))
    
    # Обработчики сообщений (теперь правильно подключены как асинхронные)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))
    
    # Запуск бота
    logger.info("Запуск бота...")
    application.run_polling()


async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    user_id = update.effective_user.id
    
    # Определяем, является ли пользователь администратором
    is_admin = user_id in ADMIN_IDS
    
    # Обработка команд из меню
    if text == "🌸 Каталог":
        await catalog_handler(update, context)
    elif text == "🛒 Корзина":
        await cart_handler(update, context)
    elif text == "📦 Мои заказы":
        await handle_my_orders(update, context)
    elif text == "📞 Поддержка":
        await handle_support(update, context)
    elif is_admin and text == "📋 Новые заказы":
        await handle_new_orders(update, context)
    elif is_admin and text == "📝 Управление каталогом":
        await handle_manage_catalog(update, context)
    elif is_admin and text == "📊 Статистика":
        await handle_statistics(update, context)
    elif is_admin and text == "⚙️ Настройки":
        await handle_admin_settings(update, context)
    else:
        # Ответ по умолчанию
        if is_admin:
            await update.message.reply_text(
                "Выберите действие из меню администратора:",
                reply_markup=get_admin_menu_keyboard()
            )
        else:
            await update.message.reply_text(
                "Выберите действие из главного меню:",
                reply_markup=get_main_menu_keyboard()
            )


if __name__ == '__main__':
    main()