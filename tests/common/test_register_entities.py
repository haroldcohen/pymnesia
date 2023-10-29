"""Provides with unit tests to validate entities registry related features.
"""
from hamcrest import assert_that, equal_to

from pymnesia.entities.registry import PymnesiaRegistry
from pymnesia.entities.config import EntityConfig


def test_register_orders_should_update_the_entity_registry():
    """Tests whether the registry is updated when using the registry decorator"""
    registry = PymnesiaRegistry()

    @registry.entity(table_name="orders")
    class InMemoryOrder:
        pass

    expected_config = EntityConfig(
        table_name="orders",
    )

    assert_that(
        registry.find(InMemoryOrder),
        equal_to(expected_config)
    )


def test_register_order_lines_should_update_the_entity_registry():
    """Tests whether the registry is updated when using the registry decorator"""
    registry = PymnesiaRegistry()

    @registry.entity(table_name="order_lines")
    class InMemoryOrderLine:
        pass

    expected_config = EntityConfig(
        table_name="order_lines",
    )

    assert_that(
        registry.find(entity_class=InMemoryOrderLine),
        equal_to(expected_config)
    )
