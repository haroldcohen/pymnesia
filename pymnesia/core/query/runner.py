"""Provides with QueryRunner.
"""
from pymnesia.core.composition import composite
from pymnesia.core.entities.entity import Entity


class QueryRunner:
    __slots__ = [
        "__entity_class",
        "__unit_of_work",
    ]

    def __init__(self, entity_class, unit_of_work):
        self.__entity_class = entity_class
        self.__unit_of_work = unit_of_work

    def __entities(self):
        """Returns the entities in the unit of work matching the entity class.

        :return: A list of entities.
        """
        return [value for key, value in getattr(self.__unit_of_work, self.__entity_class.__tablename__).items()]

    def __run_query_funcs(self, *query_funcs):
        """Runs the query functions passed when fetch methods are called.

        :param query_funcs: The query functions to run.
        :return: A list of results where filter, order by functions may have been run.
        """
        compose_query_funcs = composite(*query_funcs)

        return list(compose_query_funcs(self.__entities()))

    def __run_or_funcs(self, *or_func_groups):
        """Runs the query functions passed when fetch methods are called.

        :param query_funcs: The query functions to run.
        :return: A list of results where filter, order by functions may have been run.
        """
        or_results = []
        for or_functions in or_func_groups:
            compose_or_funcs = composite(*or_functions)
            or_results.extend(list(compose_or_funcs(self.__entities())))

        return or_results

    def __load_relations(self, entity: Entity):
        """Loads an entity relations from the unit of work.

        :param entity: The entity for which to load the relations.
        :return: None
        """
        for relation_name, relation in self.__entity_class.__conf__.relations.items():
            if relation.is_owner:
                relation_key_value = getattr(entity, relation.key)
                if relation_key_value is not None:
                    if relation.relation_type == "one_to_one":
                        setattr(
                            entity,
                            relation_name,
                            getattr(
                                self.__unit_of_work,
                                relation.entity_cls_resolver.__tablename__
                            )[getattr(entity, relation.key)]
                        )
                    if relation.relation_type == "one_to_many":
                        relation_keys = getattr(entity, relation.key)
                        relations = []
                        for relation_key in relation_keys:
                            relations.append(
                                getattr(
                                    self.__unit_of_work,
                                    relation.entity_cls_resolver.__tablename__
                                )[relation_key]
                            )
                        setattr(
                            entity,
                            relation_name,
                            relations
                        )

    def fetch(self, *args, or_function_groups: list, order_by_functions: list, limit: int) -> list:
        """Returns multiple results based on a series of parameters,
        such as a where clause, a limit, and order_by, etc...

        :param args: The query functions to run.
        :param or_function_groups: The or function groups to run.
        :param order_by_functions: The order by function groups to run.
        :param limit: The limit to use.
        :return: A list of entities
        """
        results = self.__entities()
        if args:
            results = self.__run_query_funcs(*args)
            [  # pylint: disable=expression-not-assigned
                results.append(r) for r in self.__run_or_funcs(*or_function_groups)
                if r not in results
            ]
        if order_by_functions:
            compose_order_by_funcs = composite(*order_by_functions)
            results = compose_order_by_funcs(results)
        if limit:
            results = results[0:limit]
        for result in results:
            self.__load_relations(result)

        return results

    def fetch_one(self, *args, or_function_groups: list, order_by_functions: list):
        """Returns the first result of a query based on a series of parameters,
        such as a where clause, an order_by, etc...

        :param args: The query functions to run.
        :param or_function_groups: The query functions to run.
        :param order_by_functions: The order by function groups to run.
        :return: A single entity
        """
        results = self.__entities()
        if args:
            results = self.__run_query_funcs(*args)
        results += self.__run_or_funcs(*or_function_groups)
        if order_by_functions:
            compose_order_by_funcs = composite(*order_by_functions)
            results = compose_order_by_funcs(results)
        result = results[0]

        self.__load_relations(entity=result)

        return result
