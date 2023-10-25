"""Provides with unit of work related fixtures.
"""
import pytest

__all__ = ["transaction"]

from pymnesia.transaction.transaction import InMemoryTransaction
from pymnesia.unit_of_work.unit_of_work import UnitOfWork


@pytest.fixture()
def transaction(unit_of_work: UnitOfWork) -> InMemoryTransaction:
    return InMemoryTransaction(originator=unit_of_work)
