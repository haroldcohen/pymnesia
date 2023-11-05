"""Provides with relation fields.
"""
from dataclasses import dataclass, field


@dataclass()
class Relation:
    reverse: str

    is_nullable: bool = field(default=True)
