"""Provides with an interface for """
from abc import ABC, abstractmethod
from typing import Type


class OriginatorInterface(ABC):

    @abstractmethod
    def save(self) -> Type["UnitOfWorkMementoMeta"]:
        """Saves the current unit of work and returns a memento"""
