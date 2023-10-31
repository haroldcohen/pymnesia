"""Provides with storage model InMemoryProduct.
"""
from uuid import UUID

from pymnesia.entities.field import Field
from pymnesia.entities.base import BaseEntity

__all__ = ["InMemoryProduct"]


class InMemoryProduct(BaseEntity):
    __tablename__ = "products"

    id: UUID

    name: str = Field(default="Generic product name")
