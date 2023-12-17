"""Provides with unit tests to validate entities registry related features.
"""
from uuid import UUID

import pytest
from hamcrest import assert_that, equal_to

from pymnesia.core.entities.base import DeclarativeBase
from pymnesia.core.entities.registry.exceptions.missing_primary_key import MissingPrimaryKeyException
from pymnesia.core.entities.registry.exceptions.missing_tablename import MissingTablenameException


def test_register_entity_without_a_primary_key_should_raise_MissingPrimaryKeyException():
    with pytest.raises(MissingPrimaryKeyException) as exc:
        class EntityWithoutPrimaryKey(DeclarativeBase):
            __tablename__ = "entities"

            int_f: int

    assert_that(
        str(exc.value),
        equal_to("Entity was declared without a primary key.")
    )


def test_register_entity_without_a_tablename_should_raise_MissingTablenameException():
    with pytest.raises(MissingTablenameException) as exc:
        class EntityWithoutTableName(DeclarativeBase):
            id: UUID

    assert_that(
        str(exc.value),
        equal_to("Entity was declared without a tablename.")
    )
