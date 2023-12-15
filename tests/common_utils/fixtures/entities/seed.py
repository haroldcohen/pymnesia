"""Provides with fixtures to seed entities.
"""
from typing import List, Dict

import pytest

from pymnesia.entities.entity_resolver import EntityClassResolver
from tests.common_utils.helpers.entities.seeding import generate_entities
from tests.common_utils.helpers.entities.seeding import water_seeds

__all__ = [
    "expected_seeds",
    "seeds",
    "do_water_seeds",
    "seeded_entities",
]


# pylint: disable=redefined-outer-name

@pytest.fixture()
def expected_seeds(request) -> List:
    if hasattr(request, "param"):
        return request.param
    return []


@pytest.fixture()
def seeds(request) -> List:
    if hasattr(request, "param"):
        return request.param
    return []


@pytest.fixture()
def do_water_seeds(request) -> bool:
    if hasattr(request, "param"):
        return request.param
    return True


@pytest.fixture()
def seeded_entities(
        entity_cls: EntityClassResolver,
        seeds: List[Dict],
        expected_seeds: List[Dict],
        expected_entities: List,
        unit_of_work,
        transaction,
        do_water_seeds: bool,
) -> List:
    """Seed and saves entities and expected entities.

    :param entity_cls: The entity class (or resolver) to use for seeding.
    :param seeds: The seeds to seed.
    :param expected_seeds: The expected seeds to seed.
    :param expected_entities: An empty list that will be mutated with expected entities.
    :param unit_of_work: The unit of work to use for seeding.
    :param transaction: The transaction to use for seeding.
    :param do_water_seeds: Whether the seeded entities should be saved in the unit of work or not.
    :return: A list of seeded entities, relations excluded.
    """
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
    if do_water_seeds:
        water_seeds(seeds=expected_seeds, unit_of_work=unit_of_work)
        water_seeds(seeds=expected_rel_seeds, unit_of_work=unit_of_work)
        water_seeds(seeds=entity_seeds, unit_of_work=unit_of_work)
        water_seeds(seeds=rel_seeds, unit_of_work=unit_of_work)
        transaction.commit()

    return seeded
