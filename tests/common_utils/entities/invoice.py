"""Provides with storage model InMemoryInvoice.
"""
from uuid import UUID

from pymnesia.entities.base import DeclarativeBase

__all__ = ["InMemoryInvoice"]

from pymnesia.entities.field import Field


class InMemoryInvoice(DeclarativeBase):
    __tablename__ = "invoices"

    id: UUID

    total_with_vat: float = Field(default=0)

