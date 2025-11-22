from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from database.models import create_user_if_not_exists
from database.database import get_db_connection
from keyboards.main_menu import get_main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle the /start command"""
    # Get database connection
    pool = await get_db_connection()
    
    # Create or update user in database
    await create_user_if_not_exists(
        pool=pool,
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    # Clear any existing state
    await state.clear()
    
    # Send welcome message with main menu
    welcome_text = f"""
🎉 <b>Добро пожаловать в TonLucky!</b>

🎰 Ставь. Играй. Выигрывай в TON.

<b>Ваш стартовый баланс:</b> 1000 фишек

Игры доступные прямо сейчас:
• 🎲 TonDice - Кости
• 🎰 TonRoulette - Рулетка  
• 🪙 TonCoinFlip - Монетка
• 🎰 TonSlots - Слоты
• 👑 TonBlackjack - Блэкджек
• 📈 TonCrash - Крах
• 💣 TonMines - Сапёр
• 📏 TonHiLo - Больше/Меньше
• 🧮 TonKeno - Кено
• 🃏 TonBaccarat - Баккара
• 🎯 TonPlinko - Плинко
• 🎡 TonWheel - Колесо фортуны
• 🎫 TonLottery - Лотерея
• 🎳 TonBingo - Бинго
• 🤞 TonScratch - Скретч-карты
• ↔️ TonOver/Under - Больше/Меньше
• 7️⃣ TonLucky7 - Семёрка
• 🃏 TonPoker - Покер

Начните играть прямо сейчас!
    """
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )


def setup_start_handlers(dp):
    """Setup start command handlers"""
    dp.include_router(router)