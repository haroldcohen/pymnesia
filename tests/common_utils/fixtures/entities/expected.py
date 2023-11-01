"""Provides with fixtures to build expected entities.
"""
from dataclasses import fields, MISSING
from typing import Dict, Union, Tuple

import pytest

__all__ = ["expected_entity", "expected_entities", "limit", "direction", "order_by_key", "use_properties",
           "where_clause", "or_clauses", "expected_entity_attributes", "expected_dataclass_fields",
           "extracted_entity_class_fields", "expected_entity_instance"]

from pymnesia.entities.field import UNDEFINED, Field
from tests.common_utils.helpers.make import is_type_and_field_tuple


@pytest.fixture()
def expected_entity(request, expected_unit_of_work_memento, use_properties):
    """Returns an entity instance to be used for assertion (and action as well)."""
    if hasattr(request, "param"):
        entity = request.param
        if len(use_properties):
            for prop, value in use_properties.items():
                setattr(entity, prop, value)
        table = getattr(expected_unit_of_work_memento, entity.config.table_name)
        table[entity.id] = entity

        return entity

    return None


@pytest.fixture()
def expected_entities(request, expected_unit_of_work_memento, use_properties):
    """Returns multiple entity instances to be used for assertion (and action as well)."""
    if hasattr(request, "param"):
        for entity in request.param:
            if len(use_properties):
                for prop, value in use_properties.items():
                    setattr(entity, prop, value)
            table = getattr(expected_unit_of_work_memento, entity.config.table_name)
            table[entity.id] = entity

        return request.param

    return []


@pytest.fixture()
def limit(request):
    if hasattr(request, "param"):
        return request.param
    return 0


@pytest.fixture()
def order_by_key(request):
    return request.param


@pytest.fixture()
def direction(request):
    if hasattr(request, "param"):
        return request.param
    return "asc"


@pytest.fixture()
def use_properties(request, where_clause):
    if hasattr(request, "param"):
        return request.param
    if len(where_clause):
        use_properties_ = {}
        for condition, value in where_clause.items():
            use_properties_[condition] = value
        return use_properties_
    return {}


@pytest.fixture()
def where_clause(request):
    if hasattr(request, "param"):
        return request.param
    return {}


@pytest.fixture()
def or_clauses(request):
    if hasattr(request, "param"):
        return request.param
    return []


@pytest.fixture()
def expected_entity_attributes(fields_conf):
    expected_attrs = {}
    for field_name, field_conf in fields_conf.items():
        if is_type_and_field_tuple(field_conf):
            expected_attrs[field_name] = field_conf[0]
        else:
            expected_attrs[field_name] = field_conf

    return expected_attrs


@pytest.fixture()
def expected_dataclass_fields(fields_conf: Dict[str, Union[type, Tuple[type, Field]]]):
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


@pytest.fixture()
def extracted_entity_class_fields(entity_class):
    fields_to_assert = []
    for entity_field in fields(entity_class):
        fields_to_assert.append({
            "name": entity_field.name,
            "type": entity_field.type,
            "default": entity_field.default,
            "default_factory": entity_field.default_factory,
        })

    return fields_to_assert


@pytest.fixture()
def expected_entity_instance(entity_class, instance_values):
    """Returns an expected instance of an entity class based on provided values.

    :param entity_class: The entity class to instantiate.
    :param instance_values: The values to use.
    :return: A instance of the provided entity class.
    """
    return entity_class(**instance_values)
