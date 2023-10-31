"""Provides with unit tests to validate entities registry related features.
"""
from dataclasses import is_dataclass
from uuid import UUID, uuid4

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from pymnesia.entities.config import EntityConfig
from pymnesia.entities.field import Field
from pymnesia.entities.registry import registry


# Temporarily skipping tests since the registry is not cleaned up after each test and disturbs the query test suite
@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf, instance_values",
    [
        # ("InMemoryInvoice", "invoices", {
        #     "id": UUID,
        #     "amount": float,
        #     "vat_rate": (float, Field(default=5.5)),
        # }, {"id": uuid4(), "amount": 2.3}),
    ],
    indirect=True,
)
def test_register_entity_should_update_the_registry_with_a_prepared_entity_class(
        entity_class_name,
        table_name,
        fields_conf,
        entity_class,
        unit_of_work,
        instance_values,
        expected_entity_instance,
        expected_entity_attributes,
        expected_dataclass_fields,
        extracted_entity_class_fields,
):
    expected_config = EntityConfig(
        table_name=table_name,
    )
    # Assert
    assert_that(
        registry.find(entity_class),
        equal_to(expected_config)
    )
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
    assert_that(
        getattr(unit_of_work, table_name),
        equal_to({})
    )

