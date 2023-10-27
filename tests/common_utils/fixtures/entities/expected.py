"""Provides with fixtures to build expected entities.
"""
from dataclasses import fields, MISSING

import pytest

__all__ = ["expected_entity", "expected_entities", "limit", "direction", "order_by_key", "use_properties",
           "where_clause", "or_clauses", "expected_entity_attributes", "expected_dataclass_fields",
           "extracted_entity_class_fields"]


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
        expected_attrs[field_name] = field_conf["type"]

    return expected_attrs


@pytest.fixture()
def expected_dataclass_fields(fields_conf):
    expected_fields = []
    for field_name, field_conf in fields_conf.items():
        expected = {"name": field_name, "type": field_conf["type"]}
        if field_conf["make_field"]:
            expected["default"] = field_conf["field"]["default"]
        else:
            expected["default"] = MISSING
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
        })

    return fields_to_assert
