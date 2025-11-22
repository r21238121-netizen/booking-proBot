from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import get_cart_keyboard
from bot.models import Bouquet


async def cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды просмотра корзины"""
    # Получаем корзину из контекста (в реальном приложении - из базы данных)
    user_id = update.effective_user.id
    cart = context.user_data.get('cart', [])
    
    if not cart:
        await update.message.reply_text("🛒 Ваша корзина пуста. Добавьте что-нибудь из каталога!")
        return
    
    # Формируем сообщение с содержимым корзины
    cart_text = "🛒 *Ваша корзина*\n\n"
    total_price = 0
    
    for item in cart:
        bouquet = item['bouquet']
        quantity = item['quantity']
        item_total = bouquet.price * quantity
        total_price += item_total
        
        cart_text += f"💐 {bouquet.name}\n"
        cart_text += f"   Цена: {bouquet.price}₽ x {quantity} = {item_total}₽\n\n"
    
    cart_text += f"*Итого: {total_price}₽*"
    
    keyboard = get_cart_keyboard(cart)
    
    await update.message.reply_text(
        cart_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


async def add_to_cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик добавления в корзину"""
    query = update.callback_query
    await query.answer()
    
    # Получаем ID букета из callback_data
    bouquet_id = int(query.data.split("_")[3])
    
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
        # Получаем текущую корзину
        cart = context.user_data.get('cart', [])
        
        # Проверяем, есть ли уже этот букет в корзине
        existing_item = None
        for item in cart:
            if item['bouquet'].id == bouquet.id:
                existing_item = item
                break
        
        if existing_item:
            existing_item['quantity'] += 1
        else:
            cart.append({'bouquet': bouquet, 'quantity': 1})
        
        # Сохраняем корзину в контексте
        context.user_data['cart'] = cart
        
        await query.edit_message_text(
            f"✅ Букет *{bouquet.name}* добавлен в корзину!",
            parse_mode="Markdown"
        )


async def remove_from_cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик удаления из корзины"""
    query = update.callback_query
    await query.answer()
    
    # Получаем ID букета из callback_data
    bouquet_id = int(query.data.split("_")[3])
    
    # Получаем текущую корзину
    cart = context.user_data.get('cart', [])
    
    # Удаляем букет из корзины
    updated_cart = [item for item in cart if item['bouquet'].id != bouquet_id]
    context.user_data['cart'] = updated_cart
    
    if updated_cart:
        # Если корзина не пуста, показываем обновленную корзину
        cart_text = "🛒 *Ваша корзина*\n\n"
        total_price = 0
        
        for item in updated_cart:
            bouquet = item['bouquet']
            quantity = item['quantity']
            item_total = bouquet.price * quantity
            total_price += item_total
            
            cart_text += f"💐 {bouquet.name}\n"
            cart_text += f"   Цена: {bouquet.price}₽ x {quantity} = {item_total}₽\n\n"
        
        cart_text += f"*Итого: {total_price}₽*"
        
        keyboard = get_cart_keyboard(updated_cart)
        
        await query.edit_message_text(
            cart_text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    else:
        # Если корзина пуста, сообщаем об этом
        await query.edit_message_text(
            "🛒 Ваша корзина пуста. Добавьте что-нибудь из каталога!"
        )


async def checkout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик оформления заказа"""
    query = update.callback_query
    await query.answer()
    
    # Получаем корзину
    cart = context.user_data.get('cart', [])
    
    if not cart:
        await query.edit_message_text("🛒 Ваша корзина пуста. Добавьте что-нибудь из каталога!")
        return
    
    # Рассчитываем общую стоимость
    total_price = sum(item['bouquet'].price * item['quantity'] for item in cart)
    
    # В реальном приложении здесь нужно запросить адрес, дату и время доставки
    # Пока что просто сообщим пользователю, что заказ готов к оформлению
    checkout_text = (
        f"📦 *Оформление заказа*\n\n"
        f"Всего товаров: {len(cart)}\n"
        f"Итого к оплате: *{total_price}₽*\n\n"
        "Пожалуйста, укажите адрес доставки, дату и время, а также комментарий к заказу."
    )
    
    # Клавиатура для возврата в корзину или подтверждения заказа
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = [
        [InlineKeyboardButton("✅ Подтвердить заказ", callback_data="confirm_order")],
        [InlineKeyboardButton("🛒 Назад в корзину", callback_data="show_cart")]
    ]
    
    await query.edit_message_text(
        checkout_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )