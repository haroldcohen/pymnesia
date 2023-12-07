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
    "expected_entities",
    [
        ([
             InMemoryOrder(
                 id=uuid4(),
                 invoice_id=uuid4(),
                 proforma_id=uuid4(),
             ),
         ]),
        ([
             InMemoryOrder(
                 id=uuid4(),
                 invoice_id=uuid4(),
                 proforma_id=uuid4(),
             ),
             InMemoryOrder(
                 id=uuid4(),
                 invoice_id=uuid4(),
                 proforma_id=uuid4(),
             ),
         ]),
    ],
    indirect=True,
)
def test_query_orders_should_return_all_orders_with_a_loaded_invoice(
        unit_of_work,
        transaction,
        expected_entities,
        populate_entities,
):
    for entity in expected_entities:
        invoice = InMemoryInvoice(
            id=entity.invoice_id,
            order_id=entity.id
        )
        proforma = InMemoryProforma(
            id=entity.proforma_id,
            invoice_id=entity.invoice_id,
            order_id=entity.id
        )
        unit_of_work.save_entity(entity=invoice)
        unit_of_work.save_entity(entity=proforma)
        transaction.commit()
        entity.invoice = invoice
        entity.proforma = proforma
    # Act
    result = getattr(unit_of_work.query(), expected_entities[0].__tablename__)().fetch()
    # Assert
    assert_that(
        result,
        equal_to(expected_entities)
    )
