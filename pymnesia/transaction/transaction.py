"""Provides with an in memory transaction.
"""
from typing import Generator, List

from pymnesia.common.originator_interface import OriginatorInterface
from pymnesia.unit_of_work.memento.base import UnitOfWorkMemento

__all__ = [
    "InMemoryTransaction",
]


class InMemoryTransaction:
    """Caretaker for in memory unit of works."""

    def __init__(self, originator: OriginatorInterface):
        self.__originator = originator
        self.__mementos: List[UnitOfWorkMemento] = [self.__originator.save()]

    def commit(self):
        """
        Commits the current state of the originator
        """
        self.__mementos.append(self.__originator.save())

    def rollback(self):
        *_, last = self.history()
        self.__originator.restore(memento=last)

    def history(self) -> Generator[UnitOfWorkMemento, None, None]:
        """
        Yields every memento stored.
        :return: 
        """
        for memento in self.__mementos:
            yield memento
