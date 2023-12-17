from typing import Any, Iterable
from itertools import groupby

from pymnesia.core.entities.relations import Relation
from pymnesia.core.query.filter.registry import register_filter_func

__all__ = ["filter_rel_eq"]


@register_filter_func(filter_name="eq", relational=True)
def filter_rel_eq(entities: Iterable, field: str, value: Any, unit_of_work, relation: Relation) -> filter:
    """Filters entities whose field is equal to a given value.
    :param entities: The entities to filter.
    :param field: The field to compare.
    :param value: The value to use for comparison.
    :param unit_of_work:
    :param relation:
    :return: An iterable (filter) containing the filtered results.
    """
    base_query = getattr(unit_of_work.query(), relation.entity_cls_resolver.__tablename__)()
    rels = base_query.where({field: value}).fetch()

    if relation.relation_type == "one_to_one":
        filtered_rel_ids = [rel.id for rel in rels]

        return filter(lambda e: getattr(e, relation.key) in filtered_rel_ids, entities)

    reverse_foreign_key_name = relation.reverse + "_id"
    grouped_filtered_rels = groupby(rels, key=lambda e: getattr(e, reverse_foreign_key_name))
    filtered_ids = []
    for key, group in grouped_filtered_rels:  # pylint: disable=unused-variable
        filtered_ids.append(key)

    return filter(lambda e: e.id in filtered_ids, entities)
