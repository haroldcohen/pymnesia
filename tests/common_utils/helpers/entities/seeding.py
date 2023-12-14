"""Provides with seeding functions.
"""
from typing import Callable, Dict, List

from pymnesia.entities.entity import Entity

__all__ = [
    "generate_seeds",
    "generate_seed",
    "seed_entities",
    "generate_rel_seeds",
    "generate_entities",
]


def generate_seeds(num: int, use: dict) -> List[Dict]:
    seeds_ = []
    for i in range(0, num):  # pylint: disable=unused-variable
        seed_props = generate_seed(use=use)
        seeds_.append(seed_props)

    return seeds_


def generate_seed(use: dict) -> Dict:
    seed_props = {}
    for field_name, use_value in use.items():
        if isinstance(use_value, Callable):
            seed_props[field_name] = use_value()
        else:
            seed_props[field_name] = use_value

    return seed_props


def generate_rel_seeds(use: Dict[str, Callable]) -> Dict:
    rel_seeds = {}
    for rel_name, rel_generator in use.items():
        rel_seeds[rel_name] = rel_generator()

    return rel_seeds


def seed_rels(
        seeded_entity: Entity,
        entity_cls,
        rel_seeds: Dict,
) -> List:
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
    seeded = []
    seeded_rels = []
    for seed in seeds:
        rels = seed.pop("rels", {})
        seeded_entity = entity_cls(**seed)
        seeded_rels.extend(seed_rels(seeded_entity=seeded_entity, entity_cls=entity_cls, rel_seeds=rels))
        seeded.append(seeded_entity)
    return seeded, seeded_rels


def seed_entities(
        seeds: List,
        unit_of_work,
):
    for seed in seeds:
        unit_of_work.save_entity(seed)
