"""Provides with dynamically constructed entity classes.
"""
from typing import Dict, Union, Tuple

from pymnesia.entities.field import Field
from pymnesia.entities.relations import Relation

__all__ = ["FieldConf", "FieldsConf"]

FieldConf = Union[type, Tuple[type, Union[Field, Relation]]]

FieldsConf = Dict[str, FieldConf]
