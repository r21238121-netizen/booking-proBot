# shared/database.py
import sqlite3
import os
from .config import DB_FILE, ALLOWED_SERVICES

def init_db():
    """Создаёт базу данных, если её нет"""
    if os.path.exists(DB_FILE):
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Таблица: категории услуг
    cur.execute("""
        CREATE TABLE services (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Таблица: мастера
    cur.execute("""
        CREATE TABLE masters (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            address TEXT,
            portfolio_url TEXT,
            rating REAL DEFAULT 0.0,
            review_count INTEGER DEFAULT 0,
            completed_bookings INTEGER DEFAULT 0,
            pro BOOLEAN DEFAULT 0,
            active BOOLEAN DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Таблица: услуги мастеров (многие-ко-многим)
    cur.execute("""
        CREATE TABLE master_services (
            master_id INTEGER,
            service_id INTEGER,
            FOREIGN KEY(master_id) REFERENCES masters(user_id),
            FOREIGN KEY(service_id) REFERENCES services(id),
            UNIQUE(master_id, service_id)
        )
    """)

    # Таблица: заявки на модерацию
    cur.execute("""
        CREATE TABLE applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            city TEXT NOT NULL,
            portfolio_url TEXT,
            source TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Таблица: записи клиентов
    cur.execute("""
        CREATE TABLE bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            master_id INTEGER NOT NULL,
            slot TEXT NOT NULL,
            status TEXT DEFAULT 'confirmed',
            reminder_sent BOOLEAN DEFAULT 0,
            review_asked BOOLEAN DEFAULT 0,
            reviewed BOOLEAN DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(master_id) REFERENCES masters(user_id)
        )
    """)

    # Таблица: реклама
    cur.execute("""
        CREATE TABLE ads (
            id INTEGER PRIMARY KEY,
            text TEXT NOT NULL,
            url TEXT NOT NULL,
            impressions INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            active BOOLEAN DEFAULT 1
        )
    """)

    # Таблица: подписки (Pro)
    cur.execute("""
        CREATE TABLE subscriptions (
            master_id INTEGER PRIMARY KEY,
            active_until TEXT NOT NULL,
            pro BOOLEAN DEFAULT 1,
            FOREIGN KEY(master_id) REFERENCES masters(user_id)
        )
    """)

    # Добавляем базовые категории
    cur.executemany("INSERT INTO services (name) VALUES (?)", [(s,) for s in ALLOWED_SERVICES])

    conn.commit()
    conn.close()