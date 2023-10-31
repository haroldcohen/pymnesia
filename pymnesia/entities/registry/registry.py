"""Provides with a registry to store and use entities' configuration.
"""
from pymnesia.entities.config import EntityConfig


class PymnesiaRegistry:
    """Registry class that stores entity configurations.
    """

    def __init__(self):
        self._entries = {}

    def register(self, entity_class):
        config = EntityConfig(
            table_name=entity_class.__tablename__
        )
        entity_class.config = config
        self._entries[entity_class] = config

    def unregister(self, entity_class):
        del self._entries[entity_class]

    def all_configs(self):
        for config in self._entries.items():
            yield config

    def find(self, entity_class):
        return self._entries[entity_class]
