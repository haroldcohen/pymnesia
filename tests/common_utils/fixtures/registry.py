"""Provides with registry related fixtures.
"""
import pytest
from pymnesia.entities.registry import registry

_all__ = ["unregister_entity_class"]


@pytest.fixture()
def unregister_entity_class(entity_class):
    """Allows to unregister an entity class.
    Useful when testing using the make fixture.

    :param entity_class: The entity class to unregister.
    """
    yield None
    registry.unregister(entity_class)
