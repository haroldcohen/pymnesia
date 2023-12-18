"""Provides with field related APIs.
"""
from typing import Any, Callable

from pymnesia.core.entities.field import Field, UNDEFINED


def field(
        default: Any = UNDEFINED,
        default_factory: Callable = UNDEFINED,
):
    """Returns a Field instance.

    :param default: The default value for the field.
    :param default_factory: A callback used to return a default value for the field.
    :return: A Field instance.
    """
    if default is not UNDEFINED:
        return Field(default=default)
    return Field(default_factory=default_factory)
