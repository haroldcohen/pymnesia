"""Provides with fixtures to seed entities.
"""
import pytest

from tests.common_utils.helpers.entities.seeding import generate_entities
from tests.common_utils.helpers.entities.seeding import seed_entities

__all__ = [
    "expected_seeds",
    "seeds",
    "water_seeds",
    "seeded_entities",
]


# pylint: disable=redefined-outer-name

@pytest.fixture()
def expected_seeds(request):
    if hasattr(request, "param"):
        return request.param
    return []


@pytest.fixture()
def seeds(request):
    if hasattr(request, "param"):
        return request.param
    return []


@pytest.fixture()
def water_seeds(request):
    if hasattr(request, "param"):
        return request.param
    return True


@pytest.fixture()
def seeded_entities(
        entity_cls,
        seeds,
        expected_seeds,
        expected_entities,
        unit_of_work,
        transaction,
        water_seeds,
):
    seeded = []
    expected_seeds, expected_rel_seeds = generate_entities(
        seeds=expected_seeds,
        entity_cls=entity_cls,
    )
    seeded.extend(expected_seeds)
    expected_entities.extend(expected_seeds)
    entity_seeds, rel_seeds = generate_entities(
        seeds=seeds,
        entity_cls=entity_cls,
    )
    seeded.extend(entity_seeds)
    if water_seeds:
        seed_entities(seeds=expected_seeds, unit_of_work=unit_of_work)
        seed_entities(seeds=expected_rel_seeds, unit_of_work=unit_of_work)
        seed_entities(seeds=entity_seeds, unit_of_work=unit_of_work)
        seed_entities(seeds=rel_seeds, unit_of_work=unit_of_work)
        transaction.commit()

    return seeded
