"""Provides with unit tests to validate entities registry related features.
"""
import re
from uuid import UUID, uuid4

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.registry import unregister_entity_classes
from pymnesia.core.entities.registry import DEFAULT_E_CLASSES_REGISTRY
from pymnesia.api.entities.fields import field
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
                        "float_f": float,
                        "float_f_w_default": (float, field(default=5.5)),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "float_f": 0.5, "float_f_w_default": 5.5}
        ),
        (
                generate_entity_cls_params(
                    class_name="EntityWithIntFields",
                    fields_conf={
                        "id": UUID,
                        "int_f": int,
                        "int_f_w_default": (int, field(default=1)),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "int_f": 5, "int_f_w_default": 1}
        ),
        (
                generate_entity_cls_params(
                    class_name="EntityWithStrFields",
                    fields_conf={
                        "id": UUID,
                        "str_f": dict,
                        "str_f_w_default": (dict, field(default="Chocolate pudding !")),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "str_f": "Chocolate pudding", "str_f_w_default": "Chocolate pudding !"}
        ),
        (
                generate_entity_cls_params(
                    class_name="EntityWithTupleFields",
                    fields_conf={
                        "id": UUID,
                        "tuple_f": tuple,
                        "tuple_f_w_default": (tuple, field(default=("a", "b"))),
                        "tuple_f_w_default_factory": (tuple, field(default_factory=lambda: ())),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "tuple_f": ("chocolate", "pudding"), "tuple_f_w_default_factory": ()}
        ),
        (
                generate_entity_cls_params(
                    class_name="EntityWithDictFields",
                    fields_conf={
                        "id": UUID,
                        "dict_f": dict,
                        "dict_f_w_default_factory": (dict, field(default_factory=lambda: {})),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "dict_f": {"chocolate": "pudding"}, "dict_f_w_default_factory": {}}
        ),
        (
                generate_entity_cls_params(
                    class_name="EntityWithBoolFields",
                    fields_conf={
                        "id": UUID,
                        "bool_f": dict,
                        "bool_f_w_default": (dict, field(default=True)),
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4(), "bool_f": False, "bool_f_w_default": True}
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
        registry=DEFAULT_E_CLASSES_REGISTRY,
    )
    properties_without_defaults = {}
    for prop_name, prop_value in use_properties.items():
        if not re.match(r'^.*_w_default.*$', prop_name):
            properties_without_defaults[prop_name] = prop_value
    assert_that(
        entity_cls(**use_properties),
        equal_to(entity_cls(**properties_without_defaults))
    )
    assert_that(
        getattr(unit_of_work, entity_cls_params.table_name),
        equal_to({})
    )
