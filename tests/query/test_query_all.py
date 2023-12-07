"""Provides with unit tests to validate the query all feature.
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
    "expected_entities",
    [
        ([InMemoryProduct(id=uuid4()), InMemoryProduct(id=uuid4())]),
        ([InMemoryOrder(id=uuid4())]),
    ],
    indirect=True,
)
def test_query_an_entity_table_should_return_all_its_entities(
        unit_of_work,
        transaction,
        expected_entities,
        populate_entities,
):
    # Act
    result = getattr(unit_of_work.query(), expected_entities[0].__tablename__)().fetch()
    # Assert
    assert_that(
        result,
        equal_to(expected_entities)
    )
