# bot/keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def role_choice_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Найти мастера")],
            [KeyboardButton(text="👑 Стать мастером")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def city_request_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Отправить город")]
        ],
        resize_keyboard=True
    )

def service_choice_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💅 Маникюр", callback_data="service_Маникюр")],
            [InlineKeyboardButton(text="👁️ Наращивание ресниц", callback_data="service_Наращивание ресниц")],
            [InlineKeyboardButton(text="✨ Разное", callback_data="service_Разное")],
            [InlineKeyboardButton(text="✅ Готово", callback_data="service_done")]
        ]
    )

def moderation_kb(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Принять", callback_data=f"mod_approve_{user_id}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"mod_reject_{user_id}")
            ]
        ]
    )