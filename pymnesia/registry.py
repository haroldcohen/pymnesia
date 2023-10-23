"""Provides with a registry to store and use entities' configuration.
"""
from pymnesia.entities.config import EntityConfig


class PymnesiaRegistry:
    """Registry class that stores entity configurations.
    """

    def __init__(self):
        self._entries = {}

    def entity(self, *, table_name: str):
        """
        Adds an entity to the registry
        :param table_name: The table name to be used for storage.
        """

        def decorator(entity_class):
            config = EntityConfig(
                table_name=table_name,
            )
            self._entries[entity_class] = config
            entity_class.config = config
            return entity_class

        return decorator

    def all_configs(self):
        for config in self._entries.items():
            yield config

    def find(self, entity_class):
        return self._entries[entity_class]


registry = PymnesiaRegistry()
