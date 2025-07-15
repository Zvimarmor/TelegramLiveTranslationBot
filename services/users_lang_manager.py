# services/language_manager.py
"""
This service module manages user language preferences within Telegram groups.
It provides functions to set, retrieve, and reset language preferences.
"""

import logging
from database.models import get_db_connection

def set_user_language(group_id: str, user_id: str, user_name: str, language: str):
    """
    Sets or updates the preferred language for a user in a specific group.
    Args:
        group_id (str): Telegram group identifier.
        user_id (str): Telegram user identifier.
        user_name (str): User's display name.
        language (str): Language code (e.g., 'en', 'he').
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO group_users (group_id, user_id, user_name, language)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(group_id, user_id) DO UPDATE SET language=excluded.language
    """, (group_id, user_id, user_name, language))
    conn.commit()
    conn.close()
    logging.info(f"Updated language for {user_name} in group {group_id}: {language}")

def get_user_language(group_id: str, user_id: str) -> str | None:
    """
    Retrieves the preferred language of a user within a group.
    Args:
        group_id (str): Telegram group identifier.
        user_id (str): Telegram user identifier.
    Returns:
        str | None: The language code if found, otherwise None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT language FROM group_users WHERE group_id = ? AND user_id = ?
    """, (group_id, user_id))
    row = cursor.fetchone()
    conn.close()
    return row["language"] if row else None

def get_all_languages(group_id: str) -> list[str]:
    """
    Retrieves a list of unique languages preferred by users in a group.
    Args:
        group_id (str): Telegram group identifier.
    Returns:
        list[str]: List of unique language codes.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT language FROM group_users WHERE group_id = ?
    """, (group_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row["language"] for row in rows]

def reset_group_languages(group_id: str):
    """
    Resets the language preferences for all users in a group.
    Args:
        group_id (str): Telegram group identifier.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM group_users WHERE group_id = ?
    """, (group_id,))
    conn.commit()
    conn.close()
    logging.info(f"Reset languages for group {group_id}")
