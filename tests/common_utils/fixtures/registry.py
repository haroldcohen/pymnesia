"""Provides with registry related fixtures.
"""
import pytest

from pymnesia.core.entities.registry import DEFAULT_E_CLASSES_REGISTRY

_all__ = [
    "unregister_entity_classes",
]


@pytest.fixture(scope="class")
def unregister_entity_classes(
        entity_cls,
        rel_entity_classes,
):
    """Allows to unregister an entity class.

    :param entity_cls: The main entity class to unregister.
    :param rel_entity_classes: The related entity classes to unregister.
    """
    yield None
    for entity_cls_ in rel_entity_classes:
        DEFAULT_E_CLASSES_REGISTRY.unregister(entity_cls_)
    DEFAULT_E_CLASSES_REGISTRY.unregister(entity_cls)
