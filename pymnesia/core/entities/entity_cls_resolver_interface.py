"""Provides with an interface for EntityClassResolver.
"""
from abc import ABC, abstractmethod
from typing import Type

from pymnesia.core.entities.entity import Entity


class EntityClassResolverInterface(ABC):
    @abstractmethod
    def update_entity_cls(self, entity_cls: Type[Entity]):
        """
        :param entity_cls:
        :return:
        """
