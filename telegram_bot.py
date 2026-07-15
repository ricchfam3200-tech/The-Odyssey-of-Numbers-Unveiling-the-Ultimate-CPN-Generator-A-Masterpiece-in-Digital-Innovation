import logging
import os

import requests

from telegram_conversation import handle_telegram_message

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/profile_number_generator.log", level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_telegram_message(chat_id, text):
    requests.post(f"{TELEGRAM_API_BASE}/sendMessage", json={"chat_id": chat_id, "text": text})


def main():
    offset = None
    print("Telegram bot polling started...")
    while True:
        params = {"timeout": 30}
        if offset is not None:
            params["offset"] = offset

        response = requests.get(f"{TELEGRAM_API_BASE}/getUpdates", params=params, timeout=35)
        response.raise_for_status()

        for update in response.json().get("result", []):
            offset = update["update_id"] + 1
            message = update.get("message")
            if message and "text" in message:
                handle_telegram_message(message["chat"]["id"], message["text"], send_telegram_message)


if __name__ == "__main__":
    main()
