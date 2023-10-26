"""Provides with various functions for querying.
Filter functions are located in a dedicated module.
"""
from typing import Iterable


def order_by(entities: Iterable, direction: str, order_by_key: str) -> list:
    """
    Orders (sort) a query result by a key.

    :param entities: The entities to order by.
    :param direction: Whether the result should be ordered by in an ascending or descending way.
    :param order_by_key: The property to use for ordering.
    :return: A list of sorted entities.
    """
    return sorted(entities, key=lambda e: getattr(e, order_by_key), reverse=direction == "desc")
