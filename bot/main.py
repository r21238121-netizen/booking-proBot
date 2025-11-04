# bot/main.py
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from shared.config import BOT_TOKEN, SUPER_ADMIN_ID, WEB_APP_URL
from .keyboards import role_choice_kb, city_request_kb, service_choice_kb, moderation_kb
from .states import MasterApplication
import os

# Глобальные объекты
bot = Bot(token=BOT_TOKEN)
router = Router()
dp = Dispatcher()

DB_FILE = "data.db"

def get_db():
    return sqlite3.connect(DB_FILE)

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT city FROM masters WHERE user_id = ? AND active = 1", (message.from_user.id,))
    master = cur.fetchone()
    conn.close()

    if master:
        # Уже мастер — показываем Mini App
        from aiogram.types import WebAppInfo
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        kb = InlineKeyboardBuilder()
        kb.button(text="📅 Мои записи и расписание", web_app=WebAppInfo(url=WEB_APP_URL + "?mode=master"))
        await message.answer("Вы — мастер! Управляйте расписанием:", reply_markup=kb.as_markup())
    else:
        await message.answer(
            "Добро пожаловать в Booking Pro!\n"
            "Вы хотите:",
            reply_markup=role_choice_kb()
        )

@router.message(F.text == "👑 Стать мастером")
async def become_master(message: Message, state: FSMContext):
    await message.answer("Напишите ваш город (например, Барнаул):", reply_markup=city_request_kb())
    await state.set_state(MasterApplication.waiting_for_city)

@router.message(MasterApplication.waiting_for_city)
async def process_city(message: Message, state: FSMContext):
    if not message.text or message.text == "📍 Отправить город":
        await message.answer("Пожалуйста, введите название города вручную:")
        return
    await state.update_data(city=message.text.strip())
    await message.answer("Выберите услуги:", reply_markup=service_choice_kb())
    await state.set_state(MasterApplication.waiting_for_services)

@router.callback_query(StateFilter(MasterApplication.waiting_for_services), F.data.startswith("service_"))
async def process_service(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    services = data.get("services", [])
    action = callback.data.replace("service_", "")

    if action == "done":
        if not services:
            await callback.answer("Выберите хотя бы одну услугу!", show_alert=True)
            return
        await state.update_data(services=services)
        await callback.message.edit_text("Отлично! Есть ли у вас Telegram-канал с работами? Вставьте ссылку или напишите «Нет»:")
        await state.set_state(MasterApplication.waiting_for_portfolio)
    else:
        if action not in services:
            services.append(action)
        else:
            services.remove(action)
        await state.update_data(services=services)
        await callback.answer(f"{'✅ Добавлено' if action in services else '❌ Удалено'}: {action}")

@router.message(MasterApplication.waiting_for_portfolio)
async def process_portfolio(message: Message, state: FSMContext):
    await state.update_data(portfolio=message.text.strip())
    await message.answer("Где вы о нас узнали? (например: «Из Telegram», «От друга» и т.д.)")
    await state.set_state(MasterApplication.waiting_for_source)

@router.message(MasterApplication.waiting_for_source)
async def process_source(message: Message, state: FSMContext):
    data = await state.get_data()
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO applications (user_id, city, portfolio_url, source)
            VALUES (?, ?, ?, ?)
        """, (message.from_user.id, data["city"], data["portfolio"], message.text.strip()))
        conn.commit()
        await message.answer("✅ Спасибо! Вашу заявку рассмотрят в течение 48 часов.")
    except sqlite3.IntegrityError:
        await message.answer("Вы уже отправляли заявку. Ожидайте модерации.")
    finally:
        conn.close()
    await state.clear()

# === Модерация (только для тебя) ===
@router.message(Command("moderate"))
async def check_applications(message: Message):
    if message.from_user.id != SUPER_ADMIN_ID:
        return
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, city, portfolio_url, source FROM applications WHERE status = 'pending'")
    apps = cur.fetchall()
    conn.close()

    if not apps:
        await message.answer("Нет заявок на модерацию.")
        return

    for app in apps:
        app_id, user_id, city, portfolio, source = app
        text = (
            f"🆕 Заявка #{app_id}\n"
            f"Город: {city}\n"
            f"Канал: {portfolio or '—'}\n"
            f"Источник: {source}\n"
            f"ID: {user_id}"
        )
        await message.answer(text, reply_markup=moderation_kb(user_id))

@router.callback_query(F.data.startswith("mod_approve_"))
async def approve_master(callback: CallbackQuery):
    if callback.from_user.id != SUPER_ADMIN_ID:
        return
    user_id = int(callback.data.split("_")[-1])
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT city, portfolio_url FROM applications WHERE user_id = ?", (user_id,))
    app = cur.fetchone()
    if app:
        city, portfolio = app
        user = await bot.get_chat(user_id)
        cur.execute("""
            INSERT OR IGNORE INTO masters (user_id, name, city, portfolio_url, active)
            VALUES (?, ?, ?, ?, 1)
        """, (user_id, user.full_name, city, portfolio))
        cur.execute("UPDATE applications SET status = 'approved' WHERE user_id = ?", (user_id,))
        conn.commit()
        await bot.send_message(user_id, "🎉 Поздравляем! Ваш профиль опубликован. Клиенты могут вас найти!")
    conn.close()
    await callback.message.edit_text("✅ Одобрено")

@router.callback_query(F.data.startswith("mod_reject_"))
async def reject_master(callback: CallbackQuery):
    if callback.from_user.id != SUPER_ADMIN_ID:
        return
    user_id = int(callback.data.split("_")[-1])
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE applications SET status = 'rejected' WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    await bot.send_message(user_id, "К сожалению, мы не можем опубликовать ваш профиль.")
    await callback.message.edit_text("❌ Отклонено")

async def start_bot():
    dp.include_router(router)
    await dp.start_polling(bot)