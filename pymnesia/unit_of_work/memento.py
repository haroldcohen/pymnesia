"""Provides with a memento for UnitOfWork.
"""
from dataclasses import make_dataclass, field

__all__ = ["UnitOfWorkMemento"]

from typing import Dict
from uuid import UUID

from pymnesia.entities.registry import registry


def make_fields(entities_registry) -> list:
    """
    Makes the required fields for UnitOfWorkMemento, based on the registered entities
    :param entities_registry: The registry to use for build.

    :return: A list of fields.
    """
    fields = [("state", int)]
    fields += [
        (
            entity_cls_resolver.__tablename__,
            Dict[UUID, entity_cls_resolver],
            field(default_factory=lambda: {})  # pylint: disable=invalid-field-call
        ) for entity_cls_resolver in entities_registry.all_configs()
    ]

    return fields


UnitOfWorkMemento = make_dataclass('UnitOfWorkMemento', make_fields(registry))
