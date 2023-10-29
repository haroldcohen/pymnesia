"""Provides with unit tests to validate the entity field feature.
"""
import datetime
from dataclasses import is_dataclass
from uuid import UUID, uuid4

import pytest
from freezegun import freeze_time
from hamcrest import assert_that, equal_to

from pymnesia.entities.field import Field
from tests.common_utils.helpers.make import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.registry import *

# Somehow freeze has issues being passed in a feature or used as a decorator alongside fixtures parameters.
freezer = freeze_time(datetime.datetime.now())
freezer.start()


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf, instance_values",
    [
        ("InMemoryInvoice", "invoices", {
            "id": UUID,
            "amount": float,
            "vat_rate": (float, Field(default=5.5)),
        }, {"id": uuid4(), "amount": 2.3}),
        ("InMemoryQuote", "quotes", {
            "id": UUID,
            "price": (float, Field(default=0)),
        }, {"id": uuid4()}),
        ("InMemoryProductCategory", "product_categories", {
            "id": UUID,
            "created_at": (datetime.datetime, Field(default_factory=datetime.datetime.now)),
        }, {"id": uuid4()}),
    ],
    indirect=True
)
def test_declare_an_entity_with_fields_should_return_a_entity_dataclass_with_matching_attributes(
        entity_class_name,
        table_name,
        fields_conf,
        expected_entity_attributes,
        expected_dataclass_fields,
        entity_class,
        extracted_entity_class_fields,
        registry,
        instance_values,
        expected_entity_instance,
):
    # Assert
    assert_that(
        is_dataclass(entity_class),
        equal_to(True)
    )
    assert_that(
        entity_class(**instance_values),
        equal_to(expected_entity_instance)
    )
    assert_that(
        entity_class.__annotations__,
        equal_to(expected_entity_attributes)
    )
    assert_that(
        extracted_entity_class_fields,
        equal_to(expected_dataclass_fields)
    )


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf",
    [
        ("InMemoryProductCategory", "product_categories", {
            "id": UUID,
            "config": (str, Field(default="config")),
        }),
    ],
    indirect=True
)
def test_declare_an_entity_with_a_field_named_config_should_raise_ConfigIsAReservedKeyWorkException(
        entity_class_name,
        table_name,
        fields_conf,
        registry,
):
    # Act & Assert
    make_entity_class(
        class_name=entity_class_name,
        table_name=table_name,
        fields=fields_conf,
        registry=registry
    )
