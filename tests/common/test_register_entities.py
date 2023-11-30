"""Provides with unit tests to validate entities registry related features.
"""
from uuid import UUID

from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.registry import *
from pymnesia.entities.registry import registry
from pymnesia.entities.field import Field
from tests.common_utils.helpers.misc import generate_entity_cls_params
from tests.common_utils.helpers.validate import validate_entity_cls


@pytest.mark.parametrize(
    "entity_cls_params",
    [
        generate_entity_cls_params(
            class_name="Order",
            fields_conf={
                "id": UUID,
                "amount": float,
                "vat_rate": (float, Field(default=5.5)),
            },
            rel_entity_classes_params=[],
        ),
        generate_entity_cls_params(
            class_name="OrderLine",
            fields_conf={
                "id": UUID,
                "customization": (dict, Field(default_factory=lambda: {})),
            },
            rel_entity_classes_params=[],
        ),
    ],
    indirect=True,
)
def test_register_entity_should_update_the_registry_with_a_prepared_entity_class(
        entity_cls_params,
        fields_conf,
        entity_cls,
        unit_of_work,
        owned_relations,
        unregister_entity_classes,
):
    # WARNING !!!
    # Need to check: instance from expected instance, dataclass
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
