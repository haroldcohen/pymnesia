"""Provides with unit tests to validate the query all feature.
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
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.seeding import generate_seeds


class TestQueryFetch:

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
        "seeds",
        [
            generate_seeds(1, {"id": uuid4}),
            generate_seeds(2, {"id": uuid4}),
        ],
        indirect=True,
    )
    def test_query_fetch_all_should_return_every_entity(
            self,
            entity_cls_params,
            entity_cls,
            seeds,
            seeded_entities,
            unit_of_work,
            unregister_entity_classes,
            base_query,
    ):
        result = base_query.fetch()
        assert_that(
            result,
            equal_to(seeded_entities)
        )
