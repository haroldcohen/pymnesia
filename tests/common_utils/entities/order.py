"""Provides with storage model InMemoryProduct.
"""
from uuid import UUID

from pymnesia.entities.field import Field
from pymnesia.entities.registry import registry

__all__ = ["InMemoryOrder"]


@registry.entity(table_name="orders")
class InMemoryOrder:
    id: UUID

    total_amount: int = Field(default=0)

    vat_not_included_amount: int = Field(default=0)
