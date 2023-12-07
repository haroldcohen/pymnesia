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
):  # pylint: disable=redefined-outer-name
    """Returns an entity instance to be used for assertion (and action as well)."""
    if hasattr(request, "param"):
        return request.param

    return None


@pytest.fixture()
def expected_entities(
        request,
):  # pylint: disable=redefined-outer-name
    """Returns multiple entity instances to be used for assertion (and action as well)."""
    if hasattr(request, "param"):
        return request.param

    return []


@pytest.fixture()
def use_properties(request):  # pylint: disable=redefined-outer-name
    if hasattr(request, "param"):
        return request.param
    return {}
