"""Provides with dynamically constructed entity classes.
"""
from dataclasses import MISSING
from typing import Any, Dict, Union, Tuple

from pymnesia.entities.entity_resolver import EntityClassResolver
from pymnesia.entities.field import Field, UNDEFINED
from pymnesia.entities.relations import Relation
from pymnesia.entities.base import DeclarativeBase
from pymnesia.entities.meta import EntityMeta

__all__ = ["FieldConf", "FieldsConf", "make_entity_class", "is_type_and_field_tuple", "is_relation_field_conf"]

FieldConf = Union[type, Tuple[type, Union[Field, Relation]]]

FieldsConf = Dict[str, FieldConf]


class GenericEntityMeta(type):
    """Metaclass used for dynamically making entity classes.
    """

    def __new__(mcs, name, base, attrs):
        new_attributes = {"__annotations__": {}}
        for field_name, field_conf in attrs["fields"].items():
            if is_type_and_field_tuple(field_conf):
                new_attributes["__annotations__"][field_name] = field_conf[0]
                if not is_relation_field_conf(field_conf):
                    field_ = field_conf[1]
                    field_attrs = {
                        "default": field_.default if field_.default is not UNDEFINED else MISSING,
                        "default_factory": field_.default_factory
                        if field_.default_factory is not UNDEFINED else MISSING,
                    }
                    new_attributes[field_name] = Field(
                        **field_attrs,
                    )
                else:
                    new_attributes[field_name] = field_conf[1]
            else:
                new_attributes["__annotations__"][field_name] = field_conf
        for attr_name, attr_value in attrs.items():
            new_attributes[attr_name] = attr_value

        return super().__new__(mcs, name, base, new_attributes)


def make_entity_class(name: str, table_name: str, fields_conf: FieldsConf):
    """Dynamically creates an entity class.

    :param name: The name of the class to create.
    :param table_name: The table name under which the entity should be registered.
    :param fields_conf: A dict of field configurations.
    :return: A dynamically created entity class.
    """

    class GenericEntity(metaclass=GenericEntityMeta):
        __tablename__ = table_name

        fields = fields_conf

    return EntityMeta(name, [DeclarativeBase], GenericEntity.__dict__)


def is_type_and_field_tuple(field_conf: Any) -> bool:
    """Evaluates if a field configuration for a generic entity maker is a type or a tuple of type and Field instance.
    This function is used both for making an entity class and supplying with expected properties of an entity class.
    :param field_conf: The field configuration to evaluate.
    :return: A boolean indicating if it is a simple type or not.
    """
    if isinstance(field_conf, tuple):
        if isinstance(field_conf[0], (type, EntityClassResolver)) and isinstance(field_conf[1], (Field, Relation)):
            return True
        return False
    return False


def is_relation_field_conf(field_conf: Any) -> bool:
    """Evaluates if a field conf is a relation or not.

    :param field_conf: The field conf to evaluate.
    :return: bool
    """
    is_type_field_tuple = is_type_and_field_tuple(field_conf)
    if is_type_field_tuple:
        return isinstance(field_conf[0], EntityClassResolver)

    return isinstance(field_conf, EntityClassResolver)
