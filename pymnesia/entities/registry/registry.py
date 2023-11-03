"""Provides with a registry to store and use entities' configuration.
"""
from pymnesia.entities.entity_resolver import EntityClassResolver
from pymnesia.entities.registry.interface import PymnesiaRegistryInterface


class PymnesiaRegistry(PymnesiaRegistryInterface):
    """Registry class that stores entity configurations.
    """

    def __init__(self):
        self._entries = []

    def register(self, entity_class):
        """Adds an entity class to the registry.
        :param entity_class: The entity class to add to the registry.
        :return:
        """
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

    def all_configs(self):
        for resolver in self._entries:
            yield resolver
