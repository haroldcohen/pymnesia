"""Provides with relations testing types.
"""
from typing import Optional, List
from dataclasses import dataclass

from pymnesia.entities.entity_resolver import EntityClassResolver
from pymnesia.entities.relations import Relation
from tests.common_utils.helpers.types import FieldsConf

__all__ = ["RelatedEntityClassesParams", "RelatedEntityClsParams"]


@dataclass()
class RelatedEntityClsParams:
    """Stores data to create relations for an entity class.
    """
    name: str

    table_name: str

    single_form: str

    fields_conf: FieldsConf

    cls_resolver: Optional[EntityClassResolver]

    relation_type: str

    owner_rel_api: Optional[Relation]


RelatedEntityClassesParams = List[RelatedEntityClsParams]
