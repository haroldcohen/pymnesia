"""Provides with EntityClassResolver.
"""
from typing import Type

from pymnesia.entities.entity import Entity
from pymnesia.entities.registry.interface import PymnesiaRegistryInterface


class EntityClassResolver:
    """Resolver that instantiates the proper entity class when called.
    """

    def __init__(
            self,
            entity_cls: Type[Entity],
            registry: PymnesiaRegistryInterface,
    ):
        self._entity_cls = entity_cls
        self._registry = registry

    def __call__(self, *args, **kwargs):
        return self._entity_cls(*args, **kwargs)

    def __getattr__(self, item):
        return getattr(self._entity_cls, item)

    def update_entity_cls(self, entity_cls):
        self._entity_cls = entity_cls
