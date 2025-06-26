import logging
from apscheduler.schedulers.background import BackgroundScheduler
from services.message_queue import get_queue_size, get_from_queue
from services.user_manager import get_group_user_languages
from services.translation_llm import translate_with_llm
from services.message_sender import send_translated_message
from prompts.prompt_builder import build_translation_prompt

# Scheduler instance (singleton for the app)
scheduler = BackgroundScheduler()

# Time interval (in seconds) between stack flushes
FLUSH_INTERVAL_SECONDS = 2

def flush_message_stacks():
    """
    Periodically called job that flushes all active group message queues.
    """
    from services.message_queue import message_queues  # Import here to avoid circular dependencies

    logging.info("Running scheduled message stack flush...")

    for group_id, queue in list(message_queues.items()):
        while get_queue_size(group_id) > 0:
            message = get_from_queue(group_id)
            if not message:
                continue

            sender = message["sender"]
            text = message["message_text"]

            try:
                # Retrieve language preferences for all group members
                target_languages = get_group_user_languages(group_id, exclude_user_id=sender)
                if not target_languages:
                    logging.info(f"No target languages found for group {group_id}. Skipping message.")
                    continue

                # Build the LLM prompt
                prompt = build_translation_prompt(original_text=text, sender_id=sender, languages=target_languages)

                # Translate using LLM
                translated_message = translate_with_llm(prompt)

                # Send result back to group
                send_translated_message(group_id, translated_message)

                logging.info(f"Flushed message from {sender} in group {group_id}")

            except Exception as e:
                logging.exception(f"Error flushing message from group {group_id}: {e}")

def start_scheduler():
    """
    Start the background scheduler that periodically flushes message stacks.
    """
    scheduler.add_job(flush_message_stacks, 'interval', seconds=FLUSH_INTERVAL_SECONDS, id='flush_stacks')
    scheduler.start()
    logging.info("Scheduler started: flushing message stacks every %s seconds", FLUSH_INTERVAL_SECONDS)

