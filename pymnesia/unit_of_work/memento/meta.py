"""Provides with a memento for UnitOfWork.
"""
from dataclasses import make_dataclass, field
from typing import Dict
from uuid import UUID

from pymnesia.entities.registry.interface import PymnesiaRegistryInterface
from pymnesia.unit_of_work.memento.base import UnitOfWorkMemento

__all__ = [
    "UnitOfWorkMementoMeta",
    "unit_of_work_metaclass",
]


class UnitOfWorkMementoMeta(type):
    """Metaclass for UnitOfWorkMemento.
    """
    _registry: PymnesiaRegistryInterface = None

    def __new__(mcs, name, bases, attrs):  # pylint: disable=unused-argument
        return make_dataclass('UnitOfWorkMemento', make_fields(mcs._registry), bases=(UnitOfWorkMemento,))


def make_fields(entities_registry) -> list:
    """Makes the required fields for UnitOfWorkMemento, based on the registered entities.
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


def unit_of_work_metaclass(registry_: PymnesiaRegistryInterface):
    """UnitOfWorkMemento metaclass maker.

    :param registry_:
    :return:
    """
    return type(
        UnitOfWorkMementoMeta.__name__,
        (UnitOfWorkMementoMeta,),
        {"_registry": registry_}
    )
