"""Provides with QueryRunner.
"""
from pymnesia.unit_of_work.memento import UnitOfWorkMemento


class QueryRunner:

    def __init__(self, entity_class, unit_of_work: UnitOfWorkMemento):
        self.__entity_class = entity_class
        self.__unit_of_work = unit_of_work

    def __results(self):
        return [value for key, value in getattr(self.__unit_of_work, self.__entity_class.config.table_name).items()]

    def fetch(self, *args, limit: int):
        results = self.__results()
        for arg in args:
            results = arg(results)()
        if limit:
            return results[0:limit]
        return results

    def fetch_one(self):
        return self.__results()[0]
