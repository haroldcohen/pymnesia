"""Provides with unit tests to validate the query with where clause feature.
"""
import random
from functools import partial
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
from tests.common_utils.fixtures.query.expressions import where_clause
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.seeding import generate_seeds
from pymnesia.core.entities.field import Field


class TestQueryWithNumericWhereClause:

    @pytest.fixture(scope="class")
    def entity_cls_params(self):
        return generate_entity_cls_params(
            class_name="NumericEntity",
            fields_conf={
                "id": UUID,
                "int_f": (int, Field(default=0)),
                "float_f": (float, Field(default=0.1)),
            },
            rel_entity_classes_params=[],
        )

    @pytest.mark.parametrize(
        "seeds, expected_seeds, where_clause",
        [
            (
                    generate_seeds(2, {"id": uuid4, "int_f": partial(random.randint, 1, 2)}),
                    generate_seeds(1, ({"id": uuid4, "int_f": 3})),
                    {"int_f": 3},
            ),
            (
                    generate_seeds(2, {"id": uuid4, "int_f": 2}) + generate_seeds(1, {"id": uuid4, "int_f": 3}),
                    generate_seeds(1, ({"id": uuid4, "int_f": 3})),
                    {"int_f": 3},
            ),
        ],
        indirect=True,
    )
    def test_query_and_fetch_one_with_a_where_eq_clause_should_return_a_single_filtered_entity(
            self,
            seeds,
            expected_seeds,
            expected_entities,
            seeded_entities,
            unit_of_work,
            base_query,
            where_clause,
            unregister_entity_classes,
    ):
        result = base_query.where(where_clause).fetch_one()
        assert_that(
            [result],
            equal_to(expected_entities)
        )

    @pytest.mark.parametrize(
        "seeds, expected_seeds, where_clause",
        [
            (
                    generate_seeds(2, {"id": uuid4, "int_f": 1}),
                    generate_seeds(3, ({"id": uuid4, "int_f": 2})),
                    {"int_f": 2},
            ),
        ],
        indirect=True,
    )
    def test_query_and_fetch_with_a_where_clause_eq_should_return_multiple_filtered_entities(
            self,
            seeds,
            expected_seeds,
            expected_entities,
            seeded_entities,
            unit_of_work,
            base_query,
            where_clause,
            unregister_entity_classes,
    ):
        result = base_query.where(where_clause).fetch()
        assert_that(
            result,
            equal_to(expected_entities)
        )

    @pytest.mark.parametrize(
        "seeds, expected_seeds, where_clause",
        [
            (
                    generate_seeds(2, {"id": uuid4, "int_f": 1}),
                    generate_seeds(3, ({"id": uuid4, "int_f": 2})),
                    {"int_f": 2},
            ),
            (
                    generate_seeds(2, {"id": uuid4, "int_f": 1}),
                    generate_seeds(1, ({"id": uuid4, "int_f": partial(random.randint, 2, 3)})),
                    {"int_f::not": 1},
            ),
            (
                    generate_seeds(2, {"id": uuid4, "int_f": 2}),
                    generate_seeds(2, ({"id": uuid4, "int_f": partial(random.randint, 3, 5)})),
                    {"int_f::gt": 2},
            ),
            (
                    generate_seeds(2, {"id": uuid4, "int_f": partial(random.randint, 3, 5)}),
                    generate_seeds(3, ({"id": uuid4, "int_f": partial(random.randint, 1, 2)})),
                    {"int_f::lt": 3},
            ),
            (
                    generate_seeds(2, {"id": uuid4, "int_f": 2}),
                    generate_seeds(1, ({"id": uuid4, "int_f": partial(random.randint, 3, 5)})),
                    {"int_f::gte": 3},
            ),
            (
                    generate_seeds(2, {"id": uuid4, "int_f": partial(random.randint, 3, 5)}),
                    generate_seeds(2, ({"id": uuid4, "int_f": partial(random.randint, 1, 2)})),
                    {"int_f::lte": 2},
            ),
            (
                    generate_seeds(2, {"id": uuid4, "int_f": partial(random.randint, 3, 5)}),
                    generate_seeds(3, ({"id": uuid4, "int_f": partial(random.randint, 7, 10)})),
                    {"int_f::in": [7, 8, 9, 10]},
            ),
            (
                    generate_seeds(2, {"id": uuid4, "float_f": 2.1}),
                    generate_seeds(1, ({"id": uuid4, "float_f": 2.2})) +
                    generate_seeds(1, ({"id": uuid4, "float_f": 2.3})),
                    {"float_f::in": [2.2, 2.3]},
            ),
        ],
        indirect=True,
    )
    def test_query_and_fetch_with_a_where_clause_should_return_one_or_more_filtered_entities(
            self,
            entity_cls_params,
            entity_cls,
            seeds,
            expected_seeds,
            expected_entities,
            seeded_entities,
            unit_of_work,
            unregister_entity_classes,
            base_query,
            where_clause,
    ):
        result = base_query.where(where_clause).fetch()
        assert_that(
            result,
            equal_to(expected_entities)
        )


class TestQueryWithStrWhereClause:

    @pytest.fixture(scope="class")
    def entity_cls_params(self):
        return generate_entity_cls_params(
            class_name="StrEntity",
            fields_conf={
                "id": UUID,
                "str_f": str,
            },
            rel_entity_classes_params=[],
        )

    @pytest.mark.parametrize(
        "seeds, expected_seeds, where_clause",
        [
            (
                    generate_seeds(2, {"id": uuid4, "str_f": "apple"}),
                    generate_seeds(1, ({"id": uuid4, "str_f": "banana"})),
                    {"str_f": "banana"},
            ),
            (
                    generate_seeds(2, {"id": uuid4, "str_f": "banana"}),
                    generate_seeds(2, ({"id": uuid4, "str_f": "apple"})),
                    {"str_f::not": "banana"},
            ),
            (
                    generate_seeds(3, {"id": uuid4, "str_f": "carrots are vegetables !"}),
                    generate_seeds(1, ({"id": uuid4, "str_f": "apples are fruits !"})) +
                    generate_seeds(1, ({"id": uuid4, "str_f": "bananas are fruits !"})),
                    {"str_f::match": r'^\w+ are fruits !$'},
            ),
        ],
        indirect=True,
    )
    def test_query_and_fetch_with_a_where_clause_should_return_one_or_more_filtered_entities(
            self,
            entity_cls_params,
            entity_cls,
            seeds,
            expected_seeds,
            expected_entities,
            seeded_entities,
            unit_of_work,
            unregister_entity_classes,
            base_query,
            where_clause,
    ):
        result = base_query.where(where_clause).fetch()
        assert_that(
            result,
            equal_to(expected_entities)
        )
