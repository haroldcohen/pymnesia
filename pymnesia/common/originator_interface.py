"""Provides with an interface for """
from abc import ABC, abstractmethod

from pymnesia.unit_of_work.memento import UnitOfWorkMemento


class OriginatorInterface(ABC):

    @abstractmethod
    def save(self) -> UnitOfWorkMemento:
        """Saves the current unit of work and returns a memento"""
