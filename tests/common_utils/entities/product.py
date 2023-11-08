"""Provides with storage model InMemoryProduct.
"""
from uuid import UUID

from pymnesia.api.entities import relation
from pymnesia.entities.field import Field
from pymnesia.entities.base import DeclarativeBase
from tests.common_utils.entities.product_spec import InMemoryProductSpec

__all__ = ["InMemoryProduct"]


class InMemoryProduct(DeclarativeBase):
    __tablename__ = "products"

    id: UUID

    name: str = Field(default="Generic product name")

    spec: InMemoryProductSpec = relation(reverse="product")
