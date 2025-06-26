import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "data.db")

def get_db_connection():
    """
    Return a new SQLite connection (with row dictionary access).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Create tables for groups and group_languages if they do not exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            group_id TEXT PRIMARY KEY,
            awaiting_languages INTEGER DEFAULT 1
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id TEXT,
            language TEXT
        );
    """)

    conn.commit()
    conn.close()
