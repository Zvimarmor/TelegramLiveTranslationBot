# app.py

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from services.whatsapp_handler import process_message

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)

# Webhook secret from environment variables
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-webhook-secret")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    """
    Handle incoming WhatsApp webhook events.
    """
    # Verify webhook secret
    incoming_secret = request.headers.get("X-Twilio-Signature", "")
    if incoming_secret != WEBHOOK_SECRET:
        return jsonify({"error": "Invalid webhook secret"}), 403

    # Parse incoming JSON payload
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request payload"}), 400

    # Process the incoming message
    try:
        process_message(data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))