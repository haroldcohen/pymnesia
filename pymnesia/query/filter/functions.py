import datetime
import re
from typing import Union, Any, Iterable

from pymnesia.query.filter.registry import register_filter_func

__all__ = ["filter_eq", "filter_not", "filter_greater_than", "filter_greater_than_or_equal", "filter_less_than",
           "filter_less_than_or_equal", "filter_match", "filter_in"]


@register_filter_func(filter_name="eq")
def filter_eq(entities: Iterable, field: str, value: Any) -> filter:
    """
    Filters entities whose field is equal to a given value.
    :param entities: The entities to filter.
    :param field: The field to compare.
    :param value: The value to use for comparison.
    :return: An iterable (filter) containing the filtered results.
    """
    return filter(lambda e: getattr(e, field) == value, entities)


@register_filter_func(filter_name="not")
def filter_not(entities: Iterable, field: str, value: Any) -> filter:
    """
    Filters entities whose field is not equal to a given value.
    :param entities: The entities to filter.
    :param field: The field to compare.
    :param value: The value to use for comparison.
    :return: An iterable (filter) containing the filtered results.
    """
    return filter(lambda e: getattr(e, field) != value, entities)


@register_filter_func(filter_name="gt")
def filter_greater_than(entities: Iterable, field: str, value: Union[str, int, type(datetime)]) -> filter:
    """
    Filters entities whose field is greater than a given value.
    :param entities: The entities to filter.
    :param field: The field to compare.
    :param value: The value to use for comparison.
    :return: An iterable (filter) containing the filtered results.
    """
    return filter(lambda e: getattr(e, field) > value, entities)


@register_filter_func(filter_name="gte")
def filter_greater_than_or_equal(entities: Iterable, field: str, value: Union[str, int, type(datetime)]) -> filter:
    """
    Filters entities whose field is greater than or equal to a given value.
    :param entities: The entities to filter.
    :param field: The field to compare.
    :param value: The value to use for comparison.
    :return: An iterable (filter) containing the filtered results.
    """
    return filter(lambda e: getattr(e, field) >= value, entities)


@register_filter_func(filter_name="lt")
def filter_less_than(entities: Iterable, field: str, value: Union[str, int, type(datetime)]) -> filter:
    """
    Filters entities whose field is less than a given value.
    :param entities: The entities to filter.
    :param field: The field to compare.
    :param value: The value to use for comparison.
    :return: An iterable (filter) containing the filtered results.
    """
    return filter(lambda e: getattr(e, field) < value, entities)


@register_filter_func(filter_name="lte")
def filter_less_than_or_equal(entities: Iterable, field: str, value: Union[str, int, type(datetime)]) -> filter:
    """
    Filters entities whose field is less than or equal to a given value.
    :param entities: The entities to filter.
    :param field: The field to compare.
    :param value: The value to use for comparison.
    :return: An iterable (filter) containing the filtered results.
    """
    return filter(lambda e: getattr(e, field) <= value, entities)


@register_filter_func(filter_name="match")
def filter_match(entities: Iterable, field: str, value: re.Pattern) -> filter:
    """
    Filters entities whose field matches a given value, based on a regular expression, and where re.match is used for
    evaluation.
    :param entities: The entities to filter.
    :param field: The field to compare.
    :param value: The value to use for comparison.
    :return: An iterable (filter) containing the filtered results.
    """
    return filter(lambda e: re.match(value, getattr(e, field)), entities)


@register_filter_func(filter_name="in")
def filter_in(entities: Iterable, field: str, value: list) -> filter:
    """
    Filters entities whose field's value is in a range of values.
    :param entities: The entities to filter.
    :param field: The field to compare.
    :param value: The value to use for comparison.
    :return: An iterable (filter) containing the filtered results.
    """
    return filter(lambda e: getattr(e, field) in value, entities)
