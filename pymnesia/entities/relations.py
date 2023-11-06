"""Provides with relation fields.
"""
from dataclasses import dataclass, field

from pymnesia.entities.entity_resolver import EntityClassResolver


@dataclass()
class Relation:
    reverse: str

    is_nullable: bool = field(default=True)

    entity_cls_resolver: EntityClassResolver = field(default=None)

    key: str = field(default=None)
