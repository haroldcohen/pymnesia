"""Provides with registry related fixtures.
"""
import pytest

from pymnesia.entities.registry import registry

_all__ = ["unregister_entity_class", "unregister_entity_classes"]


@pytest.fixture()
def unregister_entity_class(entity_class):
    """Allows to unregister an entity class.
    Useful when testing using the make fixture.

    :param entity_class: The entity class to unregister.
    """
    yield None
    registry.unregister(entity_class)


@pytest.fixture()
def unregister_entity_classes(related_entity_classes):
    """Allows to unregister an entity class.
    Useful when testing using the make fixture.

    :param related_entity_classes: The entity classes to unregister.
    """
    yield None
    for entity_cls in related_entity_classes:
        registry.unregister(entity_cls)
