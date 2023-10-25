"""Provides with Query class.
"""
from pymnesia.query.functions.order_by import curried_order_by
from pymnesia.query.runner import QueryRunner
from pymnesia.unit_of_work.memento import UnitOfWorkMemento


class Query:

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
        return self.__query_runner.fetch(
            *self.__query_functions,
            limit=self.__limit
        )

    def fetch_one(self):
        return self.__query_runner.fetch_one()

    def order_by(self, direction: str, order_by_key: str):
        self.__query_functions.append(curried_order_by(direction=direction, order_by_key=order_by_key))
        return self

    def limit(self, limit: int):
        self.__limit = limit

        return self
