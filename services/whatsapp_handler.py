import logging
from services.message_queue import add_to_queue

logging.basicConfig(level=logging.INFO)

def process_message(data):
    """
    Process incoming WhatsApp webhook data.
    """
    try:
        sender = data.get("sender", {}).get("id")
        message_text = data.get("message", {}).get("text", "")
        group_id = data.get("group", {}).get("id")

        if not sender or not message_text or not group_id:
            logging.warning("Invalid message payload: %s", data)
            return

        add_to_queue(group_id, sender, message_text)
        logging.info(f"Message from {sender} added to queue for group {group_id}")

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        raise
