from dataclasses import fields, MISSING

__all__ = ["extract_entity_class_fields", "extract_expected_dataclass_fields"]

from typing import List, Dict

from pymnesia.entities.field import UNDEFINED
from tests.common_utils.helpers.make import FieldsConf, is_type_and_field_tuple


def extract_entity_class_fields(entity_class) -> List[Dict]:
    fields_to_assert = []
    for entity_field in fields(entity_class):
        fields_to_assert.append({
            "name": entity_field.name,
            "type": entity_field.type,
            "default": entity_field.default,
            "default_factory": entity_field.default_factory,
        })

    return fields_to_assert


def extract_expected_dataclass_fields(fields_conf: FieldsConf) -> List[Dict]:
    expected_fields = []
    for field_name, field_conf in fields_conf.items():
        expected = {"name": field_name, "type": field_conf, "default": MISSING, "default_factory": MISSING}
        if is_type_and_field_tuple(field_conf):
            field = field_conf[1]
            expected["type"] = field_conf[0]
            expected["default"] = field.default if field.default is not UNDEFINED else MISSING
            expected["default_factory"] = field.default_factory \
                if field.default_factory is not UNDEFINED else MISSING
        expected_fields.append(expected)

    return expected_fields
