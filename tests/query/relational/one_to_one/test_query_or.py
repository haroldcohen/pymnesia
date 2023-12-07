"""Provides with unit tests to validate the query with a where and or clause feature for entities that have relations.
"""
from uuid import UUID, uuid4

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.entities.order import InMemoryOrder
from tests.common_utils.entities.invoice import InMemoryInvoice
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.unit_of_work.expected import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.populate import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.query.expressions import (
    where_clause,
    or_clauses,
)


@pytest.mark.parametrize(
    "entities, where_clause, or_clauses, expected_entities",
    [
        ([
             InMemoryOrder(
                 id=UUID("bc425a50-f0c9-4e27-91bc-e3ad16bb97cc"),
                 invoice_id=UUID("e54c93cb-470f-44f2-831b-bd2f36ce4547"),
             ),
             InMemoryInvoice(
                 id=UUID("e54c93cb-470f-44f2-831b-bd2f36ce4547"),
                 number="2026-00002",
                 order_id=uuid4(),
             ),
             InMemoryInvoice(
                 id=UUID("5f61bc32-a712-42a2-8e58-74a28fc643b9"),
                 order_id=UUID("99a8c211-c8a1-49dc-b3f3-d9999abd4212"),
                 total_with_vat=120,
                 number="2026-00001",
             ),
             InMemoryInvoice(
                 id=UUID("4c95eb4c-df59-4024-ad86-c3b16116ca52"),
                 order_id=UUID("d4c5c4ef-ac66-429e-afd0-af3fbed36177"),
                 total_with_vat=150,
                 number="2022-00001",
             ),
         ],
         {"total_amount": 60},
         [{"invoice.number::match": r'^2022-.*$'}],
         [
             InMemoryOrder(
                 id=UUID("99a8c211-c8a1-49dc-b3f3-d9999abd4212"),
                 total_amount=60,
                 invoice_id=UUID("5f61bc32-a712-42a2-8e58-74a28fc643b9"),
                 invoice=InMemoryInvoice(
                     id=UUID("5f61bc32-a712-42a2-8e58-74a28fc643b9"),
                     order_id=UUID("99a8c211-c8a1-49dc-b3f3-d9999abd4212"),
                     total_with_vat=120,
                     number="2026-00001",
                 )
             ),
             InMemoryOrder(
                 id=UUID("d4c5c4ef-ac66-429e-afd0-af3fbed36177"),
                 total_amount=70,
                 invoice_id=UUID("4c95eb4c-df59-4024-ad86-c3b16116ca52"),
                 invoice=InMemoryInvoice(
                     id=UUID("4c95eb4c-df59-4024-ad86-c3b16116ca52"),
                     order_id=UUID("d4c5c4ef-ac66-429e-afd0-af3fbed36177"),
                     total_with_vat=150,
                     number="2022-00001",
                 ),
             ),
         ]),
    ],
    indirect=True,
)
def test_query_and_fetch_with_a_where_or_clause_on_a_relation_should_return_a_number_of_filtered_entities(
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
