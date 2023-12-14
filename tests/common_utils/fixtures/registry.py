"""Provides with registry related fixtures.
"""
import pytest

from pymnesia.entities.registry import registry

_all__ = [
    "unregister_entity_classes",
]


@pytest.fixture(scope="class")
def unregister_entity_classes(
        entity_cls,
        rel_entity_classes,
):
    """Allows to unregister an entity class.
    Useful when testing using the make fixture.

    :param entity_cls: The main entity class to unregister.
    :param rel_entity_classes: The related entity classes to unregister.
    """
    yield None
    for entity_cls_ in rel_entity_classes:
        registry.unregister(entity_cls_)
    registry.unregister(entity_cls)
