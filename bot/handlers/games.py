from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from decimal import Decimal

from keyboards.main_menu import get_main_menu_keyboard
from games.dice import DiceGame

router = Router()


# FSM States for games
class GameStates(StatesGroup):
    waiting_for_dice_bet = State()
    waiting_for_dice_number = State()


@router.callback_query(lambda c: c.data == 'game_dice')
async def game_dice_start(callback_query: CallbackQuery, state: FSMContext):
    """Start the TonDice game"""
    await callback_query.answer()
    await callback_query.message.edit_text(
        "🎲 <b>TonDice</b>\n\n"
        "Введите сумму ставки (мин. 10 фишек, макс. 1000 фишек):",
    )
    await state.set_state(GameStates.waiting_for_dice_bet)


@router.message(GameStates.waiting_for_dice_bet)
async def process_dice_bet(message: Message, state: FSMContext):
    """Process the dice bet amount"""
    try:
        bet_amount = Decimal(message.text.replace(',', '.'))
        
        # Store bet amount in state
        await state.update_data(bet_amount=bet_amount)
        
        # Ask for dice number
        await message.answer(
            "Теперь выберите число от 1 до 6:",
        )
        await state.set_state(GameStates.waiting_for_dice_number)
    except:
        await message.answer("Пожалуйста, введите корректную сумму ставки (число).")
        return


@router.message(GameStates.waiting_for_dice_number)
async def process_dice_number(message: Message, state: FSMContext):
    """Process the dice number choice and play the game"""
    try:
        chosen_number = int(message.text)
        if not 1 <= chosen_number <= 6:
            await message.answer("Пожалуйста, введите число от 1 до 6.")
            return
        
        # Get stored bet amount
        data = await state.get_data()
        bet_amount = data['bet_amount']
        
        # Play the dice game
        dice_game = DiceGame()
        result = await dice_game.place_bet(
            user_id=message.from_user.id,
            bet_amount=bet_amount,
            chosen_number=chosen_number
        )
        
        if result['success']:
            await message.answer(result['message'])
        else:
            await message.answer(result['message'])
        
        # Clear state and return to main menu
        await state.clear()
        await message.answer("Используйте главное меню для продолжения игры.", reply_markup=get_main_menu_keyboard())
        
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число от 1 до 6.")
        return
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
        await state.clear()
        await message.answer("Используйте главное меню для продолжения игры.", reply_markup=get_main_menu_keyboard())


@router.callback_query(lambda c: c.data == 'game_roulette')
async def game_roulette(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonRoulette game"""
    await callback_query.answer("TonRoulette - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🎡 <b>TonRoulette</b>\n\n"
        "Европейская рулетка (0-36)\n"
        "Ставки на цвет, чёт/нечет, число и другие комбинации.",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_coinflip')
async def game_coinflip(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonCoinFlip game"""
    await callback_query.answer("TonCoinFlip - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🪙 <b>TonCoinFlip</b>\n\n"
        "Орёл или решка?\n"
        "Угадайте результат с множителем x1.95!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_slots')
async def game_slots(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonSlots game"""
    await callback_query.answer("TonSlots - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🎰 <b>TonSlots</b>\n\n"
        "3 барабана, 5 тем (космос, Египет, киберпанк, джунгли, неон)\n"
        "Выигрывайте комбинации и крупные множители!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_blackjack')
async def game_blackjack(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonBlackjack game"""
    await callback_query.answer("TonBlackjack - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "👑 <b>TonBlackjack</b>\n\n"
        "Играйте против ИИ-дилера\n"
        "Используйте страховку и удвоение ставки!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_crash')
async def game_crash(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonCrash game"""
    await callback_query.answer("TonCrash - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "📈 <b>TonCrash</b>\n\n"
        "График растёт - нажмите 'забрать' до обвала!\n"
        "Умножайте свою ставку до краха!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_mines')
async def game_mines(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonMines game"""
    await callback_query.answer("TonMines - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "💣 <b>TonMines</b>\n\n"
        "Поле 5×5, мин от 1 до 24\n"
        "Открывайте безопасные клетки и увеличивайте множитель!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_hilo')
async def game_hilo(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonHiLo game"""
    await callback_query.answer("TonHiLo - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "📏 <b>TonHiLo</b>\n\n"
        "Карта открыта - угадайте, следующая выше или ниже\n"
        "Увеличивайте множитель при правильных ответах!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_keno')
async def game_keno(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonKeno game"""
    await callback_query.answer("TonKeno - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🧮 <b>TonKeno</b>\n\n"
        "Выберите до 10 чисел из 80\n"
        "Рандомный розыгрыш с крупными выигрышами!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_baccarat')
async def game_baccarat(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonBaccarat game"""
    await callback_query.answer("TonBaccarat - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🃏 <b>TonBaccarat</b>\n\n"
        "Ставка на Player, Banker или Tie\n"
        "Автоматическая раздача карт!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_plinko')
async def game_plinko(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonPlinko game"""
    await callback_query.answer("TonPlinko - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🎯 <b>TonPlinko</b>\n\n"
        "Шарик падает по доске\n"
        "Попадает в ячейку с множителем от x0.5 до x100!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_wheel')
async def game_wheel(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonWheel game"""
    await callback_query.answer("TonWheel - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🎡 <b>TonWheel</b>\n\n"
        "Колесо фортуны с фишками, NFT, бустерами и x2\n"
        "Испытайте удачу!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_lottery')
async def game_lottery(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonLottery game"""
    await callback_query.answer("TonLottery - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🎫 <b>TonLottery</b>\n\n"
        "Ежедневный розыгрыш\n"
        "Билет всего за 0.1 TON!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_bingo')
async def game_bingo(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonBingo game"""
    await callback_query.answer("TonBingo - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🎳 <b>TonBingo</b>\n\n"
        "Карточка 5×5, совпадения по линиям\n"
        "Чат-турниры и крупные призы!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_scratch')
async def game_scratch(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonScratch game"""
    await callback_query.answer("TonScratch - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🤞 <b>TonScratch</b>\n\n"
        "Виртуальная скретч-карта\n"
        "Мгновенный результат - выигрыш или проигрыш!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_overunder')
async def game_overunder(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonOver/Under game"""
    await callback_query.answer("TonOver/Under - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "↔️ <b>TonOver/Under</b>\n\n"
        "Число от 1 до 100\n"
        "Ставка на >50 или <50!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_lucky7')
async def game_lucky7(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonLucky7 game"""
    await callback_query.answer("TonLucky7 - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "7️⃣ <b>TonLucky7</b>\n\n"
        "Ставка на выпадение семёрки\n"
        "В различных комбинациях!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == 'game_poker')
async def game_poker(callback_query: CallbackQuery, state: FSMContext):
    """Handle TonPoker game"""
    await callback_query.answer("TonPoker - Игра в разработке", show_alert=True)
    await callback_query.message.edit_text(
        "🃏 <b>TonPoker</b>\n\n"
        "Texas Hold'em против ботов\n"
        "Еженедельные турниры!",
        reply_markup=get_main_menu_keyboard()
    )


def setup_game_handlers(dp):
    """Setup game handlers"""
    dp.include_router(router)