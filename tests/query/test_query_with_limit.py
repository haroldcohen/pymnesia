"""Provides with unit tests to validate the query with a limit clause feature.
"""
from uuid import uuid4

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.entities.order import InMemoryOrder
from tests.common_utils.entities.product import InMemoryProduct
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.unit_of_work.expected import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.populate import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.misc import *


@pytest.mark.parametrize(
    "entities, expected_entities, limit",
    [
        ([InMemoryProduct(id=uuid4())], [InMemoryProduct(id=uuid4())], 1),
        ([InMemoryOrder(id=uuid4())], [InMemoryOrder(id=uuid4()), InMemoryOrder(id=uuid4())], 2),
    ],
    indirect=True,
)
def test_query_an_entity_table_with_a_limit_should_return_a_number_of_limited_entities(
        time_ns,
        mocked_time_ns,
        unit_of_work,
        transaction,
        expected_unit_of_work_memento,
        limit,
        entities,
        expected_entities,
        populate_entities,
):
    # Act
    result = getattr(unit_of_work.query(), expected_entities[0].__tablename__)().limit(limit=limit).fetch()
    # Assert
    assert_that(
        result,
        equal_to(expected_entities)
    )
