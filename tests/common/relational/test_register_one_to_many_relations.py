"""Provides with unit tests to validate 'one to one' relationships feature.
"""
from uuid import UUID

from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.registry import *
from pymnesia.core.entities.registry import DEFAULT_E_CLASSES_REGISTRY
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
                    class_name="OrderLine",
                    fields_conf={"id": UUID},
                    relation_type="many_to_one",
                )
            ]
        ),
        # Using relation api
        generate_entity_cls_params(
            class_name="Invoice",
            fields_conf={"id": UUID},
            rel_entity_classes_params=[
                generate_rel_entity_cls_params(
                    class_name="InvoiceLine",
                    fields_conf={"id": UUID},
                    relation_type="many_to_one",
                    owner_rel_api=Relation(reverse="invoice_"),
                )
            ]
        ),
    ],
    indirect=True,
)
def test_declarative_register_entity_with_one_to_many_relations_should_update_the_registry_with_matching_relations(
        entity_cls_params,
        fields_conf,
        entity_cls,
        rel_entity_classes,
        unregister_entity_classes,
        owned_relations,
        unit_of_work,
):
    related_entity_class_params = entity_cls_params.rel_entity_classes_params[0]
    # Assert
    validate_entity_cls(
        entity_cls_resolver=entity_cls,
        fields_conf=entity_cls_params.fields_conf,
        owned_relations=[related_entity_class_params.table_name],
        registry=DEFAULT_E_CLASSES_REGISTRY,
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
            registry=DEFAULT_E_CLASSES_REGISTRY,
        )
        assert_that(
            getattr(unit_of_work, rel_entity_cls_params.table_name),
            equal_to({})
        )
