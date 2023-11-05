"""Provides with unit tests to validate the query one entity feature.
"""
from uuid import uuid4, UUID

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
    "expected_entity",
    [
        (InMemoryProduct(id=UUID("ccdcf537-ab51-4b60-87d7-93ee3f27454e"))),
        (InMemoryOrder(id=uuid4())),
    ],
    indirect=True,
)
def test_query_an_entity_table_should_return_the_first_entity(
        time_ns,
        mocked_time_ns,
        unit_of_work,
        transaction,
        expected_unit_of_work_memento,
        expected_entity,
        populate_entities,
):
    # Act
    result = getattr(unit_of_work.query(), expected_entity.__tablename__)().fetch_one()
    # Assert
    assert_that(
        result,
        equal_to(expected_entity)
    )
