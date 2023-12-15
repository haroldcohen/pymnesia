"""Provides with fixtures to build expected entities.
"""
import pytest

__all__ = [
    "use_properties",
    "expected_entities",
]


@pytest.fixture()
def use_properties(request):  # pylint: disable=redefined-outer-name
    """Provides with the possibility to pass values to be used when instantiating an entity class.
    IMPORTANT NOTE: This fixture is to be used for very few tests alone, ones that don't require interactions with a
    unit of work. For any other need, please use the seeding fixtures.

    :param request: The parametrized fixture.
    :return: A dictionary of values to be used or an empty dictionary.
    """
    if hasattr(request, "param"):
        return request.param
    return {}


@pytest.fixture()
def expected_entities():
    """Provides with an empty list to be mutated by appropriate fixtures with expected entities.

    :return: An empty list to be mutated with expected entities.
    """
    return []
