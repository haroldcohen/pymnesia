"""Provides with assertion functions.
"""
from dataclasses import Field
from typing import Dict, List

from hamcrest import assert_that, equal_to

from pymnesia.entities.entity_cls_conf import EntityClsConf
from pymnesia.entities.entity_resolver import EntityClassResolver
from tests.common_utils.helpers.extract import extract_entity_class_fields

__all__ = [
    "assert_that_entity_cls_conf_equal_to_expected",
    "assert_that_entity_cls_attributes_equal_to_expected",
    "assert_that_entity_cls_fields_equal_to_expected",
]


def assert_that_entity_cls_conf_equal_to_expected(
        actual_conf: EntityClsConf,
        expected_conf: EntityClsConf,
):
    """Asserts that an entity class conf is as expected.

    :param actual_conf:
    :param expected_conf:
    :return:
    """
    assert_that(
        actual_conf,
        equal_to(expected_conf)
    )


def assert_that_entity_cls_attributes_equal_to_expected(
        actual_entity_cls: EntityClassResolver,
        expected_attributes: Dict,
):
    """Asserts that an entity class attributes are as expected.

    :param actual_entity_cls:
    :param expected_attributes:
    :return:
    """
    assert_that(
        actual_entity_cls.__annotations__,
        equal_to(expected_attributes)
    )


def assert_that_entity_cls_fields_equal_to_expected(
        actual_entity_cls: EntityClassResolver,
        expected_fields: List[Field],
):
    """Asserts that an entity class fields are as expected.

    :param actual_entity_cls:
    :param expected_fields:
    :return:
    """
    assert_that(
        extract_entity_class_fields(actual_entity_cls),
        equal_to(sorted(expected_fields, key=lambda e: e["name"]))
    )
