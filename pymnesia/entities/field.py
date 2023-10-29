"""Provides with Field class to configure an entity field.
"""
from dataclasses import dataclass, field
from typing import Any, Callable


class UNDEFINED:
    """Provides with a way to avoid defensive code when building fields.
    Similar to MISSING from dataclasses module.
    """


@dataclass()
class Field:
    """Provides with a class to store an entity field configuration.
    Many properties of which will later be used to create a dataclass field.
    """
    default: Any = field(default=UNDEFINED)

    default_factory: Callable = field(default=UNDEFINED)
