from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard():
    """Основное меню для пользователей"""
    keyboard = [
        [KeyboardButton("🌸 Каталог"), KeyboardButton("🛒 Корзина")],
        [KeyboardButton("📦 Мои заказы"), KeyboardButton("📞 Поддержка")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_catalog_keyboard(bouquets, page=0, page_size=5):
    """Клавиатура для каталога букетов"""
    keyboard = []
    start_idx = page * page_size
    end_idx = start_idx + page_size
    current_bouquets = bouquets[start_idx:end_idx]
    
    for bouquet in current_bouquets:
        keyboard.append([InlineKeyboardButton(f"💐 {bouquet.name} - {bouquet.price}₽", 
                                             callback_data=f"bouquet_{bouquet.id}")])
    
    # Навигация по страницам
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"catalog_page_{page-1}"))
    if len(bouquets) > end_idx:
        navigation_buttons.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"catalog_page_{page+1}"))
    
    if navigation_buttons:
        keyboard.append(navigation_buttons)
    
    return InlineKeyboardMarkup(keyboard)


def get_cart_keyboard(cart_items):
    """Клавиатура для корзины"""
    keyboard = []
    for item in cart_items:
        keyboard.append([
            InlineKeyboardButton(f"❌ Удалить {item['bouquet'].name}", 
                                callback_data=f"remove_from_cart_{item['bouquet'].id}")
        ])
    
    keyboard.append([InlineKeyboardButton("✅ Оформить заказ", callback_data="checkout")])
    keyboard.append([InlineKeyboardButton("◀️ Назад в меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)