"""Provides with unit of work related fixtures.
"""
import pytest

from pymnesia.core.unit_of_work.unit_of_work import UnitOfWork
from pymnesia.api.unit_of_work import uow

__all__ = ["unit_of_work"]


@pytest.fixture()
def unit_of_work() -> UnitOfWork:
    return uow()
