"""Provides with expressions fixtures.
"""
import pytest

__all__ = [
    "direction",
    "order_by_key",
    "where_clause",
    "or_clauses",
    "limit",
]


@pytest.fixture()
def or_clauses(request):
    if hasattr(request, "param"):
        return request.param
    return []


@pytest.fixture()
def order_by_key(request):
    return request.param


@pytest.fixture()
def direction(request):
    if hasattr(request, "param"):
        return request.param
    return "asc"


@pytest.fixture()
def where_clause(request):
    return request.param


@pytest.fixture()
def limit(request):
    if hasattr(request, "param"):
        return request.param
    return 0
