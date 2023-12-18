"""Provides with a metaclass for entities.
"""
from dataclasses import make_dataclass, field, fields as dataclass_fields, MISSING, Field as DataclassField
from typing import List, Type, Tuple, Dict, Union, get_origin, get_args, Any
from uuid import UUID

from pymnesia.core.entities.entity_cls_conf import EntityClsConf
from pymnesia.core.entities.field import UNDEFINED, Field
from pymnesia.core.entities.entity import Entity
from pymnesia.core.entities.registry import DEFAULT_E_CLASSES_REGISTRY
from pymnesia.core.entities.registry.exceptions.missing_primary_key import MissingPrimaryKeyException
from pymnesia.core.entities.registry.exceptions.missing_tablename import MissingTablenameException
from pymnesia.core.entities.relations import Relation
from pymnesia.core.entities.entity_resolver import EntityClassResolver


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

        _validate_entity_cls_declaration(attrs=attrs)

        tablename = attrs["__tablename__"]
        conf = EntityClsConf()

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
                    one_to_many_relation = _which_one_to_many_relation(typed_attr=field_type)
                    relation = field_type
                    if one_to_many_relation:
                        relation = one_to_many_relation
                        field_as_attr.relation_type = "one_to_many"
                    relations[relation] = field_as_attr
                    field_as_attr.is_owner = True
                    _add_foreign_key_to_fields(
                        relation_name=field_name,
                        fields=fields,
                        is_nullable=field_as_attr.is_nullable,
                        relation_type=field_as_attr.relation_type,
                    )
                    relation_fields[relation] = field_name
            else:
                one_to_many_relation = _which_one_to_many_relation(typed_attr=field_type)
                if one_to_many_relation:
                    relations[one_to_many_relation] = Relation(
                        reverse=tablename[0:-1],
                        relation_type="one_to_many",
                        is_owner=True,
                    )
                    relation_fields[one_to_many_relation] = field_name
                    _add_foreign_key_to_fields(
                        relation_name=field_name,
                        fields=fields,
                        is_nullable=True,
                        relation_type="one_to_many",
                    )
                elif issubclass(field_type, Entity):
                    relations[field_type] = Relation(reverse=tablename[0:-1], is_owner=True)
                    _add_foreign_key_to_fields(
                        relation_name=field_name,
                        fields=fields,
                        is_nullable=True,
                        relation_type="one_to_one",
                    )
                    relation_fields[field_type] = field_name
                else:
                    fields.append((
                        field_name,
                        field_type
                    ))

        cls_resolver = DEFAULT_E_CLASSES_REGISTRY.register(
            _make_entity_dataclass(
                name=name,
                tablename=tablename,
                fields=fields,
                conf=conf,
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


def empty_list_factory() -> List:
    """Used as an alternative for lambda: [], since lambdas are compared by reference and hence cannot be tested.

    :return: A empty list.
    """
    return []


def _make_relations(
        relations: Dict[EntityClassResolver, Relation],
        cls_resolver: EntityClassResolver,
        relation_fields: Dict[EntityClassResolver, str],
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

    for relation, relation_field in relations.items():
        reverse_relation_type = "one_to_one"
        if relation_field.relation_type == "one_to_many":
            reverse_relation_type = "many_to_one"
        relation_current_fields = _extract_entity_cls_fields(relation)
        _add_foreign_key_to_fields(
            relation_name=relation_field.reverse,
            fields=relation_current_fields,
            is_nullable=False,
            relation_type=reverse_relation_type,
        )
        _add_relation_to_fields(
            relation_name=relation_field.reverse,
            relation=cls_resolver,
            fields=relation_current_fields,
            is_nullable=True,
            relation_type=reverse_relation_type,
        )
        relation_new_cls = _make_entity_dataclass(
            name=relation.__name__,
            tablename=relation.__tablename__,
            fields=sorted(
                relation_current_fields,
                key=lambda e: e[2].default == MISSING and e[2].default == MISSING,
                reverse=True,
            ),
            conf=relation.__conf__,
        )
        relation.update_entity_cls(relation_new_cls)
        _add_relation_to_fields(
            relation_name=relation_fields[relation],
            relation=relation,
            fields=cls_resolver_current_fields,
            is_nullable=True,
            relation_type=relation_field.relation_type,
        )
        _add_relation_to_entity_cls_conf(
            conf=cls_resolver.__conf__,
            relation=relation,
            relation_name=relation_fields[relation],
            relation_field=relation_field,
            relation_type=relation_field.relation_type,
        )
        reverse = relation_new_cls.__tablename__[0:-1]
        if relation_field.relation_type == "one_to_many":
            reverse = relation_new_cls.__tablename__
        _add_relation_to_entity_cls_conf(
            conf=relation_new_cls.__conf__,
            relation=cls_resolver,
            relation_name=relation_field.reverse,
            relation_field=Relation(
                reverse=reverse,
                relation_type=reverse_relation_type,
            ),
            relation_type=reverse_relation_type,
        )

    updated_entity_cls = _make_entity_dataclass(
        name=cls_resolver.__name__,
        tablename=tablename,
        fields=cls_resolver_current_fields,
        conf=cls_resolver.__conf__,
    )
    cls_resolver.update_entity_cls(updated_entity_cls)


def _make_entity_dataclass(
        name: str,
        tablename: str,
        fields: List[Tuple],
        conf: EntityClsConf,
) -> Type[Entity]:
    """Makes a dataclass from entity class parameters.

    :param name: The entity class name
    :param tablename: The table name under which the entity should be registered
    :param fields: The fields to create for the entity dataclass
    :param conf:
    :return: A entity dataclass
    """
    entity_cls = make_dataclass(name, fields, bases=(Entity,))
    entity_cls.__tablename__ = tablename
    entity_cls.__conf__ = conf

    # noinspection PyTypeChecker
    return entity_cls


def _add_relation_to_entity_cls_conf(
        conf: EntityClsConf,
        relation,
        relation_name: str,
        relation_field: Relation,
        relation_type: str,
):
    """Adds a relation to an entity class configuration.
    Procedural function that mutates a configuration.

    :param conf: The configuration to add the relation to.
    :param relation: The class resolver of the relation to add.
    :param relation_name: The relation name, meaning the property declared in the relation owner.
    :param relation_field: The relation field to add to the configuration.
    :param relation_type:
    :return: None
    """
    relation_field.entity_cls_resolver = relation
    relation_field.key = _build_foreign_key_name(relation_name=relation_name, relation_type=relation_type)
    conf.relations[relation_name] = relation_field


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


def _add_foreign_key_to_fields(
        relation_name: str,
        fields: List,
        is_nullable: bool,
        relation_type: str,
):
    """Adds a foreign key to an entity class.
    Procedural function that mutates fields.

    :param relation_name: The name of the relation from which the foreign key should be built and added.
    :param fields: The list of fields instance to which the foreign key should be added.
    :param is_nullable: Wether the relation is nullable or not.
    :param relation_type: Wether the relation is nullable or not.
    """
    foreign_key_type = UUID
    if relation_type == "one_to_many":
        foreign_key_type = List[foreign_key_type]
    fields.append((
        _build_foreign_key_name(
            relation_name=relation_name,
            relation_type=relation_type
        ),
        foreign_key_type,
        field(**_build_relation_dataclass_field_args(  # pylint: disable=invalid-field-call
            is_nullable=is_nullable,
            relation_type=relation_type,
        ))
    ))


def _add_relation_to_fields(
        relation_name: str,
        relation: EntityClassResolver,
        fields: List,
        is_nullable: bool,
        relation_type: str,
):
    """Adds a foreign key to an entity class.
    Procedural function that mutates fields.

    :param relation_name: The name of the relation from which the foreign key should be built and added.
    :param relation:
    :param fields: The list of fields instance to which the foreign key should be added.
    :param is_nullable:
    :param relation_type:
    """
    if relation_type == "one_to_many":
        relation = List[relation]
    fields.append(
        (
            relation_name,
            relation,
            field(**_build_relation_dataclass_field_args(  # pylint: disable=invalid-field-call
                is_nullable=is_nullable,
                relation_type=relation_type,
            ))
        )
    )


def _build_relation_dataclass_field_args(
        is_nullable: bool,
        relation_type: str,
) -> dict:
    """Builds the arguments for dataclass field of a relation.

    :param is_nullable: Whether the relation is nullable or not.
    :param relation_type: The type of the relation (one_to_one, one_to_many)
    :return: A dictionary containing the arguments to be used.
    """
    field_args = {}

    default = None if is_nullable and relation_type != "one_to_many" else MISSING
    default_factory = MISSING if relation_type != "one_to_many" else empty_list_factory
    if default is not MISSING:
        field_args["default"] = default
    if default_factory is not MISSING:
        field_args["default_factory"] = default_factory

    return field_args


def _which_one_to_many_relation(typed_attr: Any) -> Union[EntityClassResolver, None]:
    """Determines the entity class resolver from a typed 'one to many' relation.

    :param typed_attr: The typed attribute to determine the entity class resolver from.
    :return: A entity class resolver if the provided typed_attr is a list else None
    """
    if get_origin(typed_attr) == list:
        typing_args = get_args(typed_attr)
        return typing_args[0]

    return None


def _build_foreign_key_name(
        relation_name: str,
        relation_type: str,
) -> str:
    """Builds a foreign key name, based on a relation name.

    :param relation_name: The relation name from which to build the foreign key name.
    :return: A built foreign key name.
    """
    if relation_type == "one_to_many":
        return relation_name[0:-1] + "_ids"
    return relation_name + "_id"


def _validate_entity_cls_declaration(attrs: Dict):
    """Validates that an entity class was correctly required.

    :param attrs: The attributes of the declared entity class.
    :return: None
    """
    if "__tablename__" not in attrs.keys():
        raise MissingTablenameException

    if "id" not in attrs["__annotations__"].keys():
        raise MissingPrimaryKeyException
