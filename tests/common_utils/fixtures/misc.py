"""Provides with miscellaneous fixtures.
"""
import time

import pytest

__all__ = [
    "time_ns",
    "mocked_time_ns",
]


@pytest.fixture()
def time_ns() -> int:
    """Provides with the current timestamp. To be used before time_ns is mocked.
    This fixture is likely to change in the near future, in order to handle more than one increment.

    :return: A timestamp to be used by mocked_time_ns.
    """
    return time.time_ns()


@pytest.fixture()
def mocked_time_ns(
        time_ns: int,
        mocker,
):  # pylint: disable=redefined-outer-name
    """Provides with a time_ns mocker.
    Mocks the time.time_ns() function so that it returns the time_ns + 1.

    :param time_ns: The time_ns fixture result to be used as the base for the time_ns mock function.
    :param mocker: Pytest mocker module.
    :return: None
    """

    def time_ns_mocker() -> int:
        """time.time_ns() mocker."""
        return time_ns + 1

    mocker.patch(
        "time.time_ns",
        time_ns_mocker,
    )
