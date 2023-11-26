"""Provides with unit tests to validate 'one to one' relationships feature.
"""
from uuid import UUID, uuid4

from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.registry import *
from pymnesia.entities.relations import Relation
from tests.common_utils.helpers.misc import generate_entity_cls_params
from tests.common_utils.helpers.relations.misc import generate_rel_entity_cls_params
from tests.common_utils.helpers.validate import validate_entity_cls


@pytest.mark.parametrize(
    "entity_cls_params",
    [
        generate_entity_cls_params(
            class_name="Order",
            fields_conf={"id": UUID},
            rel_entity_classes_params=[
                generate_rel_entity_cls_params(
                    class_name="OrderCustomization",
                    fields_conf={"id": UUID},
                ),
                # Using relation api
                generate_rel_entity_cls_params(
                    class_name="PackagingOption",
                    fields_conf={"id": UUID},
                    owner_rel_api=Relation(reverse="order_entity")
                )
            ]
        )
    ],
    indirect=True,
)
def test_register_entity_with_a_one_to_one_relation_should_update_the_registry_with_a_matching_relation(
        entity_cls_params,
        fields_conf,
        entity_cls,
        rel_entity_classes,
        unregister_entity_classes,
        owned_relations,
):
    # WARNING !!!
    # Need to check: non nullable relation, instance from expected instance, dataclass
    # Assert
    validate_entity_cls(
        entity_cls_resolver=entity_cls,
        fields_conf=entity_cls_params.fields_conf,
        owned_relations=owned_relations,
    )
    for rel_entity_cls_params in entity_cls_params.rel_entity_classes_params:
        validate_entity_cls(
            entity_cls_resolver=rel_entity_cls_params.cls_resolver,
            fields_conf=rel_entity_cls_params.fields_conf,
            owned_relations=[]
        )
