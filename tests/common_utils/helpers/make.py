"""Provides with dynamically constructed entity classes.
"""
from dataclasses import MISSING
from typing import Any, Dict, Union, Tuple

from pymnesia.entities.field import Field, UNDEFINED
from pymnesia.entities.registry import PymnesiaRegistry

__all__ = ["make_entity_class", "is_type_and_field_tuple"]


class GenericEntityType(type):
    """Metaclass for generic entities.
    It allows to add attributes and properties such as Fields, and to set a class name according to a config parameter.
    """

    def __new__(mcs, name, bases, attrs):
        new_attrs = {"__annotations__": {}}

        config = attrs["config"]
        name = config["name"]
        for field_name, field_conf in config["fields"].items():
            if is_type_and_field_tuple(field_conf):
                field_ = field_conf[1]
                new_attrs["__annotations__"][field_name] = field_conf[0]
                field_attrs = {
                    "default": field_.default if field_.default is not UNDEFINED else MISSING,
                    "default_factory": field_.default_factory
                    if field_.default_factory is not UNDEFINED else MISSING,
                }
                new_attrs[field_name] = Field(
                    **field_attrs,
                )
            else:
                new_attrs["__annotations__"][field_name] = field_conf

        return super().__new__(mcs, name, bases, new_attrs)


def make_entity_class(
        class_name: str,
        table_name: str,
        fields: Dict[str, Union[type, Tuple[type, Field]]],
        registry: PymnesiaRegistry
):
    """Dynamically creates entity class and registers them in a Pymnesia registry.

    :param class_name: The class name to be used
    :param table_name: The table name under which the entity should be registered
    :param fields: The configuration use to create the entity class fields
    :param registry: The registry in which the class should be registered
    :return: A entity class
    """

    class GenericEntityBase(metaclass=GenericEntityType):
        config = {
            "name": class_name,
            "fields": {}
        }

    @registry.entity(table_name=table_name)
    class GenericEntity(GenericEntityBase):
        config = {
            "name": class_name,
            "fields": fields
        }

    return GenericEntity


def is_type_and_field_tuple(field_conf: Any) -> bool:
    """Evaluates if a field configuration for a generic entity maker is a type or a tuple of type and Field instance.
    This function is used both for making an entity class and supplying with expected properties of an entity class.
    :param field_conf: The field configuration to evaluate.
    :return: A boolean indicating if it is a simple type or not.
    """
    if isinstance(field_conf, tuple):
        if isinstance(field_conf[0], type) and isinstance(field_conf[1], Field):
            return True
        return False
    return False
