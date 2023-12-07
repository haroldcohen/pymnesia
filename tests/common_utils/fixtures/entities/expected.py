"""Provides with fixtures to build expected entities.
"""
import pytest

__all__ = [
    "expected_entity",
    "expected_entities",
    "use_properties",
]


@pytest.fixture()
def expected_entity(
        request,
        expected_unit_of_work_memento,
        use_properties
):  # pylint: disable=redefined-outer-name
    """Returns an entity instance to be used for assertion (and action as well)."""
    if hasattr(request, "param"):
        entity = request.param
        if len(use_properties):
            for prop, value in use_properties.items():
                setattr(entity, prop, value)
        table = getattr(expected_unit_of_work_memento, entity.__tablename__)
        table[entity.id] = entity

        return entity

    return None


@pytest.fixture()
def expected_entities(
        request,
        expected_unit_of_work_memento,
):  # pylint: disable=redefined-outer-name
    """Returns multiple entity instances to be used for assertion (and action as well)."""
    if hasattr(request, "param"):
        for entity in request.param:
            table = getattr(expected_unit_of_work_memento, entity.__tablename__)
            table[entity.id] = entity

        return request.param

    return []


@pytest.fixture()
def use_properties(request):  # pylint: disable=redefined-outer-name
    if hasattr(request, "param"):
        return request.param
    return {}
