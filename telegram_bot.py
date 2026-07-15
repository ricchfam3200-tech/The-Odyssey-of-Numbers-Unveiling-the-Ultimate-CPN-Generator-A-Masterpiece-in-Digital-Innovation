import logging
import os
from datetime import date

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from constants import MIN_AGE, US_STATES
from luhn_algorithm import calculate_luhn_check_digit
from main import ProfileNumberGenerator, is_of_age
from utils import is_valid_number

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/profile_number_generator.log", level=logging.INFO)

NAME, STATE, DOB = range(3)

profile_number_generator = ProfileNumberGenerator()
STATES_LOWER = {state.lower(): state for state in US_STATES}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Let's generate your profile number! What's your name?\n"
        "(Send /cancel at any time to stop.)"
    )
    return NAME


async def received_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text.strip()

    keyboard = [US_STATES[i:i + 3] for i in range(0, len(US_STATES), 3)]
    await update.message.reply_text(
        "Which state?",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return STATE


async def received_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    state = STATES_LOWER.get(update.message.text.strip().lower())
    if state is None:
        await update.message.reply_text("That's not a recognized state. Please pick one from the list.")
        return STATE

    context.user_data["state"] = state
    await update.message.reply_text(
        "What's your date of birth? (YYYY-MM-DD)",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DOB


async def received_dob(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        dob = date.fromisoformat(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("Please send the date as YYYY-MM-DD, e.g. 1990-05-01.")
        return DOB

    if not is_of_age(dob, MIN_AGE):
        await update.message.reply_text(f"You must be at least {MIN_AGE} years old to get a profile number.")
        return DOB

    name = context.user_data["name"]
    state = context.user_data["state"]
    profile_number = profile_number_generator.generate_unique_random_profile_number()
    valid = is_valid_number(profile_number, calculate_luhn_check_digit)

    await update.message.reply_text(
        "Here's your profile number:\n"
        f"Name: {name}\n"
        f"State: {state}\n"
        f"DOB: {dob.isoformat()}\n"
        f"Profile Number: {profile_number}\n"
        f"Valid: {valid}"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def build_application() -> Application:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    application = Application.builder().token(token).build()

    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_name)],
            STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_state)],
            DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_dob)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conversation)
    return application


if __name__ == "__main__":
    build_application().run_polling()
