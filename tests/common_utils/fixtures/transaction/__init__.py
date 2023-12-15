"""Provides with unit of work related fixtures.
"""
import pytest

from pymnesia.transaction.transaction import InMemoryTransaction
from pymnesia.unit_of_work.unit_of_work import UnitOfWork

__all__ = ["transaction"]


@pytest.fixture()
def transaction(unit_of_work: UnitOfWork) -> InMemoryTransaction:
    """Returns a transaction for the current unit of work.

    :param unit_of_work: The unit of work for which to create a transaction.
    :return: A new InMemoryTransaction.
    """
    return InMemoryTransaction(originator=unit_of_work)
