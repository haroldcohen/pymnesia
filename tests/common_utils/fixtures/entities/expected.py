"""Provides with fixtures to build expected entities.
"""
import pytest

from tests.common_utils.helpers import extract_entity_class_fields, extract_expected_dataclass_fields
from tests.common_utils.helpers.expected import build_expected_entity_cls_attributes
from tests.common_utils.helpers.make import FieldsConf

__all__ = ["expected_entity", "expected_entities", "limit", "direction", "order_by_key", "use_properties",
           "where_clause", "or_clauses", "expected_entity_attributes", "expected_dataclass_fields",
           "extracted_entity_class_fields", "expected_entity_instance", "use_dedicated_properties"]


@pytest.fixture()
def expected_entity(
        request,
        expected_unit_of_work_memento,
        use_properties
):  # pylint: disable=redefined-outer-name
    """Returns an entity instance to be used for assertion (and action as well)."""
    if hasattr(request, "param"):
        entity = request.param
        if len(use_properties):
            for prop, value in use_properties.items():
                setattr(entity, prop, value)
        table = getattr(expected_unit_of_work_memento, entity.__tablename__)
        table[entity.id] = entity

        return entity

    return None


@pytest.fixture()
def expected_entities(
        request,
        expected_unit_of_work_memento,
        use_properties,
        use_dedicated_properties
):  # pylint: disable=redefined-outer-name
    """Returns multiple entity instances to be used for assertion (and action as well)."""
    if hasattr(request, "param"):
        properties_idx = 0
        for entity in request.param:
            if use_properties:
                for prop, value in use_properties.items():
                    setattr(entity, prop, value)
            if use_dedicated_properties:
                for prop, value in use_dedicated_properties[properties_idx].items():
                    setattr(entity, prop, value)
            table = getattr(expected_unit_of_work_memento, entity.__tablename__)
            table[entity.id] = entity
            properties_idx += 1

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
def use_properties(request, where_clause):  # pylint: disable=redefined-outer-name
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
    return build_expected_entity_cls_attributes(fields_conf=fields_conf)


@pytest.fixture()
def expected_dataclass_fields(fields_conf: FieldsConf):
    return extract_expected_dataclass_fields(fields_conf=fields_conf)


@pytest.fixture()
def extracted_entity_class_fields(entity_class):
    return extract_entity_class_fields(entity_class)


@pytest.fixture()
def expected_entity_instance(entity_class, instance_values):
    """Returns an expected instance of an entity class based on provided values.

    :param entity_class: The entity class to instantiate.
    :param instance_values: The values to use.
    :return: A instance of the provided entity class.
    """
    return entity_class(**instance_values)


@pytest.fixture()
def use_dedicated_properties(request):
    if hasattr(request, "param"):
        return request.param
    return []
