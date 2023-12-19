"""Provides with various utility functions to generate random strings.
"""
import random

__all__ = [
    "random_alphanum_str",
    "random_special_char_str",
]


def random_alphanum_str(str_len: int) -> str:
    """Generates a random alphanumeric string based on a given length.

    :param str_len: The length of the string to be generated.
    :return: A randomly generated string containing alphanumeric characters.
    """
    txt = []
    for i in range(0, str_len):  # pylint: disable=unused-variable
        txt.append(chr(random.randint(97, 122)))

    return "".join(txt)


def random_special_char_str(str_len: int) -> str:
    """Generates a random string of special characters based on a given length.

    :param str_len: The length of the string to be generated.
    :return: A randomly generated string containing special characters.
    """
    txt = []
    for i in range(0, str_len):  # pylint: disable=unused-variable
        txt.append(chr(random.randint(33, 46)))

    return "".join(txt)
