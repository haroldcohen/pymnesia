"""Provides with the base class for QueryEngine.
"""

__all__ = [
    "QueryEngine",
]


class QueryEngine:
    """Base class for QueryEngine.

    Allows to query a unit of work tables.

    @DynamicAttrs
    """

    def __init__(
            self,
            unit_of_work,
    ):
        self.unit_of_work = unit_of_work
