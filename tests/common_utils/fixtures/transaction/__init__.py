"""Provides with unit of work related fixtures.
"""
import pytest

from pymnesia.core.transaction.transaction import InMemoryTransaction
from pymnesia.core.unit_of_work.unit_of_work import UnitOfWork
from pymnesia.api.command import transaction as api_transaction

__all__ = ["transaction"]


@pytest.fixture()
def transaction(unit_of_work: UnitOfWork) -> InMemoryTransaction:
    """Returns a transaction for the current unit of work.

    :param unit_of_work: The unit of work for which to create a transaction.
    :return: A new InMemoryTransaction.
    """
    return api_transaction(unit_of_work=unit_of_work)
