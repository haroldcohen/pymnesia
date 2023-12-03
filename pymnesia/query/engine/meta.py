"""Provides with a metaclass for QueryEngine.
"""
from pymnesia.query.query import Query
from pymnesia.entities.registry import registry


class QueryEngineType(type):
    """
    Metaclass for QueryEngine.
    """

    def __new__(mcs, name, bases, attrs):
        def table_maker(entity_class_):
            def table_query_maker(self):
                return Query(entity_class=entity_class_, unit_of_work=self.unit_of_work)

            return table_query_maker

        for entity_cls_resolver in registry.all_configs():
            table = table_maker(entity_cls_resolver)
            table.__name__ = entity_cls_resolver.__tablename__
            attrs[table.__name__] = table

        return super().__new__(mcs, name, bases, attrs)