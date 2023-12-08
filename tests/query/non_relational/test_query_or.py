"""Provides with unit tests to validate the query with a where and or clause feature.
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
from tests.common_utils.fixtures.query.expressions import (
    direction,
    order_by_key,
    where_clause,
    or_clauses,
)


@pytest.mark.parametrize(
    "entities, where_clause, or_clauses, expected_entities",
    [
        ([InMemoryOrder(id=uuid4(), total_amount=50)],
         {"total_amount": 60},
         [{"total_amount": 70}],
         [InMemoryOrder(id=uuid4(), total_amount=60),
          InMemoryOrder(id=uuid4(), total_amount=70)]),
        ([InMemoryOrder(id=uuid4(), total_amount=50), InMemoryOrder(id=uuid4(), vat_not_included_amount=70)],
         {"total_amount": 60},
         [{"vat_not_included_amount": 70, "total_amount": 81}],
         [InMemoryOrder(id=uuid4(), total_amount=60),
          InMemoryOrder(id=uuid4(), total_amount=81, vat_not_included_amount=70)]),
        ([InMemoryOrder(id=uuid4(), total_amount=50)],
         {"total_amount": 60},
         [{"vat_not_included_amount": 70}, {"total_amount": 90}],
         [InMemoryOrder(id=uuid4(), total_amount=60),
          InMemoryOrder(id=uuid4(), vat_not_included_amount=70),
          InMemoryOrder(id=uuid4(), total_amount=90)]),
    ],
    indirect=True,
)
def test_query_and_fetch_with_a_where_or_clause_should_return_a_number_of_filtered_entities(
        unit_of_work,
        transaction,
        entities,
        where_clause,
        or_clauses,
        expected_entities,
        populate_entities,
):
    # Act
    base_query = getattr(unit_of_work.query(), expected_entities[0].__tablename__)().where(where_clause)
    for or_clause in or_clauses:
        base_query.or_(or_clause)
    result = base_query.fetch()
    # Assert
    assert_that(
        result,
        equal_to(expected_entities)
    )


@pytest.mark.parametrize(
    "entities, where_clause, or_clauses, expected_entities, direction, order_by_key",
    [
        ([InMemoryOrder(id=uuid4(), total_amount=50)],
         {"total_amount": 60},
         [{"total_amount": 70}],
         [InMemoryOrder(id=uuid4(), total_amount=60),
          InMemoryOrder(id=uuid4(), total_amount=70)], "desc", "total_amount"),
    ],
    indirect=True,
)
def test_query_and_fetch_with_a_where_or_clause_and_order_by_should_return_a_number_of_filtered_entities(
        unit_of_work,
        transaction,
        entities,
        where_clause,
        or_clauses,
        use_properties,
        expected_entities,
        populate_entities,
        direction,
        order_by_key,
):
    # Arrange
    sorted_entities = sorted(expected_entities, key=lambda e: getattr(e, order_by_key), reverse=direction == "desc")
    # Act
    base_query = getattr(unit_of_work.query(), expected_entities[0].__tablename__)().where(where_clause)
    for or_clause in or_clauses:
        base_query.or_(or_clause)
    base_query.order_by(direction, order_by_key)
    result = base_query.fetch()
    # Assert
    assert_that(
        result,
        equal_to(sorted_entities)
    )


@pytest.mark.parametrize(
    "entities, where_clause, or_clauses, expected_entity",
    [
        ([InMemoryOrder(id=uuid4(), total_amount=50)],
         {"total_amount": 60},
         [{"total_amount": 70}],
         InMemoryOrder(id=uuid4(), total_amount=70)),
    ],
    indirect=True,
)
def test_query_and_fetch_one_with_a_where_or_clause_should_return_one_filtered_entity(
        unit_of_work,
        transaction,
        entities,
        where_clause,
        or_clauses,
        expected_entity,
        populate_entities,
):
    # Act
    base_query = getattr(unit_of_work.query(), expected_entity.__tablename__)().where(where_clause)
    for or_clause in or_clauses:
        base_query.or_(or_clause)
    result = base_query.fetch_one()
    # Assert
    assert_that(
        result,
        equal_to(expected_entity)
    )
