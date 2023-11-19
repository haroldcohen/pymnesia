"""Provides with assertion related utility functions.
"""
from dataclasses import MISSING
from typing import Dict, List, get_origin, get_args
from uuid import UUID

from pymnesia.entities.entity import Entity
from pymnesia.entities.entity_cls_conf import EntityClsConf
from pymnesia.entities.entity_resolver import EntityClassResolver
from pymnesia.entities.field import UNDEFINED
from pymnesia.entities.meta import empty_list_factory
from pymnesia.entities.relations import Relation
from tests.common_utils.helpers.make import FieldsConf, is_relation_field_conf, is_type_and_field_tuple

__all__ = [
    "build_expected_entity_cls_conf",
    "build_expected_entity_cls_attributes",
    "build_expected_entity_cls_attributes_with_relations",
    "build_expected_entity_cls_fields",
]


def build_expected_entity_cls_conf(
        entity_cls_resolver: EntityClassResolver,
        fields_conf: FieldsConf,
        owned_relations: List[str],
) -> EntityClsConf:
    """Builds an expected entity class conf.

    :param entity_cls_resolver:
    :param fields_conf:
    :param owned_relations:
    :return:
    """
    expected_entity_cls_conf = EntityClsConf()
    for field_name, field_conf in fields_conf.items():
        origin_type = get_origin(field_conf)
        if is_type_and_field_tuple(field_conf):
            if is_relation_field_conf(field_conf):
                expected_relation_args = {
                    "key": field_name + "_id",
                    "entity_cls_resolver": entity_cls_resolver.__annotations__[field_name],
                    "is_owner": field_name in owned_relations,
                }
                if isinstance(field_conf[0], EntityClassResolver):
                    expected_relation_args["reverse"] = build_expected_reverse_from_table_name(
                        table_name=entity_cls_resolver.__tablename__,
                    )
                if get_origin(field_conf[0]) == list:
                    typing_args = get_args(field_conf[0])
                    expected_relation_args = {
                        "relation_type": "one_to_many",
                        "key": field_name[0:-1] + "_ids",
                        "entity_cls_resolver": typing_args[0],
                        "is_owner": field_name in owned_relations,
                        "reverse": build_expected_reverse_from_table_name(
                            table_name=entity_cls_resolver.__tablename__,
                        ),
                    }
                if isinstance(field_conf[1], Relation):
                    expected_relation_args["reverse"] = field_conf[1].reverse
                    expected_relation_args["is_nullable"] = field_conf[1].is_nullable
                expected_entity_cls_conf.relations[field_name] = Relation(**expected_relation_args)
        elif origin_type == list:
            typing_args = get_args(field_conf)
            expected_relation_args = {
                "relation_type": "one_to_many",
                "key": field_name[0:-1] + "_ids",
                "entity_cls_resolver": typing_args[0],
                "is_owner": field_name in owned_relations,
                "reverse": build_expected_reverse_from_table_name(
                    table_name=entity_cls_resolver.__tablename__,
                ),
            }
            expected_entity_cls_conf.relations[field_name] = Relation(**expected_relation_args)
        elif issubclass(field_conf, Entity):
            expected_relation_args = {
                "key": field_name + "_id",
                "entity_cls_resolver": entity_cls_resolver.__annotations__[field_name],
                "is_owner": field_name in owned_relations,
                "reverse": build_expected_reverse_from_table_name(
                    table_name=entity_cls_resolver.__tablename__,
                ),
            }
            expected_entity_cls_conf.relations[field_name] = Relation(**expected_relation_args)

    return expected_entity_cls_conf


def build_expected_reverse_from_table_name(table_name: str) -> str:
    """Builds an expected reverse property from a table name.

    :param table_name: The table name from which to build the reverse property.
    :return: A reverse property
    """
    return table_name[0:-1]


def build_expected_entity_cls_attributes(fields_conf: FieldsConf) -> Dict:
    """Builds a dictionary of expected attributes from a fields conf.

    :param fields_conf:
    :return:
    """
    expected_attrs = {}
    for field_name, field_conf in fields_conf.items():
        if is_type_and_field_tuple(field_conf):
            expected_attrs[field_name] = field_conf[0]
        else:
            expected_attrs[field_name] = field_conf

    return expected_attrs


def build_expected_entity_cls_attributes_with_relations(
        entity_cls_resolver: EntityClassResolver,
        fields_conf: FieldsConf,
) -> Dict:
    """Builds a dictionary of expected attributes from a fields conf with relations.

    :param entity_cls_resolver:
    :param fields_conf:
    :return:
    """
    expected_attrs = build_expected_entity_cls_attributes(fields_conf=fields_conf)

    for relation_name, relation in entity_cls_resolver.__conf__.relations.items():
        expected_relation_foreign_key_type = UUID
        if relation.relation_type == "one_to_many":
            expected_relation_foreign_key_type = List[UUID]
        expected_attrs[build_expected_foreign_key_name(
            relation_name=relation_name,
            relation_type=relation.relation_type,
        )] = expected_relation_foreign_key_type
        expected_relation_attr = relation.entity_cls_resolver
        if relation.relation_type == "one_to_many":
            expected_relation_attr = List[expected_relation_attr]
        expected_attrs[relation_name] = expected_relation_attr

    return expected_attrs


def build_expected_entity_cls_fields(
        entity_cls_resolver: EntityClassResolver,
        fields_conf: FieldsConf,
) -> List:
    """Builds a list of expected dataclass fields.

    :param entity_cls_resolver:
    :param fields_conf:
    :return:
    """
    expected_fields = []
    for field_name, field_conf in fields_conf.items():
        expected = {"name": field_name, "type": field_conf, "default": MISSING, "default_factory": MISSING}
        origin_type = get_origin(field_conf)
        if is_type_and_field_tuple(field_conf):
            if not is_relation_field_conf(field_conf):
                field = field_conf[1]
                expected["type"] = field_conf[0]
                expected["default"] = field.default if field.default is not UNDEFINED else MISSING
                expected["default_factory"] = field.default_factory \
                    if field.default_factory is not UNDEFINED else MISSING
            else:
                expected["type"] = field_conf[0]
                is_owner = entity_cls_resolver.__conf__.relations[field_name].is_owner
                expected["default"] = None
                expected_foreign_key = build_expected_foreign_key_field(
                    relation_name=field_name,
                    is_owner=is_owner,
                    relation_type="one_to_one",
                )
                if isinstance(field_conf[1], Relation):
                    if get_origin(field_conf[0]) == list:
                        expected["type"] = field_conf[0]
                        expected["default"] = MISSING
                        expected["default_factory"] = empty_list_factory
                        expected_foreign_key = build_expected_foreign_key_field(
                            relation_name=field_name,
                            relation_type="one_to_many",
                            is_owner=True,
                        )
                        expected_fields.append(expected_foreign_key)
                    else:
                        expected["default"] = None
                        expected_foreign_key["default"] = None if field_conf[1].is_nullable and is_owner else MISSING
                        expected_fields.append(expected_foreign_key)
        elif origin_type == list:
            expected["type"] = field_conf
            expected["default_factory"] = empty_list_factory
            expected_foreign_key = build_expected_foreign_key_field(
                relation_name=field_name,
                relation_type="one_to_many",
                is_owner=True,
            )
            expected_fields.append(expected_foreign_key)
        elif issubclass(field_conf, Entity):
            is_owner = entity_cls_resolver.__conf__.relations[field_name].is_owner
            expected["default"] = None if is_owner else MISSING
            expected_foreign_key = build_expected_foreign_key_field(
                relation_name=field_name,
                is_owner=is_owner,
                relation_type="one_to_one",
            )
            expected_fields.append(expected_foreign_key)
        expected_fields.append(expected)

    return expected_fields


def build_expected_foreign_key_field(
        relation_name: str,
        relation_type: str,
        is_owner: bool,
) -> Dict:
    """Builds a foreign key field based on a relation name and ownership.

    :param relation_name: The relation's name (could be reverse as well).
    :param relation_type:
    :param is_owner: Whether the relation is owned by the entity or not.
    :return: A dictionary containing the expected field values.
    """
    expected_foreign_key_type = UUID
    if relation_type == "one_to_many":
        expected_foreign_key_type = List[expected_foreign_key_type]
    default = None if is_owner and relation_type != "one_to_many" else MISSING
    default_factory = MISSING if relation_type == "one_to_one" else empty_list_factory
    return {
        "name": build_expected_foreign_key_name(
            relation_name=relation_name,
            relation_type=relation_type,
        ),
        "type": expected_foreign_key_type,
        "default": default,
        "default_factory": default_factory,
    }


def build_expected_foreign_key_name(
        relation_name: str,
        relation_type: str,
) -> str:
    """Builds a foreign key name based on a relation name.

    :param relation_name: The relation's name (could be reverse as well).
    :param relation_type:
    :return: A foreign key name
    """
    if relation_type == "one_to_many":
        return relation_name[0:-1] + "_ids"
    return relation_name + "_id"
