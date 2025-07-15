# bot.py
"""
This bot connects to Telegram groups, collects users' preferred languages upon joining,
and automatically translates every message in the group to each member's preferred language.
Users can set their preferred language by sending the language name directly.
The bot supports a help command and broadcasts setup instructions when joining a group.
"""

import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, ChatMemberUpdated
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
    ChatMemberHandler,
)

import nest_asyncio
nest_asyncio.apply()

from database.models import init_db
from services.users_lang_manager import set_user_language, get_user_language, get_all_languages
from services.translator import translate_to_multiple_languages, validate_language, InvalidLanguageException

# Load Telegram bot token from environment
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Help message explaining the bot's functionality
HELP_MESSAGE = """
Bot Usage Guide:

- To set your preferred language, simply send the language name (e.g., English, Español, עברית).
- The bot will translate each message in the group to all preferred languages.
- You can change your language preference at any time by sending a new language name.
- Use the command 'bot help' to see this help message again.
"""

async def initialize_group_if_needed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Checks if the group has any language preferences stored.
    If no preferences exist, broadcasts a message prompting users to set their language.
    """
    group_id = str(update.effective_chat.id)
    target_languages = get_all_languages(group_id)

    if not target_languages:
        await context.bot.send_message(
            chat_id=group_id,
            text="Language setup initiated. Each user, please send your preferred language (e.g., English, Español, עברית).\nSend 'bot help' to view instructions."
        )

async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all incoming group messages.
    - Detects if the message is a help command and responds with instructions.
    - Detects if the message is a language name and updates the user's preference.
    - Otherwise, translates the message to all preferred group languages.
    """
    msg = update.message
    group_id = str(msg.chat.id)
    user_id = str(msg.from_user.id)
    user_name = msg.from_user.full_name
    text = msg.text.strip().lower()

    # Respond to help command
    if text == "bot help":
        await msg.reply_text(HELP_MESSAGE)
        return

    # Detect if message is a valid language name
    if text.startswith("change language:"):
        text = text.replace("change language:", "").strip()
        try:
            if not text:
                await msg.reply_text("Please provide a valid language name.")
                return
            lang_code = validate_language(text)
            set_user_language(group_id, user_id, user_name, lang_code)
            await msg.reply_text(f"Language preference updated to {text.capitalize()} ({lang_code})")
            return
        except InvalidLanguageException:
            await msg.reply_text(f"Invalid language '{text}'. Please send a valid language name.\nIf you need help, type 'bot help.")
            return

    # Check if there are target languages in the group
    target_languages = get_all_languages(group_id)
    if not target_languages:
        await msg.reply_text("No language preferences found in this group. Please send your preferred language.")
        await initialize_group_if_needed(update, context)
        return

    # Translate the message to all preferred languages
    translated_text = translate_to_multiple_languages(msg.text, target_languages)

    await msg.reply_text(f"🌍 Translations: 🌍\n{translated_text}", reply_to_message_id=msg.message_id)

async def greet_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles new members joining the group.
    Sends a welcome message prompting the new member to provide their language preference.
    Also re-initializes language setup if needed.
    """
    chat_member_update: ChatMemberUpdated = update.chat_member
    group_id = str(chat_member_update.chat.id)
    new_member = chat_member_update.new_chat_member.user
    user_name = new_member.full_name

    await context.bot.send_message(
        chat_id=group_id,
        text=f"Welcome {user_name}! Please send me your preferred language (e.g., English, Español, עברית)."
    )
    await initialize_group_if_needed(update, context)

async def main():
    """
    Main entry point of the bot:
    - Initializes database.
    - Sets up message and member handlers.
    - Starts polling updates from Telegram.
    """
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()

    # Handle text messages in groups
    group_filter = filters.TEXT & (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP)
    app.add_handler(MessageHandler(group_filter, handle_group_message))

    # Handle new members joining the group
    app.add_handler(ChatMemberHandler(greet_new_members, ChatMemberHandler.CHAT_MEMBER))

    print("Bot is running and listening for messages...")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
