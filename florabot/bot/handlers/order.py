from telegram import Update
from telegram.ext import ContextTypes


async def my_orders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик просмотра моих заказов"""
    await update.message.reply_text("📦 Ваши заказы:\n\nПока что у вас нет оформленных заказов.")


async def order_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик просмотра деталей заказа"""
    # Получаем ID заказа из callback_data
    query = update.callback_query
    await query.answer()
    
    order_id = query.data.split("_")[2]  # order_detail_123
    await query.edit_message_text(f"📦 Детали заказа #{order_id}:\n\nИнформация о заказе #{order_id}")