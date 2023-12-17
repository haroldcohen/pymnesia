"""Provides with unit tests to validate 'one to one' relationships feature.
"""
from uuid import UUID

from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.registry import *
from pymnesia.core.entities.registry import registry
from pymnesia.core.entities.relations import Relation
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.make.relations.generate import generate_rel_entity_cls_params
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
        ),
    ],
    indirect=True,
)
def test_register_entity_with_one_to_one_relations_should_update_the_registry_with_matching_relations(
        entity_cls_params,
        fields_conf,
        entity_cls,
        rel_entity_classes,
        unregister_entity_classes,
        owned_relations,
        unit_of_work,
):
    # WARNING !!!
    # Need to check: non nullable relation, instance from expected instance, dataclass
    # Assert
    validate_entity_cls(
        entity_cls_resolver=entity_cls,
        fields_conf=entity_cls_params.fields_conf,
        owned_relations=owned_relations,
        registry=registry,
    )
    assert_that(
        getattr(unit_of_work, entity_cls_params.table_name),
        equal_to({})
    )
    for rel_entity_cls_params in entity_cls_params.rel_entity_classes_params:
        validate_entity_cls(
            entity_cls_resolver=rel_entity_cls_params.cls_resolver,
            fields_conf=rel_entity_cls_params.fields_conf,
            owned_relations=[],
            registry=registry,
        )
        assert_that(
            getattr(unit_of_work, rel_entity_cls_params.table_name),
            equal_to({})
        )
