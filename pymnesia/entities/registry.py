"""Provides with a registry to store and use entities' configuration.
"""
from dataclasses import make_dataclass, field

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
            fields = []
            for field_name, field_type in entity_class.__annotations__.items():
                if hasattr(entity_class, field_name):
                    field_as_attr = getattr(entity_class, field_name)
                    fields.append(
                        (field_name,
                         field_type,
                         field(default=field_as_attr.default))  # pylint: disable=invalid-field-call
                    )
                else:
                    fields.append((field_name, field_type))
            entity_class = make_dataclass(
                entity_class.__name__,
                fields=fields,
            )
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
