"""Provides with an interface for PymnesiaRegistry.
"""
from abc import ABC, abstractmethod
from typing import Type

from pymnesia.entities.entity import Entity


class PymnesiaRegistryInterface(ABC):
    """Interface for Pymnesia registry.
    """

    @abstractmethod
    def register(self, entity_class: Type[Entity]):
        """Registers an entity class by adding its resolver to the registry.
        The resolver will later be used to manage proper entity class instantiations.

        :param entity_class: The entity class to register.
        :return: None
        """

    @abstractmethod
    def unregister(self, entity_cls_resolver):
        """Disposes of an entity class by removing its resolver from the registry.

        :param entity_cls_resolver: The entity class' resolver
        :return: None
        """

    @abstractmethod
    def all_configs(self):
        """Iterator that returns all the registered entity class resolvers.

        :return: A generator yielding EntityClassResolver instances.
        """
