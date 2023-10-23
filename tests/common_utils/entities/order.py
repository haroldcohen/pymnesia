"""Provides with storage model InMemoryProduct.
"""
from dataclasses import dataclass
from uuid import UUID

from pymnesia.registry import registry

__all__ = ["InMemoryOrder"]


@registry.entity(table_name="orders")
@dataclass
class InMemoryOrder:
    id: UUID
