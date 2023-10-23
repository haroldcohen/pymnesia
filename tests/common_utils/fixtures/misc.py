"""Provides with miscellaneous fixtures.
"""
import time

import pytest

__all__ = ["mocked_time_ns", "time_ns"]


@pytest.fixture()
def time_ns() -> int:
    """Returns the current timestamp. To be used before time_ns is mocked."""
    return time.time_ns()


@pytest.fixture()
def mocked_time_ns(time_ns: int, mocker):
    """Mocks the time.time_ns() function to return the current timestamp + 1"""

    def time_ns_mocker() -> int:
        """time.time_ns() mocker."""
        return time_ns + 1

    mocker.patch(
        "time.time_ns",
        time_ns_mocker,
    )
