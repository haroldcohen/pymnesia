"""Provides with fixtures related to dynamically declared entities.
"""
import pytest

__all__ = ["entity_class_name", "table_name", "fields_conf", "entity_class"]

from tests.common_utils.helpers.make import make_entity_class


@pytest.fixture()
def entity_class_name(request):
    return request.param


@pytest.fixture()
def table_name(request):
    return request.param


@pytest.fixture()
def fields_conf(request):
    return request.param


@pytest.fixture()
def entity_class(entity_class_name, table_name, fields_conf, registry):
    return make_entity_class(
        class_name=entity_class_name,
        table_name=table_name,
        fields=fields_conf,
        registry=registry
    )
