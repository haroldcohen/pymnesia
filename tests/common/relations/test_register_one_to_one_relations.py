"""Provides with unit tests to validate 'one to one' relationships feature.
"""
from dataclasses import is_dataclass
from uuid import UUID, uuid4

from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.registry import *
from tests.common_utils.helpers.make import make_entity_class
from pymnesia.entities.base import DeclarativeBase
from pymnesia.entities.registry import registry
from pymnesia.entities.relations import Relation


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf, instance_values",
    [
        ("InMemoryInvoice", "invoices", {
            "id": UUID,
        }, {"id": uuid4()}),
    ],
    indirect=True,
)
def test_register_orders_with_a_one_to_one_relation_should_update_the_registry_with_a_matching_relation(
        entity_class_name,
        table_name,
        fields_conf,
        entity_class,
        expected_entity_attributes,
        instance_values,
        expected_entity_instance,
        unit_of_work,
        unregister_entity_class,
):
    # Arrange
    expected_related_entity_attributes = {
        **expected_entity_attributes,
    }
    order_id = uuid4()
    invoice_id = uuid4()

    # Act
    class InMemoryOrder(DeclarativeBase):
        __tablename__ = "orders"

        id: UUID

        invoice: entity_class

    expected_related_entity_attributes["order"] = InMemoryOrder
    expected_order_entity_attributes = {
        "id": UUID,
        "invoice_id": UUID,
        "invoice": entity_class,
    }

    # Assert
    assert_that(
        entity_class.__annotations__,
        equal_to(expected_related_entity_attributes)
    )
    assert_that(
        InMemoryOrder.__annotations__,
        equal_to(expected_order_entity_attributes)
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
        InMemoryOrder(id=order_id, invoice_id=invoice_id),
        equal_to(InMemoryOrder(id=order_id, invoice_id=invoice_id))
    )
    # Cleanup
    registry.unregister(InMemoryOrder)


@pytest.fixture()
def reverse(request):
    return request.param


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf, instance_values, reverse",
    [
        ("Invoice", "invoices", {
            "id": UUID,
        }, {"id": uuid4()}, "order"),
        ("Invoice", "invoices", {
            "id": UUID,
        }, {"id": uuid4()}, "order_test_2"),
    ],
    indirect=True,
)
def test_register_orders_with_a_one_to_one_relation_field_should_update_the_registry_with_a_matching_relation(
        entity_class_name,
        table_name,
        fields_conf,
        entity_class,
        instance_values,
        expected_entity_instance,
        expected_entity_attributes,
        unit_of_work,
        unregister_entity_class,
        reverse,
):
    # Arrange
    expected_related_entity_attributes = {
        **expected_entity_attributes,
    }
    order_id = uuid4()
    invoice_id = uuid4()

    # Act
    class InMemoryOrder(DeclarativeBase):
        __tablename__ = "orders"

        id: UUID

        invoice: entity_class = Relation(reverse=reverse)

    expected_related_entity_attributes[reverse] = InMemoryOrder
    expected_order_entity_attributes = {
        "id": UUID,
        "invoice_id": UUID,
        "invoice": entity_class,
    }

    # Assert
    assert_that(
        entity_class.__annotations__,
        equal_to(expected_related_entity_attributes)
    )
    assert_that(
        InMemoryOrder.__annotations__,
        equal_to(expected_order_entity_attributes)
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
        InMemoryOrder(id=order_id, invoice_id=invoice_id),
        equal_to(InMemoryOrder(id=order_id, invoice_id=invoice_id))
    )
    # Cleanup
    registry.unregister(InMemoryOrder)


def test_register_entity_with_one_to_one_relations_should_update_the_registry_with_matching_relations():
    """Tests whether multiple 'one to one' relationships can be declared.
    """
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
