"""Provides with a metaclass for QueryEngine.
"""
from pymnesia.core.query.engine.base import QueryEngine
from pymnesia.core.query.query import Query
from pymnesia.core.entities.registry.interface import PymnesiaRegistryInterface

__all__ = [
    "QueryEngineType",
    "query_engine_metaclass",
]


class QueryEngineType(type):
    """
    Metaclass for QueryEngine.
    """

    _registry: PymnesiaRegistryInterface = None

    def __new__(mcs, name, bases, attrs):  # pylint: disable=unused-argument
        def table_maker(entity_class_):
            def table_query_maker(self):
                return Query(entity_class=entity_class_, unit_of_work=self.unit_of_work)

            return table_query_maker

        for entity_cls_resolver in mcs._registry.all_configs():
            table = table_maker(entity_cls_resolver)
            table.__name__ = entity_cls_resolver.__tablename__
            attrs[table.__name__] = table

        return super().__new__(mcs, name, (QueryEngine, ), attrs)


def query_engine_metaclass(registry_: PymnesiaRegistryInterface):
    return type(
        QueryEngineType.__name__,
        (QueryEngineType, ),
        {"_registry": registry_}
    )
