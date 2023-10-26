"""Provides with QueryRunner.
"""
from pymnesia.composition import composite
from pymnesia.unit_of_work.memento import UnitOfWorkMemento


class QueryRunner:

    def __init__(self, entity_class, unit_of_work: UnitOfWorkMemento):
        self.__entity_class = entity_class
        self.__unit_of_work = unit_of_work

    def __entities(self):
        """
        Returns the entities in the unit of work matching the entity class.
        :return: A list of entities.
        """
        return [value for key, value in getattr(self.__unit_of_work, self.__entity_class.config.table_name).items()]

    def __run_query_funcs(self, *query_funcs):
        """
        Runs the query functions passed when fetch methods are called.
        :param query_funcs: The query functions to run.
        :return: A list of results where filter, order by functions may have been run.
        """
        compose_query_funcs = composite(*query_funcs)

        return list(compose_query_funcs(self.__entities()))

    def fetch(self, *args, limit: int):
        """
        Returns multiple results based on a series of parameters,
        such as a where clause, a limit, and order_by, etc...
        :param args: The query functions to run.
        :param limit: The limit to use.
        :return: A list of entities
        """
        results = self.__entities()
        if len(args):
            results = self.__run_query_funcs(*args)
        if limit:
            return results[0:limit]

        return results

    def fetch_one(self, *args):
        """
        Returns the first result of a query based on a series of parameters,
        such as a where clause, an order_by, etc...
        :param args: The query functions to run.
        :return: A single entity
        """
        results = self.__entities()
        if len(args):
            results = self.__run_query_funcs(*args)

        return results[0]
