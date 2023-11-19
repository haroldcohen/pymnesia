"""Provides with entities related api functions.
"""
from pymnesia.entities.relations import Relation


def relation(reverse: str, is_nullable: bool = True) -> Relation:
    """Returns a Relation instance.
    This instance is to be processed later on by the entity metaclass.

    :param reverse:
    :param is_nullable:
    :return:
    """
    return Relation(
        reverse=reverse,
        is_nullable=is_nullable,
    )
