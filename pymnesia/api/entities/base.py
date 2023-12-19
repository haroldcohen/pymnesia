"""Provides with entity class declaration related APIs.
"""
from typing import Type

from pymnesia.core.entities.base import DeclarativeBase

__all__ = [
    "declarative_base",
]


def declarative_base() -> Type[DeclarativeBase]:
    """Returns the base class to declare an entity.

    :return: The declarative base for entity classes.
    """
    return DeclarativeBase
