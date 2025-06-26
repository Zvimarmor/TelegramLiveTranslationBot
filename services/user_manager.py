import sqlite3
import logging
from database.models import init_db, get_db_connection

# Language collection reset keyword
RESET_KEYWORD = "reset-language"  # Can be changed to any string or regex

def initialize_group(group_id: str):
    """
    Initialize a group in the database (if not already present).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO groups (group_id, awaiting_languages)
        VALUES (?, 1)
    """, (group_id,))

    conn.commit()
    conn.close()
    logging.info(f"Initialized group {group_id}")

def is_group_waiting_for_languages(group_id: str) -> bool:
    """
    Check whether the group is currently in the language collection phase.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT awaiting_languages FROM groups WHERE group_id = ?
    """, (group_id,))
    row = cursor.fetchone()

    conn.close()
    return row and row["awaiting_languages"] == 1

def submit_group_language(group_id: str, language: str):
    """
    Add a language to the group preference list.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO group_languages (group_id, language)
        VALUES (?, ?)
    """, (group_id, language))

    conn.commit()
    conn.close()
    logging.info(f"Added language '{language}' for group {group_id}")

def get_group_user_languages(group_id: str, exclude_user_id=None) -> list[str]:
    """
    Return the list of unique preferred languages for a group.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT language FROM group_languages
        WHERE group_id = ?
    """, (group_id,))
    rows = cursor.fetchall()

    conn.close()
    return [row["language"] for row in rows]

def reset_group_languages(group_id: str):
    """
    Clear all stored language preferences for the group and set it back to collection mode.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM group_languages WHERE group_id = ?", (group_id,))
    cursor.execute("UPDATE groups SET awaiting_languages = 1 WHERE group_id = ?", (group_id,))

    conn.commit()
    conn.close()
    logging.info(f"Group {group_id} language preferences reset")

def mark_group_ready(group_id: str):
    """
    Mark that the group has finished the language collection process.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE groups SET awaiting_languages = 0 WHERE group_id = ?
    """, (group_id,))

    conn.commit()
    conn.close()
    logging.info(f"Group {group_id} marked as ready")
