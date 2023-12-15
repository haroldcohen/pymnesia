"""Provides with fixtures to build expected entities.
"""
import pytest

__all__ = [
    "use_properties",
    "expected_entities",
]


@pytest.fixture()
def use_properties(request):  # pylint: disable=redefined-outer-name
    if hasattr(request, "param"):
        return request.param
    return {}


@pytest.fixture()
def expected_entities():
    return []
