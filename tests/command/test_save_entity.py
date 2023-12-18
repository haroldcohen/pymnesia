"""Provides with unit tests to validate entities registry related features.
"""
from uuid import UUID, uuid4
from dataclasses import asdict

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.seed import *
from tests.common_utils.fixtures.unit_of_work.expected import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.registry import unregister_entity_classes
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.seeding import generate_seeds


class TestSaveAndCommit:
    @pytest.fixture(scope="class")
    def entity_cls_params(self):
        return generate_entity_cls_params(
            class_name="SimpleEntity",
            fields_conf={
                "id": UUID,
            },
            rel_entity_classes_params=[],
        )

    @pytest.fixture(scope="class")
    def do_water_seeds(self):
        return False

    @pytest.mark.parametrize(
        "expected_seeds",
        [
            generate_seeds(1, {"id": uuid4}),
            generate_seeds(2, {"id": uuid4}),
        ],
        indirect=True,
    )
    def test_save_an_entity_and_commit_should_update_unit_of_work_with_one_or_more_entities(
            self,
            time_ns,
            mocked_time_ns,
            entity_cls,
            expected_entities,
            expected_seeds,
            seeded_entities,
            unit_of_work,
            transaction,
            expected_unit_of_work_memento,
            unregister_entity_classes,
    ):
        # Act
        for expected_entity in expected_entities:
            unit_of_work.save_entity(expected_entity)
            expected_unit_of_work_memento.state += 1
        transaction.commit()

        # Assert
        for expected_entity in expected_entities:
            retrieved_entity = getattr(unit_of_work, entity_cls.__tablename__)[expected_entity.id]
            assert_that(
                retrieved_entity,
                equal_to(expected_entity)
            )
        *_, last = transaction.history()
        assert_that(
            asdict(last),
            equal_to(asdict(expected_unit_of_work_memento))
        )
