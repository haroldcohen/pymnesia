"""Provides with unit tests to validate the related entities feature.
"""
from dataclasses import is_dataclass
from uuid import UUID, uuid4

from hamcrest import assert_that, equal_to

from pymnesia.entities.base import DeclarativeBase
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.registry import *
from pymnesia.entities.registry import registry
from tests.common_utils.helpers.make import make_entity_class


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf",
    [
        ("InMemoryInvoice", "invoices", {
            "id": UUID,
        }),
    ],
    indirect=True,
)
def test_register_orders_with_a_one_to_one_relationship_should_update_the_registry_with_a_matching_relationship(
        entity_class_name,
        table_name,
        fields_conf,
        entity_class,
        expected_entity_attributes,
        unit_of_work,
        unregister_entity_class,
):
    # Arrange
    expected_related_entity_attributes = {
        **expected_entity_attributes,
    }

    # Act
    class InMemoryOrder(DeclarativeBase):
        __tablename__ = "orders"

        id: UUID

        invoice: entity_class

    expected_related_entity_attributes["order"] = InMemoryOrder

    # Assert
    assert_that(
        entity_class.__annotations__,
        equal_to(expected_related_entity_attributes)
    )
    # Cleanup
    registry.unregister(InMemoryOrder)


def test_register_entity_with_one_to_one_relationships_should_update_the_registry_with_a_matching_relationship():
    # Arrange
    order_customization_class = make_entity_class(
        name="InMemoryOrderCustomization",
        table_name="customizations",
        fields_conf={"id": UUID}
    )
    order_packaging_option_class = make_entity_class(
        name="InMemoryPackagingOption",
        table_name="order_packaging_options",
        fields_conf={"id": UUID}
    )
    entity_classes = {
        "customizations": order_customization_class,
        "order_packaging_options": order_packaging_option_class
    }
    expected_related_entities_attributes = {
        "customizations": {
            "id": UUID,
        },
        "order_packaging_options": {
            "id": UUID,
        }
    }

    # Act
    class InMemoryOrderLine(DeclarativeBase):
        __tablename__ = "order_lines"

        id: UUID

        customization: order_customization_class

        packaging_option: order_packaging_option_class

    for relation_name in entity_classes:
        expected_related_entities_attributes[relation_name]["order_line"] = InMemoryOrderLine

    # Assert
    for relation_name, expected_related_attributes in expected_related_entities_attributes.items():
        assert_that(
            entity_classes[relation_name].__annotations__,
            equal_to(expected_related_attributes)
        )
    # Cleanup
    registry.unregister(InMemoryOrderLine)
    for relation_entity_class in entity_classes.values():
        registry.unregister(relation_entity_class)
