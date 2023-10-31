"""Provides with a base class for entities.
"""
from pymnesia.entities.meta import EntityMeta


class BaseEntity(metaclass=EntityMeta):
    """Base class for entities.

    @DynamicAttrs"""

    def __init__(self, **kwargs):
        pass
