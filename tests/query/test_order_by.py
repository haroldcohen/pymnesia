"""Provides with unit tests to validate the order by feature.
"""
from uuid import uuid4

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.entities.order import InMemoryOrder
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.unit_of_work.expected import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.populate import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.misc import *


@pytest.mark.parametrize(
    "expected_entities, direction, order_by_key",
    [
        ([
             InMemoryOrder(id=uuid4(), total_amount=3),
             InMemoryOrder(id=uuid4(), total_amount=2)
         ], "asc", "total_amount"),
        ([
             InMemoryOrder(id=uuid4(), total_amount=10),
             InMemoryOrder(id=uuid4(), total_amount=11)
         ], "desc", "total_amount"),
        ([
             InMemoryOrder(id=uuid4(), total_amount=10, vat_not_included_amount=20),
             InMemoryOrder(id=uuid4(), total_amount=20, vat_not_included_amount=11)
         ], "desc", "vat_not_included_amount"),
    ],
    indirect=True,
)
def test_query_and_order_by_should_return_ordered_entities(
        time_ns,
        mocked_time_ns,
        unit_of_work,
        transaction,
        expected_unit_of_work_memento,
        expected_entities,
        populate_entities,
        direction,
        order_by_key,
):
    # Act
    result = getattr(unit_of_work.query(), expected_entities[0].__tablename__)()\
        .order_by(direction, order_by_key)\
        .fetch()
    sorted_entities = sorted(expected_entities, key=lambda e: getattr(e, order_by_key), reverse=direction == "desc")
    # Assert
    assert_that(
        result,
        equal_to(sorted_entities)
    )
