"""Provides with unit test to validate the query with where clause feature for entities that have relations.
"""
from uuid import uuid4, UUID

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.entities.order import InMemoryOrder
from tests.common_utils.entities.invoice import InMemoryInvoice
from tests.common_utils.entities.product import InMemoryProduct
from tests.common_utils.entities.proforma import InMemoryProforma
from tests.common_utils.entities.product_spec import InMemoryProductSpec
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.unit_of_work.expected import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.populate import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.misc import *


@pytest.mark.parametrize(
    "entities, expected_entity, where_clause, use_properties",
    [
        ([
             InMemoryOrder(
                 id=UUID("4e5c4d8e-6f2a-4cb9-bd9f-56631f544967"),
                 invoice_id=UUID("da17c172-c67e-4980-af11-1184d320a342"),
             ),
             InMemoryInvoice(
                id=UUID("69f08c92-0641-41d4-923a-47d5276bd3dc"),
                order_id=UUID("0f91e357-cd79-4a6a-b6ba-d077ebd58d26"),
             ),
         ],
         InMemoryOrder(id=UUID("0f91e357-cd79-4a6a-b6ba-d077ebd58d26")),
         {"invoice.id": UUID("69f08c92-0641-41d4-923a-47d5276bd3dc")},
         {"invoice_id": UUID("69f08c92-0641-41d4-923a-47d5276bd3dc")}),
        ([
             InMemoryOrder(
                 id=UUID("4e5c4d8e-6f2a-4cb9-bd9f-56631f544967"),
                 invoice_id=UUID("da17c172-c67e-4980-af11-1184d320a342"),
             ),
             InMemoryInvoice(
                 id=UUID("69f08c92-0641-41d4-923a-47d5276bd3dc"),
                 order_id=UUID("0f91e357-cd79-4a6a-b6ba-d077ebd58d26"),
                 total_with_vat=20,
             ),
         ],
         InMemoryOrder(id=UUID("0f91e357-cd79-4a6a-b6ba-d077ebd58d26")),
         {"invoice.total_with_vat": 20},
         {"invoice_id": UUID("69f08c92-0641-41d4-923a-47d5276bd3dc")}),
        ([
             InMemoryOrder(id=uuid4()),
             InMemoryProforma(
                 id=UUID("b45cbdcb-8a96-4ce1-8518-df8d12a1d4be"),
                 total_with_vat=32,
             ),
             InMemoryInvoice(
                 id=uuid4(),
                 number="2023-00001",
             ),
             InMemoryInvoice(
                 id=UUID("69f08c92-0641-41d4-923a-47d5276bd3dc"),
                 order_id=UUID("0f91e357-cd79-4a6a-b6ba-d077ebd58d26"),
                 proforma_id=UUID("b45cbdcb-8a96-4ce1-8518-df8d12a1d4be"),
                 proforma=InMemoryProforma(
                     id=UUID("b45cbdcb-8a96-4ce1-8518-df8d12a1d4be"),
                     total_with_vat=32,
                 ),
                 number="2023-00001",
             ),
         ],
         InMemoryOrder(id=UUID("0f91e357-cd79-4a6a-b6ba-d077ebd58d26")),
         {"invoice.proforma.total_with_vat::gt": 30, "invoice.number::match": r'^2023-.*$'},
         {"invoice_id": UUID("69f08c92-0641-41d4-923a-47d5276bd3dc")}),
    ],
    indirect=True,
)
def test_query_orders_with_a_where_clause_should_return_the_first_order_with_a_loaded_invoice(
        time_ns,
        mocked_time_ns,
        unit_of_work,
        transaction,
        entities,
        where_clause,
        use_properties,
        expected_unit_of_work_memento,
        expected_entity,
        populate_entities,
):
    expected_entity.invoice = entities[-1]
    # Act
    base_query = getattr(unit_of_work.query(), expected_entity.__tablename__)()
    result = base_query.where(where_clause).fetch_one()
    # Assert
    assert_that(
        result,
        equal_to(expected_entity)
    )


@pytest.mark.parametrize(
    "entities, expected_entity, where_clause, use_properties",
    [
        ([
             InMemoryProduct(
                 id=UUID("4e5c4d8e-6f2a-4cb9-bd9f-56631f544967"),
                 spec_id=UUID("da17c172-c67e-4980-af11-1184d320a342"),
             ),
             InMemoryProductSpec(
                id=UUID("69f08c92-0641-41d4-923a-47d5276bd3dc"),
                product_id=UUID("0f91e357-cd79-4a6a-b6ba-d077ebd58d26"),
             ),
         ],
         InMemoryProduct(id=UUID("0f91e357-cd79-4a6a-b6ba-d077ebd58d26")),
         {"spec_id": UUID("69f08c92-0641-41d4-923a-47d5276bd3dc")},
         {"spec_id": UUID("69f08c92-0641-41d4-923a-47d5276bd3dc")}),
    ],
    indirect=True,
)
def test_query_products_with_a_where_clause_should_return_the_first_product_with_a_loaded_spec(
        time_ns,
        mocked_time_ns,
        unit_of_work,
        transaction,
        entities,
        where_clause,
        use_properties,
        expected_unit_of_work_memento,
        expected_entity,
        populate_entities,
):
    expected_entity.spec = entities[-1]
    # Act
    base_query = getattr(unit_of_work.query(), expected_entity.__tablename__)()
    result = base_query.where(where_clause).fetch_one()
    # Assert
    assert_that(
        result,
        equal_to(expected_entity)
    )
