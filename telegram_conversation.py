from datetime import date

from constants import MIN_AGE, US_STATES
from luhn_algorithm import calculate_luhn_check_digit
from main import ProfileNumberGenerator, is_of_age
from utils import is_valid_number

STATES_LOWER = {state.lower(): state for state in US_STATES}

# Per-chat conversation state, keyed by Telegram chat id. Kept in memory, which is fine as long
# as the bot runs as a single process.
telegram_sessions = {}

profile_number_generator = ProfileNumberGenerator()


def handle_telegram_message(chat_id, text, send_message):
    """Advances the per-chat conversation state machine and replies via send_message(chat_id, text)."""
    text = text.strip()

    if text == "/start":
        telegram_sessions[chat_id] = {"step": "name"}
        send_message(
            chat_id,
            "Let's generate your profile number! What's your name?\n(Send /cancel at any time to stop.)",
        )
        return

    if text == "/cancel":
        telegram_sessions.pop(chat_id, None)
        send_message(chat_id, "Cancelled.")
        return

    session = telegram_sessions.get(chat_id)
    if session is None:
        send_message(chat_id, "Send /start to begin.")
        return

    step = session["step"]

    if step == "name":
        session["name"] = text
        session["step"] = "state"
        send_message(chat_id, "Which state? Type one of:\n" + ", ".join(US_STATES))
        return

    if step == "state":
        state = STATES_LOWER.get(text.lower())
        if state is None:
            send_message(chat_id, "That's not a recognized state. Please type one from the list.")
            return
        session["state"] = state
        session["step"] = "dob"
        send_message(chat_id, "What's your date of birth? (YYYY-MM-DD)")
        return

    if step == "dob":
        try:
            dob = date.fromisoformat(text)
        except ValueError:
            send_message(chat_id, "Please send the date as YYYY-MM-DD, e.g. 1990-05-01.")
            return

        if not is_of_age(dob, MIN_AGE):
            send_message(chat_id, f"You must be at least {MIN_AGE} years old to get a profile number.")
            return

        profile_number = profile_number_generator.generate_unique_random_profile_number()
        valid = is_valid_number(profile_number, calculate_luhn_check_digit)
        send_message(
            chat_id,
            "Here's your profile number:\n"
            f"Name: {session['name']}\n"
            f"State: {session['state']}\n"
            f"DOB: {dob.isoformat()}\n"
            f"Profile Number: {profile_number}\n"
            f"Valid: {valid}",
        )
        telegram_sessions.pop(chat_id, None)
