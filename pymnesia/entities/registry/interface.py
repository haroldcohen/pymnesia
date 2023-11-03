"""Provides with an interface for PymnesiaRegistry.
"""
from abc import ABC, abstractmethod


class PymnesiaRegistryInterface(ABC):
    """Interface for Pymnesia registry.
    """

    @abstractmethod
    def register(self, entity_class):
        """
        :param entity_class:
        :return:
        """

    @abstractmethod
    def unregister(self, entity_cls_resolver):
        """
        :param entity_cls_resolver:
        :return:
        """

    @abstractmethod
    def all_configs(self):
        """
        :return:
        """
