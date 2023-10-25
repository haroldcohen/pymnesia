"""Provides with a Unit Of Work (storage class that will act as the originator)
"""
import time
from copy import deepcopy

from pymnesia.common.originator_interface import OriginatorInterface
from pymnesia.query.engine import QueryEngine
from pymnesia.unit_of_work.memento import UnitOfWorkMemento
from pymnesia.registry import registry

__all__ = ["UnitOfWork"]


class UnitOfWork(OriginatorInterface):
    """InMemory storage originator

    @DynamicAttrs"""

    def __init__(
            self,
            state: int,
    ):
        self.__state = state
        self.__replica = UnitOfWorkMemento(
            state=state,
        )
        self.__setup()

    def __setup(self):
        for entity_class, config in registry.all_configs():  # pylint: disable=unused-variable
            self.__dict__[config.table_name] = {}

    def save_entity(self, entity):
        """
        Saves an entity in the replica
        :param entity: The entity to save.
        """
        self.__replica.state = time.time_ns()
        table = getattr(self.__replica, entity.config.table_name)
        table[entity.id] = entity

    def save(self) -> UnitOfWorkMemento:
        self.__state = deepcopy(self.__replica.state)
        for entity_class, config in registry.all_configs():  # pylint: disable=unused-variable
            setattr(self, config.table_name, deepcopy(getattr(self.__replica, config.table_name)))

        memento = UnitOfWorkMemento(
            state=self.__state,
        )

        for entity_class, config in registry.all_configs():
            setattr(memento, config.table_name, deepcopy(getattr(self.__replica, config.table_name)))

        return memento

    def query(self):
        """
        Returns a query engine to be used for querying the unit of work current state.

        :return: A query engine instantiated with the current unit of work state.
        """
        tables = {}
        for entity_class, config in registry.all_configs():  # pylint: disable=unused-variable
            tables[config.table_name] = deepcopy(getattr(self, config.table_name))

        return QueryEngine(
            unit_of_work=UnitOfWorkMemento(
                state=self.__state,
                **tables
            )
        )
