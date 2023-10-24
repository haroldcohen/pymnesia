"""Provides with a config class for entities.
"""
from dataclasses import dataclass

__all__ = ["EntityConfig"]


@dataclass
class EntityConfig:
    """Storage class for the entities configurations.
    """

    table_name: str
