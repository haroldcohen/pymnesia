"""Provides with unit tests to validate entities registry related features.
"""
from uuid import UUID, uuid4

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.registry import unregister_entity_classes
from pymnesia.entities.registry import registry
from pymnesia.entities.field import Field
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.validate import validate_entity_cls


@pytest.mark.parametrize(
    "entity_cls_params, use_properties",
    [
        (
                generate_entity_cls_params(
                    class_name="EntityWithFloatFields",
                    fields_conf={
                        "id": UUID,
                        "float_field": float,
                        "float_field_with_default": (float, Field(default=5.5)),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "float_field": 0.5, "float_field_with_default": 5.5}
        ),
        (
                generate_entity_cls_params(
                    class_name="EntityWithIntFields",
                    fields_conf={
                        "id": UUID,
                        "int_field": int,
                        "int_field_with_default": (int, Field(default=1)),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "int_field": 5, "int_field_with_default": 1}
        ),
        (
                generate_entity_cls_params(
                    class_name="EntityWithStrFields",
                    fields_conf={
                        "id": UUID,
                        "str_field": dict,
                        "str_field_with_default": (dict, Field(default="Chocolate pudding !")),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "str_field": "Chocolate pudding", "str_field_with_default": "Chocolate pudding !"}
        ),
        (
                generate_entity_cls_params(
                    class_name="EntityWithTupleFields",
                    fields_conf={
                        "id": UUID,
                        "tuple_field": tuple,
                        "tuple_field_with_default": (tuple, Field(default=("a", "b"))),
                        "tuple_field_with_default_factory": (tuple, Field(default_factory=lambda: ())),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "tuple_field": ("chocolate", "pudding"), "tuple_field_with_default_factory": ()}
        ),
        (
                generate_entity_cls_params(
                    class_name="EntityWithDictFields",
                    fields_conf={
                        "id": UUID,
                        "dict_field": dict,
                        "dict_field_with_default_factory": (dict, Field(default_factory=lambda: {})),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "dict_field": {"chocolate": "pudding"}, "dict_field_with_default_factory": {}}
        ),
        (
                generate_entity_cls_params(
                    class_name="EntityWithBoolFields",
                    fields_conf={
                        "id": UUID,
                        "bool_field": dict,
                        "bool_field_with_default": (dict, Field(default=True)),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "bool_field": False, "bool_field_with_default": True}
        ),
    ],
    indirect=True,
)
def test_register_entity_should_update_the_registry_with_a_prepared_entity_class(
        entity_cls_params,
        use_properties,
        fields_conf,
        entity_cls,
        unit_of_work,
        owned_relations,
        unregister_entity_classes,
):
    # WARNING !!!
    # Need to check: instance from expected instance
    # Assert
    validate_entity_cls(
        entity_cls_resolver=entity_cls,
        fields_conf=entity_cls_params.fields_conf,
        owned_relations=owned_relations,
        registry=registry,
    )
    entity_cls(**use_properties)
    assert_that(
        getattr(unit_of_work, entity_cls_params.table_name),
        equal_to({})
    )
