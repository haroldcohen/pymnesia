"""Provides with unit of work related APIs.
"""
import time

from pymnesia.core.unit_of_work.unit_of_work import UnitOfWork

__all__ = [
    "uow",
]


def uow():
    """Returns an instance of UnitOfWork.
    A unit of work is the equivalent of a database.
    It stores entities and manages their states and related operations, such as save.

    :return: An instance of UnitOfWork.
    """
    return UnitOfWork(state=time.time_ns())
