# from telegram.ext import Updater, MessageHandler, Filters
# import dotenv

# TELEGRAM_BOT_TOKEN = dotenv.dotenv_values(".env")["TELEGRAM_BOT_TOKEN"]

# def handle_message(update, context):
#     print(update.message.text)
#     update.message.reply_text("Received your message!")

# updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
# dp = updater.dispatcher
# dp.add_handler(MessageHandler(Filters.text, handle_message))

# updater.start_polling()
# updater.idle()


import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.full_name
    text = update.message.text
    print(f"[{user}] {text}")
    await update.message.reply_text("קיבלתי", reply_to_message_id=update.message.message_id)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running and waiting for messages...")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "event loop is running" in str(e):
            print("Loop already running, applying nest_asyncio patch...")
            import nest_asyncio
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise
