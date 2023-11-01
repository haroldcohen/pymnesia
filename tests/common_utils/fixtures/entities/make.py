"""Provides with fixtures related to dynamically declared entities.
"""
from typing import Union, Type, Dict, Tuple

import pytest

__all__ = ["entity_class_name", "table_name", "fields_conf", "entity_class", "instance_values"]

from pymnesia.entities.field import Field
from tests.common_utils.helpers.make import make_entity_class


@pytest.fixture()
def entity_class_name(request):
    """The name to use for making an entity class.
    """
    return request.param


@pytest.fixture()
def table_name(request):
    """The table name to use for making an entity class.
    """
    return request.param


@pytest.fixture()
def fields_conf(request) -> Dict[str, Union[Type, Tuple[Type, Field]]]:
    """The fields to make for an entity class.
    :return: Either a dict of Type or a dict of a tuple of a Type and a Field.
    """
    return request.param


@pytest.fixture()
def entity_class(entity_class_name, table_name, fields_conf):
    """Returns a dynamically made entity class.

    :param entity_class_name: The class name to use for making the class.
    :param table_name: The table name under which the entity should be registered.
    :param fields_conf: The fields to make
    :return: An entity class
    """
    return make_entity_class(
        name=entity_class_name,
        table_name=table_name,
        fields_conf=fields_conf,
    )


@pytest.fixture()
def instance_values(request):
    """The values to use for instantiating an expected entity instance.
    """
    return request.param
