import sqlite3
from config import Config

DATABASE_NAME = Config.DATABASE_URL.replace("sqlite:///", "", 1)


def get_db():
    """SQLite veritabanına bağlantı oluşturur."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(app):
    """Leads tablosunu yoksa oluşturur."""
    connection = get_db()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def lead_ekle(isim, telefon, mesaj):
    """Yeni bir lead kaydeder."""
    connection = get_db()

    try:
        cursor = connection.execute(
            """
            INSERT INTO leads (isim, telefon, mesaj)
            VALUES (?, ?, ?)
            """,
            (isim, telefon, mesaj),
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def tum_leadler():
    """Lead kayıtlarını en yeniden eskiye getirir."""
    connection = get_db()

    try:
        cursor = connection.execute(
            """
            SELECT id, isim, telefon, mesaj, tarih
            FROM leads
            ORDER BY tarih DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()