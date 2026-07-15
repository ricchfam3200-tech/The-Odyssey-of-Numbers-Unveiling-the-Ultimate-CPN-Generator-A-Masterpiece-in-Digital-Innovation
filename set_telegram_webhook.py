import os
import sys

import requests


def main():
    if len(sys.argv) != 2:
        print("Usage: python set_telegram_webhook.py <public-base-url>")
        raise SystemExit(1)

    token = os.environ["TELEGRAM_BOT_TOKEN"]
    base_url = sys.argv[1].rstrip("/")
    webhook_url = f"{base_url}/telegram/webhook"

    response = requests.post(
        f"https://api.telegram.org/bot{token}/setWebhook",
        json={"url": webhook_url},
    )
    print(response.status_code, response.json())


if __name__ == "__main__":
    main()
