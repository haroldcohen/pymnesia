"""Provides with storage model InMemoryInvoice.
"""
from uuid import UUID

from pymnesia.entities.base import DeclarativeBase

__all__ = ["InMemoryProforma"]

from pymnesia.entities.field import Field


class InMemoryProforma(DeclarativeBase):
    __tablename__ = "proformas"

    id: UUID

    total_with_vat: float = Field(default=0)
