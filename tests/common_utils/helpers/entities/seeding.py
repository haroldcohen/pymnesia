"""Provides with seeding functions.
"""
from typing import Callable, Dict, List, Union, Any

from pymnesia.entities.entity import Entity

__all__ = [
    "generate_seeds",
    "generate_seed",
    "water_seeds",
    "generate_rel_seeds",
    "generate_entities",
]


def generate_seeds(num: int, use: Dict[str, Union[Any, Callable]]) -> List[Dict]:
    """Generates data to seed entities.

    :param num: The number of entities to seed.
    :param use: The values to use for seeding.
    :return: A list of seeds.
    """
    seeds_ = []
    for i in range(0, num):  # pylint: disable=unused-variable
        seed_props = generate_seed(use=use)
        seeds_.append(seed_props)

    return seeds_


def generate_seed(use: Dict[str, Union[Any, Callable]]) -> Dict:
    """Generates a seed.

    :param use: The values to use for seeding.
    :return: A dictionary to be used as seed.
    """
    seed_props = {}
    for field_name, use_value in use.items():
        if isinstance(use_value, Callable):
            seed_props[field_name] = use_value()
        else:
            seed_props[field_name] = use_value

    return seed_props


def generate_rel_seeds(use: Dict[str, Callable]) -> Dict:
    """Generates a relation seed.

    :param use:
    :return:
    """
    rel_seeds = {}
    for rel_name, rel_generator in use.items():
        rel_seeds[rel_name] = rel_generator()

    return rel_seeds


def seed_rels(
        seeded_entity: Entity,
        entity_cls,
        rel_seeds: Dict,
) -> List:
    """Seed relations.

    :param seeded_entity:
    :param entity_cls:
    :param rel_seeds:
    :return:
    """
    seeded_rels = []
    for rel_name, rel_seed in rel_seeds.items():
        rel_conf = entity_cls.__conf__.relations[rel_name]
        rel_seed[rel_conf.reverse + "_id"] = seeded_entity.id
        rel_entity = rel_conf.entity_cls_resolver(**rel_seed)
        setattr(seeded_entity, rel_name, rel_entity)
        setattr(seeded_entity, rel_conf.key, rel_entity.id)
        seeded_rels.append(rel_entity)

    return seeded_rels


def generate_entities(
        seeds: List[Dict],
        entity_cls,
):
    """Generates entities based on seeds.

    :param seeds: The seeds to use.
    :param entity_cls: The entity class to seed.
    :return: A tuple of seeded entities and related entities.
    """
    seeded = []
    seeded_rels = []
    for seed in seeds:
        rels = seed.pop("rels", {})
        seeded_entity = entity_cls(**seed)
        seeded_rels.extend(seed_rels(seeded_entity=seeded_entity, entity_cls=entity_cls, rel_seeds=rels))
        seeded.append(seeded_entity)
    return seeded, seeded_rels


def water_seeds(
        seeds: List,
        unit_of_work,
):
    """Saves entity seeds.

    :param seeds: The seeds to save.
    :param unit_of_work: The unit of work in which entities should be saved.
    :return: None
    """
    for seed in seeds:
        unit_of_work.save_entity(seed)
