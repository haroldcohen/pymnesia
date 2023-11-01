"""Provides with a metaclass for entities.
"""
from dataclasses import make_dataclass, field

from pymnesia.entities.field import UNDEFINED
from pymnesia.entities.entity import Entity
from pymnesia.entities.registry import registry


class EntityMeta(type):
    """Metaclass for entities.

    Responsible for making dataclasses out of declared entities and registering them in the active registry.
    """

    def __new__(mcs, name, base, attrs):
        if name == "DeclarativeBase":
            return super().__new__(mcs, name, base, attrs)

        fields_to_create = []
        relations = []
        for field_name, field_type in attrs["__annotations__"].items():
            if field_name in attrs.keys():
                field_as_attr = attrs[field_name]
                dataclass_field_attrs = {}
                if field_as_attr.default is not UNDEFINED:
                    dataclass_field_attrs["default"] = field_as_attr.default
                if field_as_attr.default_factory is not UNDEFINED:
                    dataclass_field_attrs["default_factory"] = field_as_attr.default_factory
                fields_to_create.append((
                    field_name,
                    field_type,
                    field(**dataclass_field_attrs)  # pylint: disable=invalid-field-call
                ))
            else:
                fields_to_create.append((
                    field_name,
                    field_type
                ))
                if issubclass(field_type, Entity):
                    relations.append(field_type)

        cls = make_dataclass(name, fields_to_create, bases=(Entity,))
        cls.__tablename__ = attrs["__tablename__"]
        registry.register(cls)

        for relation in relations:
            relation.__annotations__[cls.__tablename__[0:-1]] = cls

        return cls
