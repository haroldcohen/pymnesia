"""Provides with an exception raised when a tablename was not declared.
"""


class MissingTablenameException(Exception):
    def __init__(self):
        super().__init__("Entity was declared without a tablename.")
