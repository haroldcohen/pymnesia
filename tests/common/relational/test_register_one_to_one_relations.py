"""Provides with unit tests to validate 'one to one' relationships feature.
"""
from uuid import UUID, uuid4

from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.registry import *
from tests.common_utils.helpers.make import make_entity_class
from pymnesia.entities.base import DeclarativeBase
from pymnesia.entities.registry import registry
from pymnesia.entities.relations import Relation
from pymnesia.api.entities import relation
from tests.common_utils.helpers.relations.misc import generate_rel_entity_cls_params
from tests.common_utils.helpers.relations.types import RelatedEntityClsParams
from tests.common_utils.helpers.validate import validate_entity_cls


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


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf, related_entity_classes_params",
    [
        (
                "InMemoryOrder", "orders",
                {"id": UUID},
                [
                    generate_rel_entity_cls_params(
                        class_name="InMemoryOrderCustomization",
                        fields_conf={"id": UUID},
                    ),
                    generate_rel_entity_cls_params(
                        class_name="InMemoryPackagingOption",
                        fields_conf={"id": UUID},
                    )
                ],
        )
    ],
    indirect=True,
)
def test_register_entity_with_one_to_one_relations_should_update_the_registry_with_matching_relations(
        entity_class_name,
        table_name,
        fields_conf,
        entity_class,
        related_entity_classes_params,
        related_entity_classes,
        unit_of_work,
        unregister_entity_classes,
):
    # Arrange
    owned_relations = [related_entity_class_params.single_form for related_entity_class_params in
                       related_entity_classes_params]
    # Assert
    validate_entity_cls(
        entity_cls_resolver=entity_class,
        fields_conf=fields_conf,
        owned_relations=owned_relations,
    )
    for rel_entity_cls_params in related_entity_classes_params:
        validate_entity_cls(
            entity_cls_resolver=rel_entity_cls_params.cls_resolver,
            fields_conf=rel_entity_cls_params.fields_conf,
            owned_relations=[]
        )



