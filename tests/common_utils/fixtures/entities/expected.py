"""Provides with fixtures to build expected entities.
"""
import pytest

__all__ = ["expected_entity", "expected_entities"]


@pytest.fixture()
def expected_entity(request, expected_unit_of_work_memento):
    """Returns an entity instance to be used for assertion (and action as well)."""
    entity = request.param
    table = getattr(expected_unit_of_work_memento, entity.config.table_name)
    table[entity.id] = entity

    return entity


@pytest.fixture()
def expected_entities(request, expected_unit_of_work_memento):
    """Returns multiple entity instances to be used for assertion (and action as well)."""
    for entity in request.param:
        table = getattr(expected_unit_of_work_memento, entity.config.table_name)
        table[entity.id] = entity

    return request.param
