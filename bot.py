import os
import requests
from flask import Flask, request, abort

app = Flask(__name__)

TOKEN = os.environ["BOT_TOKEN"]
SECRET = os.environ["WEBHOOK_SECRET"]

LATITUDE = 40.154582
LONGITUDE = 67.832457

API = f"https://api.telegram.org/bot{TOKEN}/"

@app.route("/", methods=["GET"])
def home():
    return "Bot ishlayapti!"

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != SECRET:
        abort(403)

    data = request.get_json(silent=True) or {}
    msg = data.get("business_message", {})

    if msg.get("text", "").strip() == "001":
        requests.post(
            API + "sendLocation",
            json={
                "business_connection_id": msg["business_connection_id"],
                "chat_id": msg["chat"]["id"],
                "latitude": LATITUDE,
                "longitude": LONGITUDE
            },
            timeout=15
        )

        requests.post(
            API + "sendMessage",
            json={
                "business_connection_id": msg["business_connection_id"],
                "chat_id": msg["chat"]["id"],
                "text": (
                    "📍 <b>Manzil:</b> Аккурганлик 84-уй\n"
                    "📞 <b>Telefon:</b> +998 99 351 29 29\n"
                    "📞 <b>Telefon:</b> +998 88 644 10 75\n"
                    "🕒 <b>Ish vaqti:</b> 24/7"
                ),
                "parse_mode": "HTML"
            },
            timeout=15
        )

    return "OK"
if __name__ == "__main__":
    url = os.environ["RENDER_EXTERNAL_URL"]
    requests.post(
        API + "setWebhook",
        json={
            "url": url + "/webhook",
            "secret_token": SECRET,
            "allowed_updates": ["business_message"]
        },
        timeout=15
    )
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
