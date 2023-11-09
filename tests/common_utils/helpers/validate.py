"""Provides with validation functions.
"""
from typing import List

from pymnesia.entities.entity_resolver import EntityClassResolver
from tests.common_utils.helpers.assert_that import assert_that_entity_cls_conf_equal_to_expected, \
    assert_that_entity_cls_attributes_equal_to_expected, assert_that_entity_cls_fields_equal_to_expected
from tests.common_utils.helpers.expected import build_expected_entity_cls_conf, build_expected_entity_cls_attributes, \
    build_expected_entity_cls_attributes_with_relations, build_expected_entity_cls_fields
from tests.common_utils.helpers.make import FieldsConf

__all__ = [
    "validate_entity_cls",
    "validate_entity_cls_conf",
    "validate_entity_cls_attributes",
    "validate_entity_cls_fields",
]


def validate_entity_cls(
        entity_cls_resolver: EntityClassResolver,
        fields_conf: FieldsConf,
        owned_relations: List[str],
):
    """Validates an entity class.

    :param entity_cls_resolver:
    :param fields_conf:
    :param owned_relations:
    :return: None
    """
    validate_entity_cls_attributes(
        entity_cls_resolver=entity_cls_resolver,
        fields_conf=fields_conf,
    )
    validate_entity_cls_fields(
        entity_cls_resolver=entity_cls_resolver,
        fields_conf=fields_conf,
    )
    validate_entity_cls_conf(
        entity_cls_resolver=entity_cls_resolver,
        fields_conf=fields_conf,
        owned_relations=owned_relations,
    )


def validate_entity_cls_conf(
        entity_cls_resolver: EntityClassResolver,
        fields_conf: FieldsConf,
        owned_relations: List[str],
):
    """Validates an entity class conf.

    :param entity_cls_resolver:
    :param fields_conf:
    :param owned_relations:
    :return: None
    """
    expected_entity_cls_conf = build_expected_entity_cls_conf(
        entity_cls_resolver=entity_cls_resolver,
        fields_conf=fields_conf,
        owned_relations=owned_relations,
    )
    assert_that_entity_cls_conf_equal_to_expected(
        actual_conf=entity_cls_resolver.__conf__,
        expected_conf=expected_entity_cls_conf
    )


def validate_entity_cls_attributes(
        entity_cls_resolver: EntityClassResolver,
        fields_conf: FieldsConf,
):
    """Validates an entity class attributes.

    :param entity_cls_resolver:
    :param fields_conf:
    :return: None
    """
    if entity_cls_resolver.__conf__.relations:
        expected_entity_cls_attributes = build_expected_entity_cls_attributes_with_relations(
            entity_cls_resolver=entity_cls_resolver,
            fields_conf=fields_conf,
        )
    else:
        expected_entity_cls_attributes = build_expected_entity_cls_attributes(fields_conf=fields_conf)

    assert_that_entity_cls_attributes_equal_to_expected(
        actual_entity_cls=entity_cls_resolver,
        expected_attributes=expected_entity_cls_attributes,
    )


def validate_entity_cls_fields(
        entity_cls_resolver: EntityClassResolver,
        fields_conf: FieldsConf,
):
    """Validates an entity class fields.

    :param entity_cls_resolver:
    :param fields_conf:
    :return: None
    """
    expected_entity_cls_fields = build_expected_entity_cls_fields(
        fields_conf=fields_conf,
    )

    assert_that_entity_cls_fields_equal_to_expected(
        actual_entity_cls=entity_cls_resolver,
        expected_fields=expected_entity_cls_fields,
    )
