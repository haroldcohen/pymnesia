"""Provides with fixtures to build expected unit of works.
"""
import time

import pytest

__all__ = ["expected_unit_of_work_memento"]

from pymnesia.unit_of_work.memento.base import UnitOfWorkMemento
from pymnesia.entities.registry import registry
from pymnesia.unit_of_work.memento.meta import unit_of_work_metaclass


@pytest.fixture()
def expected_unit_of_work_memento(expected_entities) -> UnitOfWorkMemento:
    """Returns a unit of work memento instance to be used for assertion (and action as well).
    """
    uow_cls = unit_of_work_metaclass(registry_=registry)(
        "UnitOfWorkMemento",
        (UnitOfWorkMemento,),
        {},
    )
    memento = uow_cls(state=time.time_ns())
    for expected_entity_ in expected_entities:
        table = getattr(memento, expected_entity_.__tablename__)
        table[expected_entity_.id] = expected_entity_

    return memento
