"""Provides with command related APIs.
"""
from pymnesia.core.transaction.transaction import InMemoryTransaction
from pymnesia.core.unit_of_work.unit_of_work import UnitOfWork


def transaction(unit_of_work: UnitOfWork) -> InMemoryTransaction:
    """Returns a transaction for a given unit of work.

    :param unit_of_work: The unit of work for which to create a transaction.
    :return: A new InMemoryTransaction.
    """
    return InMemoryTransaction(originator=unit_of_work)
