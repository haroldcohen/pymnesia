"""Provides with a registry to store and use entities' configuration.
"""
from typing import Generator

from pymnesia.core.entities.entity_resolver import EntityClassResolver
from pymnesia.core.entities.registry.interface import PymnesiaRegistryInterface


class PymnesiaRegistry(PymnesiaRegistryInterface):
    """Registry class that stores entity configurations.
    """

    def __init__(self):
        self._entries = []

    def register(self, entity_class) -> EntityClassResolver:
        resolver_cls = type(
            entity_class.__name__,
            (EntityClassResolver,),
            {}
        )
        resolver = resolver_cls(
            entity_cls=entity_class,
            registry=self,
        )
        self._entries.append(resolver)

        return resolver

    def unregister(self, entity_cls_resolver):
        self._entries.remove(entity_cls_resolver)

    def all_configs(self) -> Generator[EntityClassResolver, None, None]:
        for resolver in self._entries:
            yield resolver
