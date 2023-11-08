"""Provides with storage model InMemoryInvoice.
"""
from uuid import UUID

from pymnesia.api.entities import relation
from pymnesia.entities.base import DeclarativeBase
from pymnesia.entities.field import Field
from tests.common_utils.entities.proforma import InMemoryProforma

__all__ = ["InMemoryInvoice"]


class InMemoryInvoice(DeclarativeBase):
    __tablename__ = "invoices"

    id: UUID

    number: str = Field(default=None)

    total_with_vat: float = Field(default=0)

    proforma: InMemoryProforma = relation(reverse="invoice")

