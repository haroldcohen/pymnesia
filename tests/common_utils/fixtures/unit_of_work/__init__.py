"""Provides with unit of work related fixtures.
"""
import pytest

from pymnesia.unit_of_work.unit_of_work import UnitOfWork

__all__ = ["unit_of_work"]


@pytest.fixture()
def unit_of_work(time_ns: int) -> UnitOfWork:
    return UnitOfWork(state=time_ns)
