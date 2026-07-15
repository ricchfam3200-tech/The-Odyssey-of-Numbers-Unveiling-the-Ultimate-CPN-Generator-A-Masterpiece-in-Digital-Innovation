import logging
import os

import requests
from flask import Flask, jsonify, render_template_string, request

from datetime import date

from access_codes import AccessCodeManager
from constants import ACCESS_CODE_LIMIT, ACCESS_CODES, MIN_AGE, US_STATES
from luhn_algorithm import calculate_luhn_check_digit
from main import ProfileNumberGenerator, is_of_age
from utils import is_valid_number

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/profile_number_generator.log", level=logging.INFO)

app = Flask(__name__)
profile_number_generator = ProfileNumberGenerator()
access_code_manager = AccessCodeManager(
    ACCESS_CODES, ACCESS_CODE_LIMIT, os.path.join("logs", "access_code_usage.json")
)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
STATES_LOWER = {state.lower(): state for state in US_STATES}

# Per-chat conversation state, keyed by Telegram chat id. Kept in memory, which is fine as long
# as this web service runs a single process (the Render free-tier default).
telegram_sessions = {}


def send_telegram_message(chat_id, text):
    requests.post(f"{TELEGRAM_API_BASE}/sendMessage", json={"chat_id": chat_id, "text": text})

INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Profile Number Generator</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 640px; margin: 4rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { font-size: 1.5rem; }
    label { display: block; font-weight: 600; margin-bottom: 0.4rem; }
    input[type="text"], input[type="date"], select { display: block; width: 100%; font-size: 1rem; padding: 0.5rem 0.6rem; margin-bottom: 1rem; border: 1px solid #999; border-radius: 4px; box-sizing: border-box; }
    button { font-size: 1rem; padding: 0.6rem 1.2rem; cursor: pointer; }
    #result { margin-top: 1.5rem; padding: 1rem; background: #f4f4f4; border-radius: 6px; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h1>Profile Number Generator</h1>
  <p>Generates a random 9-digit number that passes the Luhn check.</p>
  <label for="code">Access Code</label>
  <input type="text" id="code" placeholder="Enter your access code">
  <label for="name">Name</label>
  <input type="text" id="name" placeholder="Enter a name">
  <label for="state">State</label>
  <select id="state">
    <option value="">Select a state</option>
    {% for state in states %}
    <option value="{{ state }}">{{ state }}</option>
    {% endfor %}
  </select>
  <label for="dob">Date of Birth</label>
  <input type="date" id="dob">
  <button id="generate">Generate Profile Number</button>
  <div id="result"></div>
  <script>
    document.getElementById('generate').addEventListener('click', async () => {
      const button = document.getElementById('generate');
      const result = document.getElementById('result');
      const code = document.getElementById('code').value;
      const name = document.getElementById('name').value;
      const state = document.getElementById('state').value;
      const dob = document.getElementById('dob').value;
      button.disabled = true;
      result.textContent = 'Generating...';
      try {
        const params = new URLSearchParams({ code: code, name: name, state: state, dob: dob });
        const res = await fetch('/api/generate?' + params.toString());
        const data = await res.json();
        result.textContent = JSON.stringify(data, null, 2);
      } catch (err) {
        result.textContent = 'Error generating profile number.';
      } finally {
        button.disabled = false;
      }
    });
  </script>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(INDEX_HTML, states=US_STATES)


@app.get("/api/generate")
def generate():
    code = request.args.get("code", "").strip().upper()
    name = request.args.get("name", "").strip()
    state = request.args.get("state", "").strip()
    dob_raw = request.args.get("dob", "").strip()

    try:
        dob = date.fromisoformat(dob_raw)
    except ValueError:
        return jsonify({"error": "A valid date of birth is required."}), 400

    if not is_of_age(dob, MIN_AGE):
        return jsonify({"error": f"Must be at least {MIN_AGE} years old."}), 400

    if not access_code_manager.try_use_code(code):
        return jsonify({"error": "Invalid or fully used access code."}), 400

    profile_number = profile_number_generator.generate_unique_random_profile_number()
    valid = is_valid_number(profile_number, calculate_luhn_check_digit)
    return jsonify({
        "name": name,
        "state": state,
        "dob": dob.isoformat(),
        "profile_number": profile_number,
        "valid": valid,
        "code_uses_remaining": access_code_manager.remaining_uses(code),
    })


@app.post("/telegram/webhook")
def telegram_webhook():
    update = request.get_json(silent=True) or {}
    message = update.get("message")
    if not message or "text" not in message:
        return jsonify({"ok": True})

    chat_id = message["chat"]["id"]
    text = message["text"].strip()

    if text == "/start":
        telegram_sessions[chat_id] = {"step": "name"}
        send_telegram_message(
            chat_id,
            "Let's generate your profile number! What's your name?\n(Send /cancel at any time to stop.)",
        )
        return jsonify({"ok": True})

    if text == "/cancel":
        telegram_sessions.pop(chat_id, None)
        send_telegram_message(chat_id, "Cancelled.")
        return jsonify({"ok": True})

    session = telegram_sessions.get(chat_id)
    if session is None:
        send_telegram_message(chat_id, "Send /start to begin.")
        return jsonify({"ok": True})

    step = session["step"]

    if step == "name":
        session["name"] = text
        session["step"] = "state"
        send_telegram_message(chat_id, "Which state? Type one of:\n" + ", ".join(US_STATES))
        return jsonify({"ok": True})

    if step == "state":
        state = STATES_LOWER.get(text.lower())
        if state is None:
            send_telegram_message(chat_id, "That's not a recognized state. Please type one from the list.")
            return jsonify({"ok": True})
        session["state"] = state
        session["step"] = "dob"
        send_telegram_message(chat_id, "What's your date of birth? (YYYY-MM-DD)")
        return jsonify({"ok": True})

    if step == "dob":
        try:
            dob = date.fromisoformat(text)
        except ValueError:
            send_telegram_message(chat_id, "Please send the date as YYYY-MM-DD, e.g. 1990-05-01.")
            return jsonify({"ok": True})

        if not is_of_age(dob, MIN_AGE):
            send_telegram_message(chat_id, f"You must be at least {MIN_AGE} years old to get a profile number.")
            return jsonify({"ok": True})

        profile_number = profile_number_generator.generate_unique_random_profile_number()
        valid = is_valid_number(profile_number, calculate_luhn_check_digit)
        send_telegram_message(
            chat_id,
            "Here's your profile number:\n"
            f"Name: {session['name']}\n"
            f"State: {session['state']}\n"
            f"DOB: {dob.isoformat()}\n"
            f"Profile Number: {profile_number}\n"
            f"Valid: {valid}",
        )
        telegram_sessions.pop(chat_id, None)
        return jsonify({"ok": True})

    return jsonify({"ok": True})


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
