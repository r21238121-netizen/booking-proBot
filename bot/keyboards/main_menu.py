from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Get the main menu keyboard with all available games"""
    keyboard = [
        [
            InlineKeyboardButton(text="🎲 TonDice", callback_data="game_dice"),
            InlineKeyboardButton(text="🎡 TonRoulette", callback_data="game_roulette")
        ],
        [
            InlineKeyboardButton(text="🪙 TonCoinFlip", callback_data="game_coinflip"),
            InlineKeyboardButton(text="🎰 TonSlots", callback_data="game_slots")
        ],
        [
            InlineKeyboardButton(text="👑 TonBlackjack", callback_data="game_blackjack"),
            InlineKeyboardButton(text="📈 TonCrash", callback_data="game_crash")
        ],
        [
            InlineKeyboardButton(text="💣 TonMines", callback_data="game_mines"),
            InlineKeyboardButton(text="📏 TonHiLo", callback_data="game_hilo")
        ],
        [
            InlineKeyboardButton(text="🧮 TonKeno", callback_data="game_keno"),
            InlineKeyboardButton(text="🃏 TonBaccarat", callback_data="game_baccarat")
        ],
        [
            InlineKeyboardButton(text="🎯 TonPlinko", callback_data="game_plinko"),
            InlineKeyboardButton(text="🎡 TonWheel", callback_data="game_wheel")
        ],
        [
            InlineKeyboardButton(text="🎫 TonLottery", callback_data="game_lottery"),
            InlineKeyboardButton(text="🎳 TonBingo", callback_data="game_bingo")
        ],
        [
            InlineKeyboardButton(text="🤞 TonScratch", callback_data="game_scratch"),
            InlineKeyboardButton(text="↔️ TonOver/Under", callback_data="game_overunder")
        ],
        [
            InlineKeyboardButton(text="7️⃣ TonLucky7", callback_data="game_lucky7"),
            InlineKeyboardButton(text="🃏 TonPoker", callback_data="game_poker")
        ],
        [
            InlineKeyboardButton(text="💳 Баланс", callback_data="balance"),
            InlineKeyboardButton(text="💰 Пополнить", callback_data="deposit")
        ],
        [
            InlineKeyboardButton(text="📤 Вывести", callback_data="withdraw"),
            InlineKeyboardButton(text="🎁 Бонус", callback_data="bonus")
        ],
        [
            InlineKeyboardButton(text="👥 Рефералы", callback_data="referral"),
            InlineKeyboardButton(text="🏆 Рейтинг", callback_data="rating")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)