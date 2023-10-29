"""Provides with storage model InMemoryProduct.
"""
from uuid import UUID

from pymnesia.entities.field import Field
from pymnesia.entities.registry import registry

__all__ = ["InMemoryProduct"]


@registry.entity(table_name="products")
class InMemoryProduct:
    id: UUID

    name: str = Field(default="Generic product name")
