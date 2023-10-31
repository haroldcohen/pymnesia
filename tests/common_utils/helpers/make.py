"""Provides with dynamically constructed entity classes.
"""
from dataclasses import MISSING
from typing import Any, Dict, Union, Tuple

from pymnesia.entities.field import Field, UNDEFINED
from pymnesia.entities.base import BaseEntity
from pymnesia.entities.meta import EntityMeta

__all__ = ["make_entity_class", "is_type_and_field_tuple"]


class GenericEntityMeta(type):
    def __new__(mcs, name, base, attrs):
        new_attributes = {"__annotations__": {}}
        for field_name, field_conf in attrs["fields"].items():
            if is_type_and_field_tuple(field_conf):
                field_ = field_conf[1]
                new_attributes["__annotations__"][field_name] = field_conf[0]
                field_attrs = {
                    "default": field_.default if field_.default is not UNDEFINED else MISSING,
                    "default_factory": field_.default_factory
                    if field_.default_factory is not UNDEFINED else MISSING,
                }
                new_attributes[field_name] = Field(
                    **field_attrs,
                )
            else:
                new_attributes["__annotations__"][field_name] = field_conf
        for attr_name, attr_value in attrs.items():
            new_attributes[attr_name] = attr_value
        return super().__new__(mcs, name, base, new_attributes)


def make_entity_class(name: str, table_name: str, fields_conf: Dict[str, Union[type, Tuple[type, Field]]]):
    class GenericEntity(metaclass=GenericEntityMeta):
        __tablename__ = table_name

        fields = fields_conf

    return EntityMeta(name, [BaseEntity], GenericEntity.__dict__)


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
