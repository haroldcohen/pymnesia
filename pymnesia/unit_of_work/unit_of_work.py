"""Provides with a Unit Of Work (storage class that will as the originator)
"""

__all__ = ["UnitOfWork"]

import time
from copy import deepcopy

from pymnesia.common.originator_interface import OriginatorInterface
from pymnesia.unit_of_work.memento import UnitOfWorkMemento
from pymnesia.registry import registry


class UnitOfWork(OriginatorInterface):
    """InMemory storage originator

    @DynamicAttrs"""

    def __init__(
            self,
            state: int,
    ):
        self.state = state
        self.replica = UnitOfWorkMemento(
            state=state,
        )

    def save_entity(self, entity):
        """
        Saves an entity in the replica
        :param entity: The entity to save.
        """
        self.replica.state = time.time_ns()
        table = getattr(self.replica, entity.config.table_name)
        table[entity.id] = entity

    def save(self) -> UnitOfWorkMemento:
        self.state = deepcopy(self.replica.state)
        for entity_class, config in registry.all_configs():
            setattr(self, config.table_name, deepcopy(getattr(self.replica, config.table_name)))

        memento = UnitOfWorkMemento(
            state=self.state,
        )

        for entity_class, config in registry.all_configs():
            setattr(memento, config.table_name, deepcopy(getattr(self.replica, config.table_name)))

        return memento
