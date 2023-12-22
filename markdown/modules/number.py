"""Operations with numbers."""

from modules import array

class NotPositiveException(ValueError):
    """An exception that is raised when a number is not positive.

    This exception inherits from the built-in ValueError class 
    and overrides the __init__ method to provide a custom message.
    """

    def __init__(self):
        """Initializes the exception with a message.

        The message is 'Number is not positive.' and is passed to the
        super class constructor.
        """
        super().__init__('Number is not positive.')


def check_if_is_positive(number):
    """Checks if a number is positive and raises an exception if not.

    This function takes a number as an argument and compares it to zero.
    If the number is less than or equal to zero, it raises
    a NotPositiveException. Otherwise, it does nothing.

    Args:
        number (int or float): The number to check.

    Returns:
        None

    Raises:
        NotPositiveException: If the number is not positive.

    Examples:
        >>> check_if_is_positive(5)
        >>> check_if_is_positive(-3)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "<stdin>", line 5, in check_if_is_positive
        NotPositiveException: Number is not positive.
    """
    if number <= 0:
        raise NotPositiveException


def check_if_number_is_in_range(number, start, end, number_name):
    """Checks if a number is in a given range and raises an exception if not.

    This function takes four arguments: a number, a start value, an end value,
    and a name for the number. It uses the array module to create a range of
    numbers from start to end inclusive, and checks if the number is in that range.
    If the number is not in the range, it raises a ValueError with a 
    message that includes the number name and the range. Otherwise, it does nothing.

    Args:
        number (int or float): The number to check.
        start (int or float): The lower bound of the range.
        end (int or float): The upper bound of the range.
        number_name (str): The name of the number.

    Returns:
        None

    Raises:
        ValueError: If the number is not in the range.

    Examples:
        >>> check_if_number_is_in_range(3, 1, 5, 'x')
        >>> check_if_number_is_in_range(7, 1, 5, 'y')
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "<stdin>", line 8, in check_if_number_is_in_range
        ValueError: y must be in range from 1 to 5 inclusive.
    """
    if not number in array.get_range_inclusive(start, end):
        raise ValueError(f'{number_name} must be in ' + \
        f'range from {start} to {end} inclusive.')
