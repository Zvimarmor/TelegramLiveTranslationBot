# Telegram Multilingual Translation Bot

## Overview

This is a Telegram bot designed to translate all messages in a group into each user's preferred language. The bot runs entirely on a cloud server (e.g., AWS EC2) and manages everything automatically after deployment.

### Key Features

* Collects each user's language preference by free text (e.g., "English", "עברית").
* Stores preferences in a local SQLite database.
* Translates each message in the group into all preferred languages.
* Sends translations in a single, well-formatted message.
* Fully asynchronous using `python-telegram-bot`.

## How It Works (Behind the Scenes)

* **Language Validation**: Uses pre-defined dictionaries to map between user-friendly language names and translation API codes.
* **Translation**: Powered by Google Translate via `deep-translator`.
* **Persistence**: Language preferences are stored using SQLite.
* **Cloud Ready**: Optimized for deployment on cloud services like AWS EC2.

## Project Structure

```
project_root/
├── bot.py                    # Main bot logic
├── .env.example             # Template for environment variables
├── requirements.txt         # Python dependencies
├── database/
│   └── models.py            # Database setup
├── services/
│   ├── translator.py        # Translation logic
│   └── users_lang_manager.py # Language preference logic
└── README.md                # Project documentation
```

## How To Use The Bot (Telegram Usage)

1. **Add LiveTranslatorBot to your Telegram group.**

   * Open your group settings → Add Members → Search for `LiveTranslatorBot` → Add.

2. **Set your preferred language:**

   * Simply send a message with the name of your preferred language (e.g., `English`, `Français`, `עברית`).
   * The bot will confirm the language selection.

3. **See translations:**

   * Every time someone sends a message, the bot will automatically reply with translations for all group members in their selected languages.

4. **Bot Commands:**

   * `bot help` — Shows instructions on how to use the bot.
   * `reset languages` — (Admins only) Resets all language preferences in the group.

5. **Changing language preference:**

   * You can change your language at any time by sending a new language name.

### Example:

```
User A sends: "Hello everyone!"
LiveTranslatorBot replies:
- French (Français): Bonjour à tous !
- Hebrew (עברית): שלום לכולם!
- Spanish (Español): ¡Hola a todos!
```

## Notes

* The bot works fully automatically after being added to a group.
* Language preferences are specific to each group and user.
* Supports up to 10 members per group.

## Summary

LiveTranslatorBot provides a simple way to enable multilingual communication in Telegram groups. Once added, it seamlessly translates all messages to each user's preferred language without any additional interaction.
