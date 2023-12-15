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
    return getattr(unit_of_work.query(), entity_cls.__tablename__)()
