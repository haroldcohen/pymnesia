"""Provides with a class to store an entity class configuration.
"""
from dataclasses import dataclass, field
from typing import Dict


@dataclass()
class EntityClsConf:
    relations: Dict = field(default_factory=lambda: {})

    fields: Dict = field(default_factory=lambda: {})
