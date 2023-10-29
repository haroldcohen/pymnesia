"""Provides with registry related fixtures.
"""
import pytest

__all__ = ["registry"]

from pymnesia.entities.registry import PymnesiaRegistry


@pytest.fixture()
def registry():
    return PymnesiaRegistry()
