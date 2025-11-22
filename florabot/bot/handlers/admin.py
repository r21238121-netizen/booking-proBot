from telegram import Update
from telegram.ext import ContextTypes


async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команд администратора"""
    await update.message.reply_text("Вы вошли в режим администратора")


async def new_orders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик просмотра новых заказов (для администраторов)"""
    await update.message.reply_text("📋 Новые заказы:\n\nНовых заказов пока нет.")


async def manage_catalog_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик управления каталогом (для администраторов)"""
    await update.message.reply_text("📝 Управление каталогом:\n\nЗдесь вы можете добавить или изменить букеты.")