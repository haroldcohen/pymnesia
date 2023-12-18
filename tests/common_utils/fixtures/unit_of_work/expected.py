"""Provides with fixtures to build expected unit of works.
"""
import time
from typing import List

import pytest

__all__ = [
    "expected_unit_of_work_memento",
    "is_delete_op",
]

# pylint: disable=redefined-outer-name


from pymnesia.core.entities.entity import Entity
from pymnesia.core.unit_of_work.memento.base import UnitOfWorkMemento
from pymnesia.core.entities.registry import DEFAULT_E_CLASSES_REGISTRY
from pymnesia.core.unit_of_work.memento.meta import unit_of_work_metaclass


@pytest.fixture()
def is_delete_op(request) -> bool:
    if hasattr(request, "param"):
        return request.param
    return False


@pytest.fixture()
def expected_unit_of_work_memento(
        expected_entities: List[Entity],
        is_delete_op: bool,
) -> UnitOfWorkMemento:
    """Returns a unit of work memento instance to be used for assertion (and action as well).

    :param expected_entities: A list of expected entities that should be present in the expected uow memento.
    :param is_delete_op:
    :return: A unit of work memento containing expected entities.
    """
    uow_cls = unit_of_work_metaclass(registry_=DEFAULT_E_CLASSES_REGISTRY)(
        "UnitOfWorkMemento",
        (UnitOfWorkMemento,),
        {},
    )
    memento = uow_cls(state=time.time_ns())
    if not is_delete_op:
        for expected_entity_ in expected_entities:
            table = getattr(memento, expected_entity_.__tablename__)
            table[expected_entity_.id] = expected_entity_

    return memento
