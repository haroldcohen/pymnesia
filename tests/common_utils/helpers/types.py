"""Provides with dynamically constructed entity classes.
"""
from typing import Dict, Union, Tuple

from pymnesia.core.entities.field import Field
from pymnesia.core.entities.relations import Relation

__all__ = ["FieldConf", "FieldsConf"]

FieldConf = Union[type, Tuple[type, Union[Field, Relation]]]

FieldsConf = Dict[str, FieldConf]
