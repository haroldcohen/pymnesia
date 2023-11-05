"""Provides with unit tests to validate 'one to one' relationships feature.
"""
from dataclasses import MISSING
from uuid import UUID, uuid4

from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.registry import *
from tests.common_utils.helpers import extract_entity_class_fields, extract_expected_dataclass_fields
from tests.common_utils.helpers.make import make_entity_class
from pymnesia.entities.base import DeclarativeBase
from pymnesia.entities.registry import registry
from pymnesia.entities.relations import Relation


@pytest.fixture()
def reverse(request):
    return request.param


@pytest.fixture()
def use_relation_api(request):
    return request.param


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf, instance_values, reverse, use_relation_api",
    [
        ("Invoice", "invoices", {
            "id": UUID,
        }, {"id": uuid4()}, "order_test", True),
        ("Invoice", "invoices", {
            "id": UUID,
        }, {"id": uuid4()}, "order_test_2", False),
    ],
    indirect=True,
)
def test_register_orders_with_a_one_to_one_relation_field_should_update_the_registry_with_a_matching_relation(
        entity_class_name,
        table_name,
        fields_conf,
        entity_class,
        instance_values,
        expected_entity_attributes,
        unit_of_work,
        unregister_entity_class,
        reverse,
        use_relation_api,
):
    # Arrange
    expected_related_entity_attributes = {
        **expected_entity_attributes,
    }
    order_id = uuid4()
    invoice_id = uuid4()
    if not use_relation_api:
        reverse = "order"

    # Act
    class InMemoryOrder(DeclarativeBase):
        __tablename__ = "orders"

        id: UUID

        if use_relation_api:
            invoice: entity_class = Relation(reverse=reverse)
        else:
            invoice: entity_class

    expected_related_entity_attributes["order_id"] = UUID
    expected_related_entity_attributes[reverse] = InMemoryOrder
    expected_order_entity_attributes = {
        "id": UUID,
        "invoice_id": UUID,
        "invoice": entity_class,
    }
    expected_related_entity_class_fields = extract_expected_dataclass_fields(fields_conf)
    expected_related_entity_class_fields.append({
        "name": "order_id",
        "type": UUID,
        "default": MISSING,
        "default_factory": MISSING,
    })
    expected_related_entity_class_fields.append({
        "name": reverse,
        "type": InMemoryOrder,
        "default": None,
        "default_factory": MISSING,
    })
    extracted_related_entity_class_fields = extract_entity_class_fields(entity_class)
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
        extracted_related_entity_class_fields,
        equal_to(expected_related_entity_class_fields)
    )
    assert_that(
        InMemoryOrder(id=order_id, invoice_id=invoice_id),
        equal_to(InMemoryOrder(id=order_id, invoice_id=invoice_id))
    )
    try:
        entity_class(**instance_values, order_id=order_id)
    except TypeError:
        assert False
    # Cleanup
    registry.unregister(InMemoryOrder)


def test_register_entity_with_one_to_one_relations_should_update_the_registry_with_matching_relations():
    """Tests whether multiple 'one to one' relationships can be declared.
    """
    # Arrange
    order_customization_fields_conf = {"id": UUID}
    order_customization_class = make_entity_class(
        name="InMemoryOrderCustomization",
        table_name="customizations",
        fields_conf=order_customization_fields_conf
    )
    order_packaging_option_fields_conf = {"id": UUID}
    order_packaging_option_class = make_entity_class(
        name="InMemoryPackagingOption",
        table_name="order_packaging_options",
        fields_conf=order_packaging_option_fields_conf
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
    expected_related_entities_fields = {
        "customizations": extract_expected_dataclass_fields(order_customization_fields_conf),
        "order_packaging_options": extract_expected_dataclass_fields(order_packaging_option_fields_conf),
    }

    # Act
    class InMemoryOrderLine(DeclarativeBase):
        __tablename__ = "order_lines"

        id: UUID

        customization: order_customization_class

        packaging_option: order_packaging_option_class

    extracted_related_entities_fields = {
        "customizations": extract_entity_class_fields(order_customization_class),
        "order_packaging_options": extract_entity_class_fields(order_packaging_option_class),
    }

    for relation_name in entity_classes:
        expected_related_entities_attributes[relation_name]["order_line"] = InMemoryOrderLine
        expected_related_entities_attributes[relation_name]["order_line_id"] = UUID
        expected_related_entities_fields[relation_name].append({
            "name": "order_id",
            "type": UUID,
            "default": MISSING,
            "default_factory": MISSING,
        })
        expected_related_entities_fields[relation_name].append({
            "name": reverse,
            "type": InMemoryOrderLine,
            "default": None,
            "default_factory": MISSING,
        })

    # Assert
    for relation_name, expected_related_attributes in expected_related_entities_attributes.items():
        assert_that(
            entity_classes[relation_name].__annotations__,
            equal_to(expected_related_attributes)
        )
        assert_that(
            extracted_related_entities_fields[relation_name],
            equal_to(extracted_related_entities_fields[relation_name])
        )
    # Cleanup
    registry.unregister(InMemoryOrderLine)
    for relation_entity_class in entity_classes.values():
        registry.unregister(relation_entity_class)
