"""Provides with fixtures related to dynamically declared entities.
"""
from typing import List

import pytest

from pymnesia.api.entities import relation
from pymnesia.entities.relations import Relation
from pymnesia.entities.entity_resolver import EntityClassResolver
from tests.common_utils.helpers.entities.make.types import EntityClsParams
from tests.common_utils.helpers.entities.make.make import make_entity_class
from tests.common_utils.helpers.types import FieldsConf

# pylint: disable=redefined-outer-name

__all__ = [
    "entity_cls",
    "entity_cls_params",
    "rel_entity_classes",
    "fields_conf",
    "owned_relations",
]


@pytest.fixture(scope="class")
def entity_cls_params(request) -> EntityClsParams:
    """Provides with parameters to dynamically build an entity class without having to declare it in a hard coded way.

    :param request: The parametrized fixture.
    :return: The entity class parameters.
    """
    return request.param


@pytest.fixture(scope="class")
def fields_conf(
        entity_cls_params: EntityClsParams,
        rel_entity_classes: List[EntityClassResolver],  # pylint: disable=unused-argument
) -> FieldsConf:
    """Provides with the field configurations passed in entity_cls_params.
    The relation field configurations are modified accordingly.

    :param entity_cls_params: Entity class parameters provided by the matching fixture.
    :param rel_entity_classes: A list of related class generated in the matching fixture.
    :return: A dictionary of field confs.
    """
    for related_entity_class_params in entity_cls_params.rel_entity_classes_params:
        if related_entity_class_params.relation_type == "one_to_one":
            rel_conf = related_entity_class_params.cls_resolver
            if related_entity_class_params.owner_rel_api:
                rel_conf = (
                    rel_conf,
                    relation(reverse=related_entity_class_params.owner_rel_api.reverse)
                )
            # noinspection PyTypeChecker
            entity_cls_params.fields_conf[related_entity_class_params.single_form] = rel_conf
        if related_entity_class_params.relation_type == "many_to_one":
            rel_conf = List[related_entity_class_params.cls_resolver]
            if related_entity_class_params.owner_rel_api:
                rel_conf = (
                    rel_conf,
                    relation(reverse=related_entity_class_params.owner_rel_api.reverse)
                )
            # noinspection PyTypeChecker
            entity_cls_params.fields_conf[related_entity_class_params.table_name] = rel_conf

    return entity_cls_params.fields_conf


@pytest.fixture(scope="class")
def entity_cls(
        entity_cls_params: EntityClsParams,
        rel_entity_classes: List[EntityClassResolver],
):  # pylint: disable=unused-argument
    """Provides with a dynamically created entity class resolver,
    based on given entity class parameters.

    :param entity_cls_params: Entity class parameters provided by the matching fixture.
    :param rel_entity_classes: A list of related class generated in the matching fixture.
    :return: An dynamically created entity class resolver.
    """
    entity_cls_ = make_entity_class(
        name=entity_cls_params.name,
        table_name=entity_cls_params.table_name,
        fields_conf=entity_cls_params.fields_conf,
    )

    for related_entity_class_params in entity_cls_params.rel_entity_classes_params:
        field_name = entity_cls_.__tablename__[0:-1]
        if related_entity_class_params.owner_rel_api:
            field_name = related_entity_class_params.owner_rel_api.reverse
        reverse_ = related_entity_class_params.single_form
        if related_entity_class_params.relation_type == "many_to_one":
            reverse_ = related_entity_class_params.table_name
        related_entity_class_params.fields_conf[field_name] = (
            entity_cls_,
            Relation(
                reverse=reverse_,
                is_owner=False,
                relation_type=related_entity_class_params.relation_type,
            )
        )

    return entity_cls_


@pytest.fixture(scope="class")
def rel_entity_classes(entity_cls_params: EntityClsParams) -> List[EntityClassResolver]:
    """Provides with dynamically created related entity class resolvers,
    based on entity class parameters.

    :param entity_cls_params: Entity class parameters provided by the matching fixture.
    :return: A list of related entity class resolvers.
    """
    entity_classes = []

    for rel_entity_cls_param in entity_cls_params.rel_entity_classes_params:
        related_entity_cls = make_entity_class(
            name=rel_entity_cls_param.name,
            table_name=rel_entity_cls_param.table_name,
            fields_conf=rel_entity_cls_param.fields_conf
        )
        entity_classes.append(related_entity_cls)
        rel_entity_cls_param.cls_resolver = related_entity_cls

    return entity_classes


@pytest.fixture(scope="class")
def owned_relations(
        entity_cls,  # pylint: disable=unused-argument
        entity_cls_params: EntityClsParams,
        rel_entity_classes: List[EntityClassResolver],  # pylint: disable=unused-argument
) -> List[str]:
    """Provides with a list of owned relations for a given entity class.

    :param entity_cls: The entity class for which to list the owned relations.
    :param entity_cls_params: Entity class parameters provided by the matching fixture.
    :param rel_entity_classes: A list of related class generated in the matching fixture.
    :return: A list of owned relation names.
    """
    return [rel_entity_cls_params.single_form for rel_entity_cls_params in entity_cls_params.rel_entity_classes_params]
