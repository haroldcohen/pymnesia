"""Provides with storage model InMemoryProductSpec.
"""
from uuid import UUID

from pymnesia.entities.base import DeclarativeBase

__all__ = ["InMemoryProductSpec"]


class InMemoryProductSpec(DeclarativeBase):
    __tablename__ = "product_specs"

    id: UUID
