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
    my_orders_handler,
    order_detail_handler,
    admin_handler,
    new_orders_handler,
    manage_catalog_handler
)
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
    
    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))
    
    # Обработчики callback-запросов (нажатия на inline-кнопки)
    application.add_handler(CallbackQueryHandler(bouquet_detail_handler, pattern="^bouquet_"))
    application.add_handler(CallbackQueryHandler(catalog_navigation_handler, pattern="^catalog_page_"))
    application.add_handler(CallbackQueryHandler(add_to_cart_handler, pattern="^add_to_cart_"))
    application.add_handler(CallbackQueryHandler(remove_from_cart_handler, pattern="^remove_from_cart_"))
    application.add_handler(CallbackQueryHandler(checkout_handler, pattern="^checkout$"))
    application.add_handler(CallbackQueryHandler(cart_handler, pattern="^show_cart$"))
    application.add_handler(CallbackQueryHandler(catalog_handler, pattern="^show_catalog$"))
    
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


async def handle_my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик просмотра моих заказов"""
    await update.message.reply_text("📦 Ваши заказы:\n\nПока что у вас нет оформленных заказов.")


async def handle_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик поддержки"""
    await update.message.reply_text("📞 Служба поддержки:\n\nНапишите нам @florabot_support")


async def handle_new_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик просмотра новых заказов (для администраторов)"""
    await update.message.reply_text("📋 Новые заказы:\n\nНовых заказов пока нет.")


async def handle_manage_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик управления каталогом (для администраторов)"""
    await update.message.reply_text("📝 Управление каталогом:\n\nЗдесь вы можете добавить или изменить букеты.")


async def handle_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик статистики (для администраторов)"""
    await update.message.reply_text("📊 Статистика:\n\nЗдесь отображается статистика продаж.")


async def handle_admin_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик настроек администратора"""
    await update.message.reply_text("⚙️ Настройки администратора:\n\nЗдесь вы можете настроить параметры бота.")


if __name__ == '__main__':
    main()