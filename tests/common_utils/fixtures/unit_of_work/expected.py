"""Provides with fixtures to build expected unit of works.
"""
import time

import pytest

__all__ = ["expected_unit_of_work_memento"]

from pymnesia.unit_of_work.memento.default import UnitOfWorkMemento


@pytest.fixture()
def expected_unit_of_work_memento(expected_entity, expected_entities) -> UnitOfWorkMemento:
    """Returns a unit of work memento instance to be used for assertion (and action as well).
    """
    memento = UnitOfWorkMemento(
        state=time.time_ns(),
    )
    if expected_entity:
        table = getattr(memento, expected_entity.__tablename__)
        table[expected_entity.id] = expected_entity
    for expected_entity_ in expected_entities:
        table = getattr(memento, expected_entity_.__tablename__)
        table[expected_entity_.id] = expected_entity_

    return memento
