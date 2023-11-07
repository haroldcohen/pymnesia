"""Provides with QueryEngine.
"""
from pymnesia.query.engine.meta import QueryEngineType


class QueryEngine(metaclass=QueryEngineType):
    """
    QueryEngine class.

    Allows to query a unit of work tables.
    """

    def __init__(
            self,
            unit_of_work
    ):
        self.unit_of_work = unit_of_work
