"""Provides with field related exceptions.
"""


class ConfigIsAReservedKeywordException(Exception):
    """Raised when an entity class is declared with a field named "config".
    """

    def __init__(self):
        super().__init__("'config' is keyword reserved for Pymnesia. Please choose another field name.")
