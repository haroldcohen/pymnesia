"""Provides with storage model InMemoryProduct.
"""
from uuid import UUID

from pymnesia.entities.base import DeclarativeBase
from pymnesia.entities.field import Field
from pymnesia.api.entities import relation
from tests.common_utils.entities.invoice import InMemoryInvoice

__all__ = ["InMemoryOrder"]

from tests.common_utils.entities.proforma import InMemoryProforma


class InMemoryOrder(DeclarativeBase):
    __tablename__ = "orders"

    id: UUID

    total_amount: int = Field(default=0)

    vat_not_included_amount: int = Field(default=0)

    invoice: InMemoryInvoice = relation(reverse="order")

    proforma: InMemoryProforma = relation(reverse="order")
