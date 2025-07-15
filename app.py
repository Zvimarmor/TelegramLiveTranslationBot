from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import logging

from services.whatsapp_handler import process_message
from database.models import init_db
from scheduler.flush_scheduler import start_scheduler

# Load environment variables from .env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Flask app instance
app = Flask(__name__)

# Webhook secret (used for verifying incoming requests)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-webhook-secret")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    """
    Handle incoming WhatsApp webhook events.
    """
    # Optional: verify webhook signature
    incoming_secret = request.headers.get("X-Twilio-Signature", "")
    if incoming_secret != WEBHOOK_SECRET:
        return jsonify({"error": "Invalid webhook secret"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request payload"}), 400

    try:
        process_message(data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.exception("Error while processing incoming message")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Initialize the DB and start the scheduler
    init_db()
    start_scheduler()

    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
