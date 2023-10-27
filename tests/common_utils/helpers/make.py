"""Provides with dynamically constructed entity classes.
"""
from pymnesia.entities.field import Field
from pymnesia.entities.registry import PymnesiaRegistry

__all__ = ["make_entity_class"]


class GenericEntityType(type):
    """Metaclass for generic entities.
    It allows to add attributes and properties such as Fields, and to set a class name according to a config parameter.
    """

    def __new__(mcs, name, bases, attrs):
        new_attrs = {"__annotations__": {}}

        config = attrs["config"]
        name = config["name"]
        for field_name, field_conf in config["fields"].items():
            new_attrs["__annotations__"][field_name] = field_conf["type"]
            if field_conf["make_field"]:
                new_attrs[field_name] = Field(
                    default=field_conf["field"]["default"],
                )

        return super().__new__(mcs, name, bases, new_attrs)


def make_entity_class(class_name: str, table_name: str, fields: dict, registry: PymnesiaRegistry):
    """Dynamically creates entity class and registers them in a Pymnesia registry.

    :param class_name: The class name to be used
    :param table_name: The table name under which the entity should be registered
    :param fields: The configuration use to create the entity class fields
    :param registry: The registry in which the class should be registered
    :return: A entity class
    """
    class GenericEntityBase(metaclass=GenericEntityType):
        config = {
            "name": class_name,
            "fields": {}
        }

    @registry.entity(table_name=table_name)
    class GenericEntity(GenericEntityBase):
        config = {
            "name": class_name,
            "fields": fields
        }

    return GenericEntity
