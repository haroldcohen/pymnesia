"""Provides with unit tests to validate the query with where clause feature.
"""
from typing import Iterable, Union
from uuid import UUID, uuid4
from functools import partial

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
from tests.common_utils.fixtures.query.expressions import where_clause
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.seeding import generate_seeds


class TestQueryWithComposition:

    @pytest.fixture(scope="class")
    def entity_cls_params(self):
        return generate_entity_cls_params(
            class_name="StringEntity",
            fields_conf={
                "id": UUID,
                "str_f": str,
            },
            rel_entity_classes_params=[],
        )

    @pytest.mark.parametrize(
        "seeds, expected_seeds",
        [
            (
                    generate_seeds(2, {"id": uuid4, "str_f": "abc"}),
                    generate_seeds(1, {"id": uuid4, "str_f": "banana"}),
            ),
        ],
        indirect=True,
    )
    def test_query_and_fetch_one_with_composition_should_return_one_or_more_filtered_entities(
            self,
            seeds,
            expected_seeds,
            expected_entities,
            seeded_entities,
            unit_of_work,
            base_query,
            unregister_entity_classes,
    ):
        def banana_func(entities_: Iterable, field: str, value: Union[str, int]) -> filter:
            return filter(lambda e: getattr(e, field) == value, entities_)

        partial_banana_func = partial(
            banana_func,
            field="str_f",
            value="banana",
        )

        result = base_query.where_with_composition([partial_banana_func]).fetch()
        assert_that(
            result,
            equal_to(expected_entities)
        )
