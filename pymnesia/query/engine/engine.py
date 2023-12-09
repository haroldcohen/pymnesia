"""Provides with QueryEngine.
"""
from pymnesia.query.engine.meta import query_engine_metaclass
from pymnesia.entities.registry import registry  # pylint: disable=unused-import


class QueryEngine(metaclass=query_engine_metaclass(registry_=registry)):
    """
    Default QueryEngine class that uses a default global registry.

    Allows to query a unit of work tables.
    """

    def __init__(
            self,
            unit_of_work,
    ):
        self.unit_of_work = unit_of_work
