"""Provides with unit tests to validate the query with a custom filter function.
"""
from typing import Iterable, Union
from uuid import uuid4

import pytest
from hamcrest import assert_that, equal_to

from pymnesia.composition import runner
from pymnesia.query.query import Query
from tests.common_utils.entities.product import InMemoryProduct
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.unit_of_work.expected import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.populate import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.misc import *


@pytest.mark.parametrize(
    "entities, expected_entity, populate_expected_last",
    [
        (
                [InMemoryProduct(id=uuid4())], InMemoryProduct(id=uuid4(), name="banana"), True
        ),
    ],
    indirect=True,
)
def test_query_and_fetch_one_with_a_custom_filter_func_should_return_a_single_entity(
        unit_of_work,
        transaction,
        entities,
        expected_entity,
        populate_entities,
        populate_expected_last,
):
    def banana_func(entities_: Iterable, field: str, value: Union[str, int]) -> filter:
        return filter(lambda e: getattr(e, field) == value, entities_)

    partial_banana_func = runner(
        banana_func,
        field="name",
        value="banana",
    )

    # Act
    base_query: Query = getattr(unit_of_work.query(), expected_entity.__tablename__)()
    result = base_query.where_with_composition([partial_banana_func]).fetch_one()
    # Assert
    assert_that(
        result,
        equal_to(expected_entity)
    )