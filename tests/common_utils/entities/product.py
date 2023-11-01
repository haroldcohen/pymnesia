"""Provides with storage model InMemoryProduct.
"""
from uuid import UUID

from pymnesia.entities.field import Field
from pymnesia.entities.base import DeclarativeBase

__all__ = ["InMemoryProduct"]


class InMemoryProduct(DeclarativeBase):
    __tablename__ = "products"

    id: UUID

    name: str = Field(default="Generic product name")
