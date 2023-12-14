"""Provides with various functions to generate random strings.
"""
import random

__all__ = [
    "random_alphanum_str",
    "random_special_char_str",
]


def random_alphanum_str(str_len: int) -> str:
    txt = []
    for i in range(0, str_len):  # pylint: disable=unused-variable
        txt.append(chr(random.randint(97, 122)))

    return "".join(txt)


def random_special_char_str(str_len: int) -> str:
    txt = []
    for i in range(0, str_len):  # pylint: disable=unused-variable
        txt.append(chr(random.randint(33, 46)))

    return "".join(txt)
