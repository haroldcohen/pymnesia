"""Provides with unit tests to validate the query with where clause feature.
"""
from uuid import uuid4

import pytest
from hamcrest import assert_that, equal_to

from pymnesia.query.query import Query
from tests.common_utils.entities.order import InMemoryOrder
from tests.common_utils.entities.product import InMemoryProduct
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.unit_of_work.expected import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.populate import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.misc import *


@pytest.mark.parametrize(
    "entities, where_clause, expected_entities",
    [
        ([InMemoryOrder(id=uuid4())], {"id": uuid4()}, [InMemoryOrder(id=uuid4())]),
        ([InMemoryOrder(id=uuid4())], {"total_amount": 50}, [InMemoryOrder(id=uuid4()), InMemoryOrder(id=uuid4())]),
    ],
    indirect=True,
)
def test_query_with_a_where_clause_should_return_a_number_of_filtered_entities(
        time_ns,
        mocked_time_ns,
        unit_of_work,
        transaction,
        expected_unit_of_work_memento,
        entities,
        where_clause,
        use_properties,
        expected_entities,
        populate_entities,
):
    # Act
    base_query: Query = getattr(unit_of_work.query(), expected_entities[0].config.table_name)()
    result = base_query.where(where_clause).fetch()
    # Assert
    assert_that(
        result,
        equal_to(expected_entities)
    )


@pytest.mark.parametrize(
    "entities, where_clause, use_properties, expected_entities",
    [
        ([
             InMemoryOrder(id=uuid4(), total_amount=50)
         ], {"total_amount::not": 50}, {}, [InMemoryOrder(id=uuid4(), total_amount=60)]),
        ([
             InMemoryOrder(id=uuid4(), total_amount=50)
         ], {"total_amount::gt": 51}, {}, [InMemoryOrder(id=uuid4(), total_amount=60)]),
        ([
             InMemoryOrder(id=uuid4(), total_amount=80)
         ], {"total_amount::lt": 80}, {}, [InMemoryOrder(id=uuid4(), total_amount=60)]),
        ([
             InMemoryOrder(id=uuid4(), total_amount=79)
         ], {"total_amount::gte": 80}, {}, [
             InMemoryOrder(id=uuid4(), total_amount=80),
             InMemoryOrder(id=uuid4(), total_amount=82)
         ]),
        ([
             InMemoryOrder(id=uuid4(), total_amount=81)
         ], {"total_amount::lte": 80}, {}, [
            InMemoryOrder(id=uuid4(), total_amount=80),
            InMemoryOrder(id=uuid4(), total_amount=60)
        ]),
        ([
             InMemoryOrder(id=uuid4(), total_amount=81),
             InMemoryOrder(id=uuid4(), total_amount=60)
         ], {"total_amount::lt": 80, "vat_not_included_amount": 60}, {}, [
            InMemoryOrder(id=uuid4(), total_amount=79, vat_not_included_amount=60),
        ]),
        ([
             InMemoryProduct(id=uuid4()),
             InMemoryProduct(id=uuid4())
         ], {"name::match": r'^Framework laptop \d+ inches$'}, {}, [
             InMemoryProduct(id=uuid4(), name="Framework laptop 16 inches"),
             InMemoryProduct(id=uuid4(), name="Framework laptop 13 inches"),
         ]),
    ],
    indirect=True,
)
def test_query_with_a_where_clause_different_from_equal_should_return_a_number_of_filtered_entities(
        time_ns,
        mocked_time_ns,
        unit_of_work,
        transaction,
        expected_unit_of_work_memento,
        entities,
        where_clause,
        use_properties,
        expected_entities,
        populate_entities,
):
    # Act
    base_query: Query = getattr(unit_of_work.query(), expected_entities[0].config.table_name)()
    result = base_query.where(where_clause).fetch()
    # Assert
    assert_that(
        result,
        equal_to(expected_entities)
    )
