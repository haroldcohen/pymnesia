"""Provides with unit test to validate the query feature for entities that have relations.
"""
from uuid import uuid4, UUID

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.entities.order import InMemoryOrder
from tests.common_utils.entities.invoice import InMemoryInvoice
from tests.common_utils.entities.product import InMemoryProduct
from tests.common_utils.entities.product_spec import InMemoryProductSpec
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.unit_of_work.expected import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.populate import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.misc import *


@pytest.mark.parametrize(
    "expected_entity",
    [
        (InMemoryOrder(
            id=uuid4(),
            invoice_id=UUID("4e5c4d8e-6f2a-4cb9-bd9f-56631f544967")
        )),
        (InMemoryOrder(
            id=uuid4(),
            invoice_id=UUID("69f08c92-0641-41d4-923a-47d5276bd3dc"),
        )),
    ],
    indirect=True,
)
def test_query_orders_should_return_the_first_order_with_a_loaded_invoice(
        unit_of_work,
        transaction,
        expected_entity,
        populate_entities,
):
    unit_of_work.save_entity(entity=InMemoryInvoice(id=expected_entity.invoice_id, order_id=expected_entity.id))
    transaction.commit()
    expected_entity.invoice = InMemoryInvoice(id=expected_entity.invoice_id, order_id=expected_entity.id)
    # Act
    result = getattr(unit_of_work.query(), expected_entity.__tablename__)().fetch_one()
    # Assert
    assert_that(
        result,
        equal_to(expected_entity)
    )


@pytest.mark.parametrize(
    "expected_entity",
    [
        (InMemoryProduct(
            id=uuid4(),
            spec_id=UUID("69f08c92-0641-41d4-923a-47d5276bd3dc"),
        )),
    ],
    indirect=True,
)
def test_query_products_should_return_the_first_product_with_a_loaded_spec(
        unit_of_work,
        transaction,
        expected_entity,
        populate_entities,
):
    unit_of_work.save_entity(entity=InMemoryProductSpec(id=expected_entity.spec_id, product_id=expected_entity.id))
    transaction.commit()
    expected_entity.spec = InMemoryProductSpec(id=expected_entity.spec_id, product_id=expected_entity.id)
    # Act
    result = getattr(unit_of_work.query(), expected_entity.__tablename__)().fetch_one()
    # Assert
    assert_that(
        result,
        equal_to(expected_entity)
    )
