"""Provides with an in memory transaction.
"""
from typing import Generator, List

from pymnesia.common.originator_interface import OriginatorInterface

__all__ = ["InMemoryTransaction"]

from pymnesia.unit_of_work.memento import UnitOfWorkMemento


class InMemoryTransaction:
    """Caretaker for in memory unit of works."""

    def __init__(self, originator: OriginatorInterface):
        self.__originator = originator
        self.__mementos: List[UnitOfWorkMemento] = []

    def commit(self):
        """
        Commits the current state of the originator
        """
        self.__mementos.append(self.__originator.save())

    def history(self) -> Generator[UnitOfWorkMemento, None, None]:
        """
        Yields every memento stored.
        :return: 
        """
        for memento in self.__mementos:
            yield memento
