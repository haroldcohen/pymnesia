import re

from pymnesia.composition import curry

FILTER_FUNCTIONS_REGISTRY = {}


def register_filter_func(*, filter_name: str):
    def decorator(func):
        FILTER_FUNCTIONS_REGISTRY[filter_name] = func

        return func

    return decorator


@register_filter_func(filter_name="not")
def filter_not(entities: list, field: str, value):
    return list(filter(lambda e: getattr(e, field) != value, entities))


@register_filter_func(filter_name="gt")
def filter_greater_than(entities: list, field: str, value):
    return list(filter(lambda e: getattr(e, field) > value, entities))


@register_filter_func(filter_name="gte")
def filter_greater_than_or_equal(entities: list, field: str, value):
    return list(filter(lambda e: getattr(e, field) >= value, entities))


@register_filter_func(filter_name="lt")
def filter_less_than(entities: list, field: str, value):
    return list(filter(lambda e: getattr(e, field) < value, entities))


@register_filter_func(filter_name="lte")
def filter_less_than_or_equal(entities: list, field: str, value):
    return list(filter(lambda e: getattr(e, field) <= value, entities))


@register_filter_func(filter_name="match")
def filter_match(entities: list, field: str, value):
    return list(filter(lambda e: re.match(value, getattr(e, field)), entities))


def filter_results(entities: list, clause: dict):
    result = entities
    for condition, value in clause.items():
        split_condition = condition.split("::")
        matched_condition = re.match(r'^(?P<field>\w+)::(?P<operator>\w+)$', condition)
        if matched_condition:
            result = FILTER_FUNCTIONS_REGISTRY[matched_condition.group("operator")](result,
                                                                                    matched_condition.group("field"),
                                                                                    value)
        else:
            result = list(filter(lambda e: getattr(e, split_condition[0]) == value, result))

    return result


curried_filter_results = curry(filter_results)
