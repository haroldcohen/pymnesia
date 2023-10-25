"""Provides with fixtures to populate entities.
"""
import pytest

from pymnesia.transaction.transaction import InMemoryTransaction
from pymnesia.unit_of_work.unit_of_work import UnitOfWork

__all__ = ["populate_entities", "entities", "populate_expected_last"]


@pytest.fixture()
def populate_entities(
        unit_of_work: UnitOfWork,
        transaction: InMemoryTransaction,
        entities,
        expected_entities,
        expected_entity,
        populate_expected_last,
):
    if populate_expected_last:
        for entity in entities:
            unit_of_work.save_entity(entity=entity)
    if expected_entity:
        unit_of_work.save_entity(entity=expected_entity)
    for expected_entity in expected_entities:
        unit_of_work.save_entity(entity=expected_entity)
    if not populate_expected_last:
        for entity in entities:
            unit_of_work.save_entity(entity=entity)

    transaction.commit()


@pytest.fixture()
def entities(request):
    if hasattr(request, "param"):
        return request.param
    return []


@pytest.fixture()
def populate_expected_last(request):
    if hasattr(request, "param"):
        return request.param
    return False
