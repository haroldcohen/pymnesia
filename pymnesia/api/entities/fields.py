"""Provides with field related APIs.
"""
from typing import Any, Callable

from pymnesia.core.entities.field import Field, UNDEFINED
from pymnesia.core.entities.relations import Relation


def field(
        default: Any = UNDEFINED,
        default_factory: Callable = UNDEFINED,
):
    """Returns a Field instance.
    The instance is to be processed later on by the entity metaclass and various procedural functions.

    :param default: The default value for the field.
    :param default_factory: A callback used to return a default value for the field.
    :return: A Field instance.
    """
    if default is not UNDEFINED:
        return Field(default=default)
    return Field(default_factory=default_factory)


def relation(
        reverse: str,
        is_nullable: bool = True,
) -> Relation:
    """Returns a Relation instance.
    The instance is to be processed later on by the entity metaclass and various procedural functions.

    :param reverse: The name of the reverse relation.
    :param is_nullable: Whether the relation is nullable or not.
    :return: A Relation instance.
    """
    return Relation(
        reverse=reverse,
        is_nullable=is_nullable,
    )
