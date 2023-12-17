"""Provides with Query class.
"""
import re
from typing import Callable

from pymnesia.core.composition import runner
from pymnesia.core.query.filter.registry import find_filter_function
from pymnesia.core.query.functions import order_by
from pymnesia.core.query.runner import QueryRunner
from pymnesia.core.query.filter.functions import *  # pylint: disable=wildcard-import,unused-wildcard-import
from pymnesia.core.query.filter.relations import *  # pylint: disable=wildcard-import,unused-wildcard-import

FIELD_OPERATOR_REGEX = re.compile(r'^(?P<field>\w+)::(?P<operator>\w+)$')
RELATION_PROPERTY_REGEX = re.compile(r'^(?P<rel>\w+)\.(?P<rel_property>.*)$')

__all__ = [
    "Query"
]


class Query:
    """Allows to store a query parameters and run the query using a QueryRunner.
    """

    __slots__ = [
        "__entity_class",
        "__unit_of_work",
        "__query_runner",
        "__limit",
        "__query_functions",
        "__or_functions",
        "__order_by_functions",
    ]

    def __init__(self, entity_class, unit_of_work):
        self.__entity_class = entity_class
        self.__unit_of_work = unit_of_work
        self.__query_runner = QueryRunner(
            entity_class=self.__entity_class,
            unit_of_work=self.__unit_of_work
        )
        self.__limit = 0
        self.__query_functions = []
        self.__or_functions = []
        self.__order_by_functions = []

    def fetch(self) -> list:
        """Returns multiple results based on a series of parameters,
        such as a where clause, a limit, and order_by, etc...

        :return: A list of entities
        """
        return self.__query_runner.fetch(
            *self.__query_functions,
            or_function_groups=self.__or_functions,
            order_by_functions=self.__order_by_functions,
            limit=self.__limit
        )

    def fetch_one(self):
        """Returns the first result of a query based on a series of parameters,
        such as a where clause, an order_by, etc...

        :return: A single entity
        """
        return self.__query_runner.fetch_one(
            *self.__query_functions,
            or_function_groups=self.__or_functions,
        )

    def where(self, clause: dict):
        """Processes and stores the parameters for a 'where' clause.
        Each condition in the where clause is matched with a filter function.

        :param clause: The where clause to use for the query.
        :return: The query to use for chaining.
        """
        self.__query_functions.extend(self.__build_filter_composite_funcs(clause))

        return self

    def where_with_composition(self, filter_funcs: list[Callable]):
        """Adds composite functions to be used as conditional filters.

        :param filter_funcs: A list of callables matching the Pymnesia filter API.
        :return: The query to use for chaining.
        """
        self.__query_functions.extend(filter_funcs)

        return self

    def or_(self, clause: dict):
        """Processes and stores parameters for 'or' clauses.

        :param clause: The or clause to use for the query. This clause is to be considered as an 'or and', meaning that
        every parameter passed will be processed as additional filter.
        Eg:
            query().orders().where({"status":"shipped"}).or_({"status":"ready_to_ship", "is_paid": True}).fetch()
            will return all the entities that have a status "shipped" or the ones
            that have a status "ready_to_ship" AND are paid.
        :return: The query to use for chaining.
        """
        self.__or_functions.append(self.__build_filter_composite_funcs(clause))

        return self

    def __build_filter_composite_funcs(self, clause: dict) -> list[Callable]:
        """Builds partial/composite functions to use for where/or clauses.

        :param clause: The clause to build the functions from.
        :return: A list of composite callables.
        """
        filter_funcs = []
        for condition, value in clause.items():
            filter_args = {"value": value}
            matched_condition = re.match(FIELD_OPERATOR_REGEX, condition)
            if matched_condition:
                filter_func = find_filter_function(filter_name=matched_condition.group("operator"))
                filter_args["field"] = matched_condition.group("field")
            else:
                filter_func = find_filter_function(filter_name="eq")
                filter_args["field"] = condition
                matched_rel_property = re.match(RELATION_PROPERTY_REGEX, condition)
                if matched_rel_property:
                    filter_func = find_filter_function(filter_name="eq", relational=True)
                    filter_args["unit_of_work"] = self.__unit_of_work
                    filter_args["field"] = matched_rel_property.group("rel_property")
                    filter_args["relation"] = self.__entity_class.__conf__.relations[matched_rel_property.group("rel")]
            filter_funcs.append(runner(
                filter_func,
                **filter_args
            ))

        return filter_funcs

    def order_by(self, direction: str, order_by_key: str):
        """Stores parameters to use for ordering (sorting) a query result by a key.

        :param direction: Whether the result should be ordered by in an ascending or descending manner.
        :param order_by_key: The property to use for ordering.
        :return: The query to use for chaining.
        """
        self.__order_by_functions.append(runner(
            order_by,
            direction=direction,
            order_by_key=order_by_key,
        ))

        return self

    def limit(self, limit: int):
        """Adds a limit to a query.

        :param limit: The limit to set, 0 if not limit.
        :return: The query to use for chaining.
        """
        self.__limit = limit

        return self
