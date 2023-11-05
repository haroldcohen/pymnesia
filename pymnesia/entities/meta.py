"""Provides with a metaclass for entities.
"""
from dataclasses import make_dataclass, field, fields as dataclass_fields, MISSING, Field as DataclassField
from typing import List, Type, Tuple, Dict, Union
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
        relation_fields = {}
        relations = {}
        tablename = attrs["__tablename__"]

        for field_name, field_type in attrs["__annotations__"].items():
            if field_name in attrs.keys():
                field_as_attr = attrs[field_name]
                if isinstance(field_as_attr, Field):
                    fields.append((
                        field_name,
                        field_type,
                        field(  # pylint: disable=invalid-field-call
                            **_extract_entity_field_attrs(field_as_attr, UNDEFINED)
                        )
                    ))
                if isinstance(field_as_attr, Relation):
                    relations[field_type] = field_as_attr
                    add_foreign_key_to_fields(
                        relation_name=field_name,
                        fields=fields,
                        is_nullable=field_as_attr.is_nullable
                    )
                    relation_fields[field_type] = field_name
            else:
                if issubclass(field_type, Entity):
                    relations[field_type] = Relation(reverse=tablename[0:-1])
                    add_foreign_key_to_fields(relation_name=field_name, fields=fields, is_nullable=False)
                    relation_fields[field_type] = field_name
                else:
                    fields.append((
                        field_name,
                        field_type
                    ))

        cls_resolver = registry.register(
            _make_entity_dataclass(
                name=name,
                tablename=tablename,
                fields=fields,
            )
        )
        if relations:
            _make_relations(
                relations=relations,
                cls_resolver=cls_resolver,
                relation_fields=relation_fields,
                cls_resolver_current_fields=_extract_entity_cls_fields(cls_resolver)
            )

        return cls_resolver


def _make_relations(
        relations: Dict[Type[Entity], Relation],
        cls_resolver,
        relation_fields: Dict[Type[Entity], str],
        cls_resolver_current_fields: List[Tuple],
):
    """Makes relations for both the relation owner and the related entities.
    After making dataclasses for every related entity, the relation owner entity is updated with
    the newly made relations.

    :param relations: The relations to make.
    :param cls_resolver: The relation owner entity class resolver.
    :param relation_fields: A dictionary where the key is the relation and the value the relation name.
    :param cls_resolver_current_fields: The current existing fields for the relationship owner.
    :return: None
    """
    tablename = cls_resolver.__tablename__
    nullable_fields = []

    for relation, relation_field in relations.items():
        relation_current_fields = _extract_entity_cls_fields(relation)
        add_foreign_key_to_fields(
            relation_name=tablename[0:-1],
            fields=relation_current_fields,
            is_nullable=relation_field.is_nullable,
        )
        add_relation_to_fields(
            relation_name=relation_field.reverse,
            relation=cls_resolver,
            fields=relation_current_fields
        )
        relation_new_cls = _make_entity_dataclass(
            name=relation.__name__,
            tablename=relation.__tablename__,
            fields=relation_current_fields
        )
        relation.update_entity_cls(relation_new_cls)
        add_relation_to_fields(
            relation_name=relation_fields[relation],
            relation=relation,
            fields=nullable_fields,
        )

    updated_entity_cls = _make_entity_dataclass(
        name=cls_resolver.__name__,
        tablename=tablename,
        fields=cls_resolver_current_fields + nullable_fields
    )
    cls_resolver.update_entity_cls(updated_entity_cls)


def _make_entity_dataclass(name: str, tablename: str, fields: List[Tuple]):
    """Makes a dataclass from entity class parameters.

    :param name: The entity class name
    :param tablename: The table name under which the entity should be registered
    :param fields: The fields to create for the entity dataclass
    :return: A entity dataclass
    """
    entity_cls = make_dataclass(name, fields, bases=(Entity,))
    entity_cls.__tablename__ = tablename

    return entity_cls


def _extract_entity_cls_fields(entity_cls) -> List[Tuple]:
    """Extracts the dataclass fields of an entity class.

    :param entity_cls: The entity class to extract the fields from.
    :return: A list of extracted dataclass fields.
    """
    fields = []
    for dataclass_field in dataclass_fields(entity_cls):
        fields.append((
            dataclass_field.name,
            dataclass_field.type,
            field(**_extract_entity_field_attrs(dataclass_field, MISSING))  # pylint: disable=invalid-field-call
        ))

    return fields


def _extract_entity_field_attrs(
        entity_field: Union[DataclassField, Field],
        default_check
) -> Dict:
    """Extracts field attributes from either a dataclass field or a pymnesia field.

    :param entity_field: The object from which to extract the attributes.
    :param default_check: The check value used for checking if a default value or default_factory value has been set.
    :return: A dictionary containing the extracted attributes.
    """
    field_attrs = {}

    if entity_field.default is not default_check:
        field_attrs["default"] = entity_field.default
    if entity_field.default_factory is not default_check:
        field_attrs["default_factory"] = entity_field.default_factory

    return field_attrs


def add_foreign_key_to_fields(relation_name: str, fields: List, is_nullable: bool):
    """Adds a foreign key to an entity class.
    Procedural function that mutates fields.

    :param relation_name: The name of the relation from which the foreign key should be built and added.
    :param fields: The list of fields instance to which the foreign key should be added.
    :param is_nullable: Wether the relation is nullable or not.
    """
    fields.append((
        build_foreign_key_name(relation_name),
        UUID,
        field(default=None if is_nullable else MISSING)  # pylint: disable=invalid-field-call
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
    :return: A built foreign key name.
    """
    return relation_name + "_id"
