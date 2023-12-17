"""Provides with EntityClassResolver.
"""
from typing import Type

from pymnesia.core.entities.entity import Entity
from pymnesia.core.entities.registry.interface import PymnesiaRegistryInterface
from pymnesia.core.entities.entity_cls_resolver_interface import EntityClassResolverInterface


class EntityClassResolver(EntityClassResolverInterface):
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

    def update_entity_cls(self, entity_cls: Type[Entity]):
        """Updates the entity class associated with the resolver.

        :param entity_cls: The updated entity class.
        :return: None
        """
        self._entity_cls = entity_cls
