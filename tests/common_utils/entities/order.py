"""Provides with storage model InMemoryProduct.
"""
from uuid import UUID

from pymnesia.entities.base import DeclarativeBase
from pymnesia.entities.field import Field

__all__ = ["InMemoryOrder"]


class InMemoryOrder(DeclarativeBase):
    __tablename__ = "orders"

    id: UUID

    total_amount: int = Field(default=0)

    vat_not_included_amount: int = Field(default=0)
