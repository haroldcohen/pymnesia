"""Provides with assertion related utility functions.
"""
from dataclasses import MISSING
from typing import Dict, List
from uuid import UUID

from pymnesia.entities.entity import Entity
from pymnesia.entities.entity_cls_conf import EntityClsConf
from pymnesia.entities.entity_resolver import EntityClassResolver
from pymnesia.entities.field import UNDEFINED
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
        if is_type_and_field_tuple(field_conf):
            if is_relation_field_conf(field_conf):
                expected_relation_args = {
                    "key": field_name + "_id",
                    "entity_cls_resolver": entity_cls_resolver.__annotations__[field_name],
                    "is_owner": field_name in owned_relations,
                }
                if isinstance(field_conf[0], EntityClassResolver):
                    expected_relation_args["reverse"] = entity_cls_resolver.__tablename__[0:-1]
                if isinstance(field_conf[1], Relation):
                    expected_relation_args["reverse"] = field_conf[1].reverse
                    expected_relation_args["is_nullable"] = field_conf[1].is_nullable
                expected_entity_cls_conf.relations[field_name] = Relation(**expected_relation_args)
        elif issubclass(field_conf, Entity):
            expected_relation_args = {
                "key": field_name + "_id",
                "entity_cls_resolver": entity_cls_resolver.__annotations__[field_name],
                "is_owner": field_name in owned_relations,
                "reverse": entity_cls_resolver.__tablename__[0:-1],
            }
            expected_entity_cls_conf.relations[field_name] = Relation(**expected_relation_args)

    return expected_entity_cls_conf


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
):
    """Builds a dictionary of expected attributes from a fields conf with relations.

    :param entity_cls_resolver:
    :param fields_conf:
    :return:
    """
    expected_attrs = build_expected_entity_cls_attributes(fields_conf=fields_conf)

    for relation_name, relation in entity_cls_resolver.__conf__.relations.items():
        expected_attrs[relation_name + "_id"] = UUID
        expected_attrs[relation_name] = relation.entity_cls_resolver

    return expected_attrs


def build_expected_entity_cls_fields(
        entity_cls_resolver: EntityClassResolver,
        fields_conf: FieldsConf,
):
    """Builds a list of expected dataclass fields.

    :param entity_cls_resolver:
    :param fields_conf:
    :return:
    """
    expected_fields = []
    for field_name, field_conf in fields_conf.items():
        expected = {"name": field_name, "type": field_conf, "default": MISSING, "default_factory": MISSING}
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
                expected_foreign_key = {
                    "name": field_name + "_id",
                    "type": UUID,
                    "default": None if is_owner else MISSING,
                    "default_factory": MISSING
                }
                if isinstance(field_conf[1], Relation):
                    expected["default"] = None
                    expected_foreign_key["default"] = None if field_conf[1].is_nullable and is_owner else MISSING
                    expected_fields.append(expected_foreign_key)
        elif issubclass(field_conf, Entity):
            is_owner = entity_cls_resolver.__conf__.relations[field_name].is_owner
            expected["default"] = None if is_owner else MISSING
            # expected["default"] = None if is_owner else MISSING
            expected_foreign_key = {
                "name": field_name + "_id",
                "type": UUID,
                "default": None if is_owner else MISSING,
                "default_factory": MISSING
            }
            expected_fields.append(expected_foreign_key)
        expected_fields.append(expected)

    return expected_fields
