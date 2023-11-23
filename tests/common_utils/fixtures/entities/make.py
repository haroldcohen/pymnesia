"""Provides with fixtures related to dynamically declared entities.
"""
from typing import Dict, List

import pytest

from pymnesia.entities.entity_resolver import EntityClassResolver
from pymnesia.entities.relations import Relation
from tests.common_utils.helpers.relations.types import RelatedEntityClassesParams
from tests.common_utils.helpers.make import make_entity_class
from tests.common_utils.helpers.types import FieldsConf

# pylint: disable=redefined-outer-name

__all__ = [
    "entity_class_name",
    "table_name",
    "fields_conf",
    "reverse",
    "use_relation_api",
    "related_entity_classes_params",
    "instance_values",
    "related_entity_classes",
    "entity_class",
]


@pytest.fixture()
def entity_class_name(request) -> str:
    """The name to use for making an entity class.
    """
    return request.param


@pytest.fixture()
def table_name(request) -> str:
    """The table name to use for making an entity class.
    """
    return request.param


@pytest.fixture()
def fields_conf(request) -> FieldsConf:
    """The fields to make for an entity class.
    :return: Either a dict of Type or a dict of a tuple of a Type and a Field.
    """
    return request.param


@pytest.fixture()
def reverse(request) -> str:
    return request.param


@pytest.fixture()
def use_relation_api(request) -> bool:
    return request.param


@pytest.fixture()
def entity_class(
        entity_class_name: str,
        table_name: str,
        fields_conf: FieldsConf,
        related_entity_classes: Dict[str, EntityClassResolver],  # pylint: disable=unused-argument
        related_entity_classes_params: RelatedEntityClassesParams,
) -> EntityClassResolver:
    """Returns a dynamically made non-relational entity class resolver.

    :param entity_class_name: The class name to use for making the class.
    :param table_name: The table name under which the entity should be registered.
    :param fields_conf: The fields to make
    :param related_entity_classes:
    :param related_entity_classes_params:
    :return: An entity class resolver
    """
    for related_entity_class_params in related_entity_classes_params:
        # noinspection PyTypeChecker
        fields_conf[related_entity_class_params.single_form] = related_entity_class_params.cls_resolver

    entity_class = make_entity_class(
        name=entity_class_name,
        table_name=table_name,
        fields_conf=fields_conf,
    )

    for related_entity_class_params in related_entity_classes_params:
        related_entity_class_params.fields_conf[entity_class.__tablename__[0:-1]] = (
            entity_class,
            Relation(reverse=related_entity_class_params.single_form, is_owner=False)
        )

    return entity_class


@pytest.fixture()
def related_entity_classes_params(request) -> RelatedEntityClassesParams:
    if hasattr(request, "param"):
        return request.param

    return []


@pytest.fixture()
def related_entity_classes(related_entity_classes_params: RelatedEntityClassesParams) -> List[EntityClassResolver]:
    """
    :param related_entity_classes_params:
    :return:
    """
    entity_classes = []

    for rel_entity_cls_param in related_entity_classes_params:
        related_entity_cls = make_entity_class(
            name=rel_entity_cls_param.name,
            table_name=rel_entity_cls_param.table_name,
            fields_conf=rel_entity_cls_param.fields_conf
        )
        entity_classes.append(related_entity_cls)
        rel_entity_cls_param.cls_resolver = related_entity_cls

    return entity_classes


@pytest.fixture()
def instance_values(request) -> dict:
    """The values to use for instantiating an expected entity instance.
    """
    return request.param
