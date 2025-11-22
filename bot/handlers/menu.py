from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models import get_user_balance
from database.database import get_db_connection
from keyboards.main_menu import get_main_menu_keyboard

router = Router()


@router.callback_query(lambda c: c.data == 'balance')
async def show_balance(callback_query: CallbackQuery, state: FSMContext):
    """Show user's balance"""
    pool = await get_db_connection()
    balance = await get_user_balance(pool, callback_query.from_user.id)
    
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"💳 <b>Ваш баланс:</b> {balance} фишек\n\n"
        f"Используйте главное меню для продолжения игры.",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'deposit')
async def show_deposit_info(callback_query: CallbackQuery, state: FSMContext):
    """Show deposit information"""
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"💰 <b>Пополнение баланса</b>\n\n"
        f"Для пополнения баланса переведите TON на наш адрес:\n"
        f"<code>EQ...</code>\n\n"
        f"После перевода нажмите кнопку \"Проверить платеж\".\n\n"
        f"Курс: 1 TON = 1000 фишек",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'withdraw')
async def show_withdraw_info(callback_query: CallbackQuery, state: FSMContext):
    """Show withdrawal information"""
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"📤 <b>Вывод средств</b>\n\n"
        f"Максимальный вывод: 5 TON в день\n"
        f"Комиссия: 3% от суммы вывода\n\n"
        f"Введите адрес вашего TON кошелька и сумму для вывода.",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'bonus')
async def show_bonus_info(callback_query: CallbackQuery, state: FSMContext):
    """Show bonus information"""
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"🎁 <b>Ежедневный бонус</b>\n\n"
        f"Зайдите завтра для получения ежедневного бонуса!\n\n"
        f"Также вы можете получить бонус за:\n"
        f"• Приглашение друзей\n"
        f"• Выигрыш в играх\n"
        f"• Участие в турнирах",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'referral')
async def show_referral_info(callback_query: CallbackQuery, state: FSMContext):
    """Show referral information"""
    referral_link = f"https://t.me/tonlucky_bot?start={callback_query.from_user.id}"
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"👥 <b>Реферальная программа</b>\n\n"
        f"Приглашайте друзей и получайте 10% от их первых пополнений!\n\n"
        f"Ваша реферальная ссылка:\n"
        f"<code>{referral_link}</code>\n\n"
        f"Поделитесь этой ссылкой с друзьями и зарабатывайте вместе!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'rating')
async def show_rating(callback_query: CallbackQuery, state: FSMContext):
    """Show rating information"""
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"🏆 <b>Рейтинг игроков</b>\n\n"
        f"Здесь будет отображаться рейтинг самых успешных игроков.\n\n"
        f"Играйте больше, чтобы подняться в рейтинге!",
        reply_markup=get_main_menu_keyboard()
    )


def setup_menu_handlers(dp):
    """Setup menu handlers"""
    dp.include_router(router)