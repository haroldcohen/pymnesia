"""Provides with QueryEngine.
"""
from pymnesia.query.engine_meta import QueryEngineType
from pymnesia.unit_of_work.memento import UnitOfWorkMemento


class QueryEngine(metaclass=QueryEngineType):
    """
    QueryEngine class.

    Allows to query a unit of work tables.
    """

    def __init__(
            self,
            unit_of_work: UnitOfWorkMemento
    ):
        self.unit_of_work = unit_of_work
