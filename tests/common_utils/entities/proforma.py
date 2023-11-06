"""Provides with storage model InMemoryInvoice.
"""
from uuid import UUID

from pymnesia.entities.base import DeclarativeBase

__all__ = ["InMemoryProforma"]


class InMemoryProforma(DeclarativeBase):
    __tablename__ = "proformas"

    id: UUID
