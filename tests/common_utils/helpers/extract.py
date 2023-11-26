from dataclasses import fields

from typing import List, Dict

__all__ = [
    "extract_entity_class_fields",
]


def extract_entity_class_fields(entity_class) -> List[Dict]:
    fields_to_assert = []
    for entity_field in fields(entity_class):
        fields_to_assert.append({
            "name": entity_field.name,
            "type": entity_field.type,
            "default": entity_field.default,
            "default_factory": entity_field.default_factory,
        })

    return sorted(fields_to_assert, key=lambda e: e["name"])
