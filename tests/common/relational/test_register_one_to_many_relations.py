"""Provides with unit tests to validate 'one to one' relationships feature.
"""
from typing import List
from uuid import UUID, uuid4

from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.registry import *
from pymnesia.entities.base import DeclarativeBase
from pymnesia.entities.registry import registry
from pymnesia.entities.relations import Relation
from pymnesia.api.entities import relation
from tests.common_utils.helpers.validate import validate_entity_cls


@pytest.mark.parametrize(
    "entity_class_name, table_name, fields_conf, instance_values, use_relation_api",
    [
        ("OrderLine", "order_lines", {
            "id": UUID,
        }, {"id": uuid4()}, False),
        ("OrderLine", "order_lines", {
            "id": UUID,
        }, {"id": uuid4()}, True),
    ],
    indirect=True,
)
def test_register_entity_with_a_one_to_many_relation_should_update_the_registry_with_a_matching_relation(
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
    relation_field = None
    if use_relation_api:
        relation_field = relation(reverse="order")

    class Order(DeclarativeBase):
        __tablename__ = "orders"

        id: UUID

        if use_relation_api:
            order_lines: List[entity_class] = relation_field
        else:
            order_lines: List[entity_class]

    if use_relation_api:
        relation_field.relation_type = "one_to_many"
        # noinspection PyTypeChecker
        in_memory_order_fields_conf = {
            "id": UUID,
            "order_lines": (
                List[entity_class],
                relation_field
            )
        }
    else:
        in_memory_order_fields_conf = {"id": UUID, "order_lines": List[entity_class]}

    # noinspection PyTypeChecker
    fields_conf["order"] = (Order, Relation(reverse="order_lines", is_owner=False, relation_type="many_to_one"))

    # noinspection PyTypeChecker
    validate_entity_cls(
        entity_cls_resolver=Order,
        fields_conf=in_memory_order_fields_conf,
        owned_relations=["order_lines"],
    )
    # noinspection PyTypeChecker
    validate_entity_cls(
        entity_cls_resolver=entity_class,
        fields_conf=fields_conf,
        owned_relations=[],
    )

    # Cleanup
    registry.unregister(Order)
