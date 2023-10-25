"""Provides with storage model InMemoryProduct.
"""
from dataclasses import dataclass, field
from uuid import UUID

from pymnesia.registry import registry

__all__ = ["InMemoryOrder"]


@registry.entity(table_name="orders")
@dataclass
class InMemoryOrder:
    id: UUID

    total_amount: int = field(default=0)

    vat_not_included_amount: int = field(default=0)
