"""Provides with an interface for """
from abc import ABC, abstractmethod

from pymnesia.core.unit_of_work.memento.base import UnitOfWorkMemento


class OriginatorInterface(ABC):

    @abstractmethod
    def save(self) -> UnitOfWorkMemento:
        """Saves the current unit of work and returns a memento"""

    @abstractmethod
    def restore(self, memento: UnitOfWorkMemento):
        """Restores a unit of work states from a previous memento"""
