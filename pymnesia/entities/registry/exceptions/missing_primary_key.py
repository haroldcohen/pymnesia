"""Provides with an exception raised when a primary key was not declared.
"""


class MissingPrimaryKeyException(Exception):
    def __init__(self):
        super().__init__("Entity was declared without a primary key.")
