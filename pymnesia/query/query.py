"""Provides with Query class.
"""
import re

from pymnesia.composition import runner
from pymnesia.query.filter.registry import FILTER_FUNCTIONS_REGISTRY
from pymnesia.query.filter.functions import *
from pymnesia.query.functions import order_by
from pymnesia.query.runner import QueryRunner
from pymnesia.unit_of_work.memento import UnitOfWorkMemento


class Query:
    """
    Allows to store a query parameters and run the query using a QueryRunner.
    """

    def __init__(self, entity_class, unit_of_work: UnitOfWorkMemento):
        self.__entity_class = entity_class
        self.__unit_of_work = unit_of_work
        self.__query_runner = QueryRunner(
            entity_class=self.__entity_class,
            unit_of_work=self.__unit_of_work
        )
        self.__limit = 0
        self.__query_functions = []

    def fetch(self):
        """
        Returns multiple results based on a series of parameters,
        such as a where clause, a limit, and order_by, etc...
        :return: A list of entities
        """
        if len(self.__query_functions):
            return self.__query_runner.fetch(
                *self.__query_functions,
                limit=self.__limit
            )
        return self.__query_runner.fetch(
            *self.__query_functions,
            limit=self.__limit
        )

    def fetch_one(self):
        """
        Returns the first result of a query based on a series of parameters,
        such as a where clause, an order_by, etc...
        :return: A single entity
        """
        if len(self.__query_functions):
            return self.__query_runner.fetch_one(
                *self.__query_functions,
            )

        return self.__query_runner.fetch_one()

    def where(self, clause: dict):
        """
        Processes and stores the parameters for a where clause.
        Each condition in the where clause is matched with a filter function.
        :param clause: The where clause to use for the query.
        :return: The query to use for chaining.
        """
        for condition, value in clause.items():
            matched_condition = re.match(r'^(?P<field>\w+)::(?P<operator>\w+)$', condition)
            if matched_condition:
                filter_func = FILTER_FUNCTIONS_REGISTRY[matched_condition.group("operator")]
                field = matched_condition.group("field")
            else:
                filter_func = FILTER_FUNCTIONS_REGISTRY["eq"]
                field = condition
            self.__query_functions.append(runner(
                filter_func,
                field=field,
                value=value,
            ))

        return self

    def order_by(self, direction: str, order_by_key: str):
        """
        Orders (sort) a query result by a key.
        :param direction: Whether the result should be ordered by in an ascending or descending way.
        :param order_by_key: The property to use for ordering.
        :return: The query to use for chaining.
        """
        self.__query_functions.append(runner(
            order_by,
            direction=direction,
            order_by_key=order_by_key,
        ))

        return self

    def limit(self, limit: int):
        """
        Adds a limit to a query.
        :param limit: The limit to set, 0 if not limit.
        :return: The query to use for chaining.
        """
        self.__limit = limit

        return self
