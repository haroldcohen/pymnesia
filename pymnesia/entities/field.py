"""Provides with Field class to configure an entity field"""
from dataclasses import dataclass
from typing import Any


@dataclass()
class Field:
    default: Any
