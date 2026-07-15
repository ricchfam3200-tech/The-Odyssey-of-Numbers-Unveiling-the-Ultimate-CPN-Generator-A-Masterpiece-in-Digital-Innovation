import json
import logging
import secrets
from time import sleep

import requests

from constants import MAX_PROFILE_NUMBER, MIN_PROFILE_NUMBER
from luhn_algorithm import calculate_luhn_check_digit
from utils import is_valid_number

# Initialize logging
logging.basicConfig(filename='logs/profile_number_generator.log', level=logging.INFO)


class ProfileNumberGenerator:

    def __init__(self):
        self.generated_profile_numbers = set()

    def generate_random_profile_number(self) -> int:
        profile_number = secrets.SystemRandom().randint(MIN_PROFILE_NUMBER,
                                                    MAX_PROFILE_NUMBER)
        check_digit = calculate_luhn_check_digit(profile_number)
        return profile_number if check_digit == 0 else self.generate_random_profile_number(
        )

    def generate_unique_random_profile_number(self) -> int:
        profile_number = self.generate_random_profile_number()
        while profile_number in self.generated_profile_numbers:
            profile_number = self.generate_random_profile_number()
        self.generated_profile_numbers.add(profile_number)
        return profile_number


def log_message(message: str, level: str = "info"):
    logging.log(getattr(logging, level.upper()), message)


def display_progress_bar(iteration, total, bar_length=50):
    progress = float(iteration) / float(total)
    arrow = '=' * int(round(progress * bar_length) - 1)
    spaces = ' ' * (bar_length - len(arrow))
    print(f'Progress: [{arrow + spaces}] {int(progress * 100)}%')


def audit_generated_profile_number(profile_number: int):
    with open('logs/audit_log.json', 'a') as f:
        json.dump({'generated_profile_number': profile_number}, f)
        f.write(",\n")


def notify_api_about_new_profile_number(profile_number: int):
    api_endpoint = "https://example.com/api/new_profile_number"
    response = requests.post(api_endpoint, json={"profile_number": profile_number})
    if response.status_code == 200:
        log_message("Successfully notified the API.")
    else:
        log_message(
            f"Failed to notify the API. Status Code: {response.status_code}",
            level="error")


if __name__ == "__main__":
    profile_number_gen = ProfileNumberGenerator()
    num_of_profile_numbers_to_generate = 10  # You can change this number

    for i in range(1, num_of_profile_numbers_to_generate + 1):
        try:
            profile_number = profile_number_gen.generate_unique_random_profile_number()
            log_message(f"Generated Profile Number: {profile_number}")

            is_valid = is_valid_number(profile_number, calculate_luhn_check_digit)
            if is_valid:
                log_message("The profile number is valid.")
                audit_generated_profile_number(profile_number)
                notify_api_about_new_profile_number(profile_number)
            else:
                log_message("The profile number is not valid.", level="error")

            display_progress_bar(i, num_of_profile_numbers_to_generate)
            sleep(0.1)  # Simulate some delay
        except Exception as e:
            log_message(str(e), level="error")
