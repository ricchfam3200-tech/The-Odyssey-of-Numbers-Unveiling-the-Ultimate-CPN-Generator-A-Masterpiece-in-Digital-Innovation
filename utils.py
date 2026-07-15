from typing import Callable, Union


def is_valid_number(number: Union[int, str], check_digit_func: Callable[[Union[int, str]], int]) -> bool:
    """
    Validates a given number using a check digit function.
    
    Args:
        number (Union[int, str]): The number to validate.
        check_digit_func (Callable): The function to calculate the check digit.
        
    Returns:
        bool: True if the number is valid, False otherwise.
    """
    return check_digit_func(number) == 0

def validate_input_number(number: Union[int, str], min_profile_number: int, max_profile_number: int) -> bool:
    """
    Validates the input number to check if it's within the acceptable range.

    Args:
        number (Union[int, str]): The number to validate.
        min_profile_number (int): The minimum acceptable profile number.
        max_profile_number (int): The maximum acceptable profile number.

    Returns:
        bool: True if the number is valid, False otherwise.
    """
    try:
        num = int(number)
        return min_profile_number <= num <= max_profile_number
    except ValueError:
        return False
