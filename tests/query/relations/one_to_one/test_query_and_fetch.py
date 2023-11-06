"""Provides with unit test to validate the query and fetch feature for entities that have relations.
"""
from uuid import uuid4, UUID

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.entities.order import InMemoryOrder
from tests.common_utils.entities.invoice import InMemoryInvoice
from tests.common_utils.entities.proforma import InMemoryProforma
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.unit_of_work.expected import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.populate import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.misc import *


@pytest.mark.parametrize(
    "expected_entities, use_dedicated_properties",
    [
        ([
             InMemoryOrder(id=UUID("4e5c4d8e-6f2a-4cb9-bd9f-56631f544967")),
         ],
         [
             {"invoice_id": uuid4(), "proforma_id": uuid4()},
         ]),
        ([
             InMemoryOrder(id=uuid4()),
             InMemoryOrder(id=uuid4()),
         ],
         [
             {"invoice_id": uuid4(), "proforma_id": uuid4()},
             {"invoice_id": uuid4(), "proforma_id": uuid4()},
         ]),
    ],
    indirect=True,
)
def test_query_orders_should_return_all_orders_with_a_loaded_invoice(
        time_ns,
        mocked_time_ns,
        unit_of_work,
        transaction,
        use_dedicated_properties,
        expected_unit_of_work_memento,
        expected_entities,
        populate_entities,
):
    properties_idx = 0
    for entity in expected_entities:
        invoice = InMemoryInvoice(id=use_dedicated_properties[properties_idx]["invoice_id"], order_id=entity.id)
        proforma = InMemoryProforma(id=use_dedicated_properties[properties_idx]["proforma_id"], order_id=entity.id)
        unit_of_work.save_entity(entity=invoice)
        unit_of_work.save_entity(entity=proforma)
        transaction.commit()
        entity.invoice = invoice
        entity.proforma = proforma
        properties_idx += 1
    # # Act
    result = getattr(unit_of_work.query(), expected_entities[0].__tablename__)().fetch()
    # Assert
    assert_that(
        result,
        equal_to(expected_entities)
    )
