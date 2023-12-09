"""Provides with a Unit Of Work (storage class that will act as the originator)
"""
import time
from copy import deepcopy

from pymnesia.common.originator_interface import OriginatorInterface
from pymnesia.unit_of_work.memento.meta import unit_of_work_metaclass
from pymnesia.unit_of_work.meta import UnitOfWorkMeta
from pymnesia.query.engine.engine import QueryEngine
from pymnesia.unit_of_work.memento.base import UnitOfWorkMemento
from pymnesia.entities.registry import registry

__all__ = ["UnitOfWork"]


class UnitOfWork(OriginatorInterface, metaclass=UnitOfWorkMeta):
    """InMemory storage originator

    @DynamicAttrs"""

    def __init__(
            self,
            state: int,
    ):
        self.__state = state
        self.__replica = None
        self.__unit_of_work_memento_cls = unit_of_work_metaclass(registry_=registry)(
            "UnitOfWorkMemento",
            (UnitOfWorkMemento, ),
            {},
        )
        self.__setup()

    def __setup(self):
        self.__replica = self.__unit_of_work_memento_cls(
            state=self.__state,
        )
        for entity_cls_resolver in registry.all_configs():  # pylint: disable=unused-variable
            setattr(self, entity_cls_resolver.__tablename__, {})

    def save_entity(self, entity):
        """Saves an entity in the replica.

        :param entity: The entity to save.
        """
        self.__replica.state = time.time_ns()
        table = getattr(self.__replica, entity.__tablename__)
        table[entity.id] = entity

    def save(self) -> UnitOfWorkMemento:
        """Saves the unit of work replica's current state.
        Used by the caretaker to commit.

        :return: The memento of the saved state.
        """
        self.__state = deepcopy(self.__replica.state)  # pylint: disable=no-member
        replica_values = {}

        for entity_cls_resolver in registry.all_configs():  # pylint: disable=unused-variable
            tablename = entity_cls_resolver.__tablename__
            values = deepcopy(getattr(self.__replica, tablename))
            setattr(
                self,
                tablename,
                values
            )
            replica_values[tablename] = values

        memento = self.__unit_of_work_memento_cls(
            state=self.__state,
            **replica_values
        )

        return memento

    def query(self):
        """Returns a query engine to be used for querying the unit of work current state.

        :return: A query engine instantiated with the current unit of work state.
        """
        return QueryEngine(unit_of_work=self)
