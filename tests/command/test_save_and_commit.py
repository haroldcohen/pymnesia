"""Provides with unit tests to validate save and commit features.
"""
from uuid import uuid4

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.entities.order import InMemoryOrder
from tests.common_utils.entities.product import InMemoryProduct
from pymnesia.unit_of_work.unit_of_work import UnitOfWork
from pymnesia.transaction.transaction import InMemoryTransaction
from tests.common_utils.fixtures.unit_of_work.expected import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.unit_of_work import *


@pytest.mark.parametrize(
    "expected_entity",
    [
        (InMemoryProduct(id=uuid4())),
        (InMemoryProduct(id=uuid4())),
        (InMemoryOrder(id=uuid4())),
    ],
    indirect=True
)
def test_save_an_entity_and_commit_should_update_unit_of_work_with_an_entity(
        time_ns,
        unit_of_work,
        mocked_time_ns,
        expected_unit_of_work_memento,
        expected_entity,
):
    """Tests whether saving and committing an entity updates the unit of work."""
    # Arrange
    transaction = InMemoryTransaction(originator=unit_of_work)

    # Act
    unit_of_work.save_entity(entity=expected_entity)
    transaction.commit()

    # Assert
    retrieved_entity = getattr(unit_of_work, expected_entity.config.table_name)[expected_entity.id]
    *_, last = transaction.history()
    assert_that(
        last,
        equal_to(expected_unit_of_work_memento)
    )
    assert_that(
        retrieved_entity,
        equal_to(expected_entity)
    )


@pytest.mark.parametrize(
    "expected_entities",
    [
        ([InMemoryProduct(id=uuid4()), InMemoryProduct(id=uuid4())])
    ],
    indirect=True,
)
def test_save_multiple_entities_and_commit_should_update_unit_of_work_with_multiple_entities(
        time_ns,
        mocked_time_ns,
        expected_entities,
        expected_unit_of_work_memento,
):
    """Tests whether saving and committing multiple entities updates the unit of work."""
    # Arrange
    unit_of_work = UnitOfWork(state=time_ns)
    transaction = InMemoryTransaction(originator=unit_of_work)

    # Act
    for expected_entity in expected_entities:
        unit_of_work.save_entity(entity=expected_entity)
    transaction.commit()

    # Assert
    *_, last = transaction.history()
    assert_that(
        last,
        equal_to(expected_unit_of_work_memento)
    )
    for expected_entity in expected_entities:
        retrieved_entity = getattr(unit_of_work, expected_entity.config.table_name)[expected_entity.id]
        assert_that(
            retrieved_entity,
            equal_to(expected_entity)
        )

