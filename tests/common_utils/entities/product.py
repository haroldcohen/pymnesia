"""Provides with storage model InMemoryProduct.
"""
from dataclasses import dataclass, field
from uuid import UUID

from pymnesia.registry import registry

__all__ = ["InMemoryProduct"]


@registry.entity(table_name="products")
@dataclass
class InMemoryProduct:
    id: UUID

    name: str = field(default="Generic product name")
