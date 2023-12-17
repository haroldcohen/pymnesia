"""Provides with relations testing types.
"""
from typing import Optional
from dataclasses import dataclass

from pymnesia.core.entities.entity_resolver import EntityClassResolver
from tests.common_utils.helpers.entities.make.relations.types import RelatedEntityClassesParams
from tests.common_utils.helpers.types import FieldsConf

__all__ = ["EntityClsParams"]


@dataclass()
class EntityClsParams:
    """Stores data to create an entity class.
    """
    name: str

    table_name: str

    fields_conf: FieldsConf

    rel_entity_classes_params: Optional[RelatedEntityClassesParams]

    cls_resolver: Optional[EntityClassResolver] = None
