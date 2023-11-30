"""Provides with a custom iterable matcher.
"""
from typing import Any, Iterable

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher, T


class IterableContains(BaseMatcher[Any]):
    def __init__(self, item: Any):
        self._item = item

    def _matches(self, item: Iterable) -> bool:
        for value in item:
            if self._item == value:
                return True

        return False

    def describe_to(self, description: Description) -> None:
        description.append_text("Iterable to contain ")
        description.append_description_of(self._item)

    def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
        mismatch_description.append_text(f"item {self._item} was not in iterable.")


def iterable_contains(item: Any) -> Matcher[Any]:
    """
    :param item:
    :return:
    """
    return IterableContains(item)
