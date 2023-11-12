"""Provides with unit tests to validate 'one to one' relationships feature.
"""
from uuid import UUID, uuid4

from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.registry import *
from tests.common_utils.helpers.make import make_entity_class
from pymnesia.entities.base import DeclarativeBase
from pymnesia.entities.registry import registry
from pymnesia.entities.relations import Relation
from pymnesia.api.entities import relation
from tests.common_utils.helpers.validate import validate_entity_cls


@pytest.fixture()
def reverse(request):
    return request.param


@pytest.fixture()
def use_relation_api(request):
    return request.param


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf, instance_values, use_relation_api",
    [
        ("Invoice", "invoices", {
            "id": UUID,
        }, {"id": uuid4()}, True),
        ("Invoice", "invoices", {
            "id": UUID,
        }, {"id": uuid4()}, False),
    ],
    indirect=True,
)
def test_register_entity_with_a_one_to_one_relation_should_update_the_registry_with_a_matching_relation(
        entity_class_name,
        table_name,
        fields_conf,
        entity_class,
        instance_values,
        expected_entity_attributes,
        unit_of_work,
        unregister_entity_class,
        use_relation_api,
):
    # Act
    class InMemoryOrder(DeclarativeBase):
        __tablename__ = "orders"

        id: UUID

        if use_relation_api:
            invoice: entity_class = relation(reverse="order")
        else:
            invoice: entity_class

    in_memory_order_fields_conf = {
        "id": UUID,
    }

    if use_relation_api:
        in_memory_order_fields_conf["invoice"] = (entity_class, relation(reverse="order"))
    else:
        in_memory_order_fields_conf["invoice"] = entity_class

    # noinspection PyTypeChecker
    fields_conf["order"] = (InMemoryOrder, Relation(reverse="invoice", is_owner=False))

    # Assert
    # noinspection PyTypeChecker
    validate_entity_cls(
        entity_cls_resolver=InMemoryOrder,
        fields_conf=in_memory_order_fields_conf,
        owned_relations=["invoice"],
    )
    validate_entity_cls(
        entity_cls_resolver=entity_class,
        fields_conf=fields_conf,
        owned_relations=[]
    )
    try:
        order_id = uuid4()
        invoice_id = uuid4()
        instance_values["order"] = order_id
        instance_values["order_id"] = order_id
        InMemoryOrder(id=order_id, invoice_id=invoice_id)
        entity_class(**instance_values)
    except TypeError:
        assert False
    # Cleanup
    registry.unregister(InMemoryOrder)


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf, instance_values, reverse",
    [
        ("Invoice", "invoices", {
            "id": UUID,
        }, {"id": uuid4()}, "order_test"),
        ("Invoice", "invoices", {
            "id": UUID,
        }, {"id": uuid4()}, "order_test_2"),
    ],
    indirect=True,
)
def test_register_orders_with_a_one_to_one_non_nullable_relation_should_update_the_registry_with_a_matching_relation(
        entity_class_name,
        table_name,
        fields_conf,
        entity_class,
        instance_values,
        expected_entity_attributes,
        unit_of_work,
        unregister_entity_class,
        reverse,
):
    # Act
    relation_field = relation(reverse=reverse, is_nullable=False)

    class InMemoryOrder(DeclarativeBase):
        __tablename__ = "orders"

        id: UUID

        invoice: entity_class = relation_field

    in_memory_order_fields_conf = {
        "id": UUID,
        "invoice": (entity_class, relation_field)
    }
    # Assert
    # noinspection PyTypeChecker
    validate_entity_cls(
        entity_cls_resolver=InMemoryOrder,
        fields_conf=in_memory_order_fields_conf,
        owned_relations=["invoice"],
    )
    # noinspection PyTypeChecker
    fields_conf[reverse] = (InMemoryOrder, Relation(reverse="invoice", is_owner=False))
    validate_entity_cls(
        entity_cls_resolver=entity_class,
        fields_conf=fields_conf,
        owned_relations=[],
    )
    try:
        order_id = uuid4()
        invoice_id = uuid4()
        instance_values[reverse] = order_id
        instance_values[reverse + "_id"] = order_id
        InMemoryOrder(id=order_id, invoice_id=invoice_id)
        entity_class(**instance_values)
    except TypeError:
        assert False
    # Cleanup
    registry.unregister(InMemoryOrder)


def test_register_entity_with_one_to_one_relations_should_update_the_registry_with_matching_relations():
    """Tests whether multiple 'one to one' relationships can be declared.
    """
    # Arrange
    related_entities_cls_info = {
        "InMemoryOrderCustomization": {
            "table_name": "customizations",
            "single_form": "customization",
            "fields_conf": {"id": UUID},
            "cls_resolver": None,
        },
        "InMemoryPackagingOption": {
            "table_name": "packaging_options",
            "single_form": "packaging_option",
            "fields_conf": {"id": UUID},
            "cls_resolver": None,
        },
    }
    order_customization_class = make_entity_class(
        name="InMemoryOrderCustomization",
        table_name="customizations",
        fields_conf=related_entities_cls_info["InMemoryOrderCustomization"]["fields_conf"],
    )
    related_entities_cls_info["InMemoryOrderCustomization"]["cls_resolver"] = order_customization_class
    order_packaging_option_class = make_entity_class(
        name="InMemoryPackagingOption",
        table_name="packaging_options",
        fields_conf=related_entities_cls_info["InMemoryPackagingOption"]["fields_conf"]
    )
    related_entities_cls_info["InMemoryPackagingOption"]["cls_resolver"] = order_packaging_option_class
    in_memory_order_line_fields_conf = {"id": UUID}

    for rel_entity_cls_name, rel_entity_cls_info in related_entities_cls_info.items():
        entity_cls_resolver = rel_entity_cls_info["cls_resolver"]
        in_memory_order_line_fields_conf[rel_entity_cls_info["single_form"]] = (
            entity_cls_resolver,
            relation(reverse="order_line")
        )

    # Act
    in_memory_order_line_class = make_entity_class(
        name="InMemoryOrderLine",
        table_name="order_lines",
        fields_conf=in_memory_order_line_fields_conf,
    )

    # Assert
    for rel_entity_cls_name, rel_entity_cls_info in related_entities_cls_info.items():
        entity_cls_resolver = rel_entity_cls_info["cls_resolver"]
        rel_entity_fields_conf = rel_entity_cls_info["fields_conf"]
        in_memory_order_line_fields_conf[rel_entity_cls_info["single_form"]] = (
            entity_cls_resolver,
            relation(reverse="order_line")
        )
        rel_entity_cls_info["fields_conf"]["order_line"] = (
            in_memory_order_line_class,
            Relation(reverse=rel_entity_cls_info["single_form"], is_owner=False)
        )
        validate_entity_cls(
            entity_cls_resolver=entity_cls_resolver,
            fields_conf=rel_entity_fields_conf,
            owned_relations=[],
        )
    validate_entity_cls(
        entity_cls_resolver=in_memory_order_line_class,
        fields_conf=in_memory_order_line_fields_conf,
        owned_relations=["customization", "packaging_option"],
    )
    # Cleanup
    registry.unregister(in_memory_order_line_class)
    for rel_entity_cls_name, rel_entity_cls_info in related_entities_cls_info.items():
        registry.unregister(rel_entity_cls_info["cls_resolver"])
