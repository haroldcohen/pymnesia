"""Provides with a metaclass for entities.
"""
from dataclasses import make_dataclass, field
from typing import List, Type
from uuid import UUID

from pymnesia.entities.field import UNDEFINED, Field
from pymnesia.entities.entity import Entity
from pymnesia.entities.registry import registry
from pymnesia.entities.relations import Relation


class EntityMeta(type):
    """Metaclass for entities.

    Responsible for making dataclasses out of declared entities and registering them in the active registry.
    """

    def __new__(mcs, name, base, attrs):
        if name == "DeclarativeBase":
            return super().__new__(mcs, name, base, attrs)

        fields = []
        nullable_fields = []
        relations = {}
        for field_name, field_type in attrs["__annotations__"].items():
            if field_name in attrs.keys():
                field_as_attr = attrs[field_name]
                if isinstance(field_as_attr, Field):
                    dataclass_field_attrs = {}
                    if field_as_attr.default is not UNDEFINED:
                        dataclass_field_attrs["default"] = field_as_attr.default
                    if field_as_attr.default_factory is not UNDEFINED:
                        dataclass_field_attrs["default_factory"] = field_as_attr.default_factory
                    fields.append((
                        field_name,
                        field_type,
                        field(**dataclass_field_attrs)  # pylint: disable=invalid-field-call
                    ))
                if isinstance(field_as_attr, Relation):
                    relations[field_type] = field_as_attr
                    add_foreign_key_to_fields(relation_name=field_name, fields=fields)
                    add_relation_to_fields(
                        relation_name=field_name,
                        relation=field_type,
                        fields=nullable_fields
                    )
            else:
                if issubclass(field_type, Entity):
                    relations[field_type] = Relation(reverse=attrs["__tablename__"][0:-1])
                    add_foreign_key_to_fields(relation_name=field_name, fields=fields)
                    add_relation_to_fields(
                        relation_name=field_name,
                        relation=field_type,
                        fields=nullable_fields
                    )
                else:
                    fields.append((
                        field_name,
                        field_type
                    ))

        cls = make_dataclass(name, fields + nullable_fields, bases=(Entity,))
        cls.__tablename__ = attrs["__tablename__"]
        registry.register(cls)

        for relation, relation_field in relations.items():
            relation.__annotations__[relation_field.reverse] = cls

        return cls


def add_foreign_key_to_fields(relation_name: str, fields: List):
    """Adds a foreign key to an entity class.
    Procedural function that mutates fields.

    :param relation_name: The name of the relation from which the foreign key should be built and added.
    :param fields: The list of fields instance to which the foreign key should be added.
    """
    fields.append((
        build_foreign_key_name(relation_name),
        UUID
    ))


def add_relation_to_fields(relation_name: str, relation: Type[Entity], fields: List):
    """Adds a foreign key to an entity class.
    Procedural function that mutates fields.

    :param relation_name: The name of the relation from which the foreign key should be built and added.
    :param relation:
    :param fields: The list of fields instance to which the foreign key should be added.
    """
    fields.append(
        (relation_name, relation, field(default=None))  # pylint: disable=invalid-field-call
    )


def build_foreign_key_name(relation_name: str) -> str:
    """Builds a foreign key name, based on a relation name.

    :param relation_name: The relation name from which to build the foreign key name.
    :return:
    """
    return relation_name + "_id"
