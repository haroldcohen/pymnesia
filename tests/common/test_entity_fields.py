"""Provides with unit tests to validate the entity field feature.
"""
from dataclasses import is_dataclass
from uuid import UUID

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.helpers.make import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.registry import *


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf",
    [
        ("InMemoryInvoice", "invoices", {
            "id": {"type": UUID, "make_field": False},
            "amount": {"type": float, "make_field": False},
            "vat_rate": {"type": float, "make_field": True, "field": {"default": 5.5}},
        }),
        ("InMemoryQuote", "quotes", {
            "id": {"type": UUID, "make_field": False},
            "price": {"type": float, "make_field": True, "field": {"default": 0}},
        })
    ],
    indirect=True
)
def test_declare_an_invoice_entity_with_fields_should_return_a_entity_dataclass_with_matching_attributes(
        entity_class_name,
        table_name,
        fields_conf,
        expected_entity_attributes,
        expected_dataclass_fields,
        entity_class,
        extracted_entity_class_fields,
        registry,
):
    # Assert
    assert_that(
        is_dataclass(entity_class),
        equal_to(True)
    )
    assert_that(
        entity_class.__annotations__,
        equal_to(expected_entity_attributes)
    )
    assert_that(
        extracted_entity_class_fields,
        equal_to(expected_dataclass_fields)
    )
