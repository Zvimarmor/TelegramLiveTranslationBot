# database/models.py
"""
This module handles all database operations related to user language preferences within Telegram groups.
It uses SQLite to store each user's preferred language by group.
"""

import sqlite3
import os

# Path to the SQLite database file
DB_PATH = os.getenv("DATABASE_PATH", "translation_bot.db")

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    Returns:
        sqlite3.Connection: SQLite connection object.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes the database by creating the necessary tables if they don't exist.
    Tables:
        - group_users: Stores group_id, user_id, user_name, and preferred language.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_users (
            group_id TEXT,
            user_id TEXT,
            user_name TEXT,
            language TEXT,
            PRIMARY KEY (group_id, user_id)
        );
    """)

    conn.commit()
    conn.close()