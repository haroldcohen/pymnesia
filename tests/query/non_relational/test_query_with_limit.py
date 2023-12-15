"""Provides with unit tests to validate the query with a limit clause feature.
"""
from uuid import UUID, uuid4

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.entities.seed import *
from tests.common_utils.fixtures.query.query import *
from tests.common_utils.fixtures.registry import unregister_entity_classes
from tests.common_utils.fixtures.query.expressions import limit
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.seeding import generate_seeds


class TestQueryWithLimit:

    @pytest.fixture(scope="class")
    def entity_cls_params(self):
        return generate_entity_cls_params(
            class_name="SimpleEntity",
            fields_conf={
                "id": UUID,
            },
            rel_entity_classes_params=[],
        )

    @pytest.mark.parametrize(
        "seeds, expected_seeds, limit",
        [
            (generate_seeds(1, {"id": uuid4}), generate_seeds(1, {"id": uuid4}), 1),
            (generate_seeds(3, {"id": uuid4}), generate_seeds(2, {"id": uuid4}), 2),
        ],
        indirect=True,
    )
    def test_query_an_entity_table_with_a_limit_should_return_a_number_of_limited_entities(
            self,
            seeds,
            expected_seeds,
            expected_entities,
            seeded_entities,
            unit_of_work,
            base_query,
            limit,
            unregister_entity_classes,
    ):
        result = base_query.limit(limit).fetch()
        assert_that(
            result,
            equal_to(expected_entities)
        )
