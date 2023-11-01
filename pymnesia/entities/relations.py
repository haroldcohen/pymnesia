"""Provides with relation fields.
"""
from dataclasses import dataclass


@dataclass()
class Relation:
    reverse: str
