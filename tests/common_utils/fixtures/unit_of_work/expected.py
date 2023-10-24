"""Provides with fixtures to build expected unit of works.
"""
import time

import pytest

__all__ = ["expected_unit_of_work_memento"]

from pymnesia.unit_of_work.memento import UnitOfWorkMemento


@pytest.fixture()
def expected_unit_of_work_memento() -> UnitOfWorkMemento:
    """Returns a unit of work memento instance to be used for assertion (and action as well)."""
    memento = UnitOfWorkMemento(
        state=time.time_ns(),
    )

    return memento
