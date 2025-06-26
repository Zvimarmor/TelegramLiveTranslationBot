import os
import logging
import requests

WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")  
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")

def send_translated_message(group_id: str, translated_text: str) -> bool:
    """
    Send a translated message to the given WhatsApp group.

    Args:
        group_id (str): The target group ID.
        translated_text (str): The full translated response to send.

    Returns:
        bool: True if sent successfully, False otherwise.
    """
    if os.getenv("LLM_PROVIDER") == "mock":
        # If mocking, just log instead of sending
        logging.info(f"[MOCK SEND] Group {group_id}: \n{translated_text}")
        return True

    payload = {
        "to": group_id,
        "type": "text",
        "text": {
            "body": translated_text
        }
    }

    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"Message sent to group {group_id}")
        return True
    except requests.RequestException as e:
        logging.error(f"Failed to send message to group {group_id}: {e}")
        return False
