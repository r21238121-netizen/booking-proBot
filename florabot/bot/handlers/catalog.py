from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import get_catalog_keyboard
from bot.models import Bouquet
from bot.database import get_session
from sqlmodel import select


async def catalog_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды просмотра каталога"""
    try:
        # В реальном приложении получаем букеты из базы данных
        # Пока что создадим тестовые данные
        test_bouquets = [
            Bouquet(id=1, name="Красные розы", description="Классические красные розы", price=3500, available=True),
            Bouquet(id=2, name="Белые тюльпаны", description="Элегантные белые тюльпаны", price=2500, available=True),
            Bouquet(id=3, name="Микс цветов", description="Смешанный букет из свежих цветов", price=4200, available=True),
            Bouquet(id=4, name="Желтые хризантемы", description="Яркие желтые хризантемы", price=2800, available=True),
            Bouquet(id=5, name="Свадебный букет", description="Элегантный свадебный букет", price=6500, available=True),
            Bouquet(id=6, name="Розы 101 шт.", description="101 красная роза", price=15000, available=True)
        ]
        
        keyboard = get_catalog_keyboard(test_bouquets)
        
        await update.message.reply_text(
            "💐 Выберите букет из каталога:",
            reply_markup=keyboard
        )
    except Exception as e:
        logging.error(f"Ошибка при обработке команды каталога: {e}")
        await update.message.reply_text("Произошла ошибка при загрузке каталога. Пожалуйста, попробуйте позже.")


async def bouquet_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик просмотра деталей букета"""
    query = update.callback_query
    await query.answer()
    
    # Получаем ID букета из callback_data
    bouquet_id = int(query.data.split("_")[1])
    
    # В реальном приложении получаем букет из базы данных
    # Пока что создадим тестовые данные
    test_bouquets = {
        1: Bouquet(id=1, name="Красные розы", description="Классические красные розы", price=3500, available=True),
        2: Bouquet(id=2, name="Белые тюльпаны", description="Элегантные белые тюльпаны", price=2500, available=True),
        3: Bouquet(id=3, name="Микс цветов", description="Смешанный букет из свежих цветов", price=4200, available=True),
        4: Bouquet(id=4, name="Желтые хризантемы", description="Яркие желтые хризантемы", price=2800, available=True),
        5: Bouquet(id=5, name="Свадебный букет", description="Элегантный свадебный букет", price=6500, available=True),
        6: Bouquet(id=6, name="Розы 101 шт.", description="101 красная роза", price=15000, available=True)
    }
    
    bouquet = test_bouquets.get(bouquet_id)
    if bouquet:
        # В реальном приложении здесь будет изображение
        detail_text = f"💐 *{bouquet.name}*\n\n"
        detail_text += f"{bouquet.description}\n\n"
        detail_text += f"Цена: *{bouquet.price}₽*"
        
        # Клавиатура с кнопками "Добавить в корзину" и "Назад"
        from telegram import InlineKeyboardMarkup, InlineKeyboardButton
        keyboard = [
            [InlineKeyboardButton("🛒 Добавить в корзину", callback_data=f"add_to_cart_{bouquet.id}")],
            [InlineKeyboardButton("◀️ Назад к каталогу", callback_data="show_catalog")]
        ]
        
        await query.edit_message_text(
            detail_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def catalog_navigation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик навигации по каталогу"""
    query = update.callback_query
    await query.answer()
    
    # Получаем номер страницы из callback_data
    page = int(query.data.split("_")[2])
    
    # В реальном приложении получаем букеты из базы данных
    # Пока что создадим тестовые данные
    test_bouquets = [
        Bouquet(id=1, name="Красные розы", description="Классические красные розы", price=3500, available=True),
        Bouquet(id=2, name="Белые тюльпаны", description="Элегантные белые тюльпаны", price=2500, available=True),
        Bouquet(id=3, name="Микс цветов", description="Смешанный букет из свежих цветов", price=4200, available=True),
        Bouquet(id=4, name="Желтые хризантемы", description="Яркие желтые хризантемы", price=2800, available=True),
        Bouquet(id=5, name="Свадебный букет", description="Элегантный свадебный букет", price=6500, available=True),
        Bouquet(id=6, name="Розы 101 шт.", description="101 красная роза", price=15000, available=True)
    ]
    
    keyboard = get_catalog_keyboard(test_bouquets, page=page)
    
    await query.edit_message_text(
        "💐 Выберите букет из каталога:",
        reply_markup=keyboard
    )