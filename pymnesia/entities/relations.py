"""Provides with relation fields.
"""
from dataclasses import dataclass, field

from pymnesia.entities.entity_cls_resolver_interface import EntityClassResolverInterface


@dataclass()
class Relation:

    reverse: str

    relation_type: str = field(default="one_to_one")

    is_nullable: bool = field(default=True)

    entity_cls_resolver: EntityClassResolverInterface = field(default=None)

    key: str = field(default=None)

    is_owner: bool = field(default=False)
