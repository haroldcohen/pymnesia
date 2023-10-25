"""Provides with fixtures to build expected entities.
"""
import pytest

__all__ = ["expected_entity", "expected_entities", "limit", "direction", "order_by_key"]


@pytest.fixture()
def expected_entity(request, expected_unit_of_work_memento):
    """Returns an entity instance to be used for assertion (and action as well)."""
    if hasattr(request, "param"):
        entity = request.param
        table = getattr(expected_unit_of_work_memento, entity.config.table_name)
        table[entity.id] = entity

        return entity

    return None


@pytest.fixture()
def expected_entities(request, expected_unit_of_work_memento):
    """Returns multiple entity instances to be used for assertion (and action as well)."""
    if hasattr(request, "param"):
        for entity in request.param:
            table = getattr(expected_unit_of_work_memento, entity.config.table_name)
            table[entity.id] = entity

        return request.param

    return []


@pytest.fixture()
def limit(request):
    if hasattr(request, "param"):
        return request.param
    return 0


@pytest.fixture()
def order_by_key(request):
    return request.param


@pytest.fixture()
def direction(request):
    if hasattr(request, "param"):
        return request.param
    return "asc"
