# backend/main.py
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .utils import generate_slots_for_week
from datetime import datetime

app = FastAPI(title="Booking Pro API")

# Разрешаем запросы из Telegram WebApp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://t.me", "https://web.telegram.org"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

DB_FILE = "data.db"

def get_db():
    return sqlite3.connect(DB_FILE)

@app.get("/api/cities")
def get_cities():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT city FROM masters WHERE active = 1 ORDER BY city")
    cities = [row[0] for row in cur.fetchall()]
    conn.close()
    return cities

@app.get("/api/services")
def get_services():
    from shared.config import ALLOWED_SERVICES
    return ALLOWED_SERVICES

@app.get("/api/masters")
def get_masters(city: str, service: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.user_id, m.name, m.city, m.address, m.rating, m.review_count
        FROM masters m
        JOIN master_services ms ON m.user_id = ms.master_id
        JOIN services s ON ms.service_id = s.id
        WHERE m.city = ? AND s.name = ? AND m.active = 1
        ORDER BY m.rating DESC, m.completed_bookings DESC
    """, (city, service))
    masters = []
    for row in cur.fetchall():
        masters.append({
            "id": row[0],
            "name": row[1],
            "city": row[2],
            "address": row[3] or "Адрес уточнит мастер",
            "rating": row[4],
            "review_count": row[5]
        })
    conn.close()
    return masters

@app.get("/api/slots/{master_id}")
def get_slots(master_id: int):
    conn = get_db()
    cur = conn.cursor()
    # Получаем занятые слоты
    cur.execute("SELECT slot FROM bookings WHERE master_id = ? AND status = 'confirmed'", (master_id,))
    busy_slots = {row[0] for row in cur.fetchall()}
    conn.close()

    # Генерируем все возможные и убираем занятые
    all_slots = generate_slots_for_week()
    free_slots = [s for s in all_slots if s not in busy_slots]
    return free_slots[:30]  # максимум 30 слотов

@app.post("/api/book")
def book_slot(payload: dict):
    client_id = payload.get("client_id")
    master_id = payload.get("master_id")
    slot = payload.get("slot")

    if not all([client_id, master_id, slot]):
        raise HTTPException(400, "Недостаточно данных")

    try:
        slot_dt = datetime.fromisoformat(slot)
        if slot_dt <= datetime.now():
            raise HTTPException(400, "Время в прошлом")
    except ValueError:
        raise HTTPException(400, "Неверный формат времени")

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO bookings (client_id, master_id, slot)
            VALUES (?, ?, ?)
        """, (client_id, master_id, slot))
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.close()
        raise HTTPException(409, f"Конфликт записи: {e}")
    except Exception as e:
        conn.close()
        raise HTTPException(500, f"Ошибка записи: {e}")
    conn.close()
    return {"ok": True}

@app.get("/api/ad")
def get_ad():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT text, url FROM ads WHERE active = 1 LIMIT 1")
    ad = cur.fetchone()
    conn.close()
    if ad:
        return {"text": ad[0], "url": ad[1]}
    return {"text": "🔥 Попробуйте Pro-аккаунт — безлимит записей!", "url": "https://t.me/your_bot?start=pro"}

async def start_backend():
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()