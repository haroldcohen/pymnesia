"""Provides with querying fixtures.
"""
import pytest

__all__ = [
    "base_query",
]


@pytest.fixture()
def base_query(
        entity_cls,
        unit_of_work,
):
    """Creates and returns a base query.
    Eg: For an entity named 'Shoe' using a table name 'shoes',
    the fixture will return unit_of_work.query().shoes()

    :param entity_cls: The entity class to query.
    :param unit_of_work: The unit of work to query.
    :return: A query for a given entity class and a given unit of work.
    """
    return getattr(unit_of_work.query(), entity_cls.__tablename__)()
