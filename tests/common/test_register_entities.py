"""Provides with unit tests to validate entities registry related features.
"""
from dataclasses import is_dataclass
from uuid import UUID, uuid4

from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.registry import *
from pymnesia.entities.field import Field
from pymnesia.entities.entity import Entity
from tests.common_utils.helpers.validate import validate_entity_cls


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf, instance_values",
    [
        ("InMemoryInvoice", "invoices", {
            "id": UUID,
            "amount": float,
            "vat_rate": (float, Field(default=5.5)),
        }, {"id": uuid4(), "amount": 2.3}),
        ("InMemoryOrderLine", "order_lines", {
            "id": UUID,
            "customization": (dict, Field(default_factory=lambda: {})),
        }, {"id": uuid4()}),
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
        unregister_entity_class,
):
    entity_instance = entity_class(**instance_values)
    # Assert
    assert_that(
        issubclass(entity_class, Entity),
        equal_to(True)
    )
    assert_that(
        entity_instance,
        equal_to(expected_entity_instance)
    )
    assert_that(
        is_dataclass(entity_instance),
        equal_to(True)
    )
    validate_entity_cls(
        entity_cls_resolver=entity_class,
        fields_conf=fields_conf,
        owned_relations=[]
    )
    assert_that(
        getattr(unit_of_work, table_name),
        equal_to({})
    )
