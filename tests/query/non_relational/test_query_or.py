"""Provides with unit tests to validate the query with where clause feature.
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
from tests.common_utils.fixtures.query.expressions import where_clause, or_clauses
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.seeding import generate_seeds
from pymnesia.entities.field import Field


class TestQueryWithWhereOrClause:

    @pytest.fixture(scope="class")
    def entity_cls_params(self):
        return generate_entity_cls_params(
            class_name="MixedEntity",
            fields_conf={
                "id": UUID,
                "int_f": (int, Field(default=0)),
                "float_f": (float, Field(default=0.1)),
                "str_f": (str, Field(default="banana")),
            },
            rel_entity_classes_params=[],
        )

    @pytest.mark.parametrize(
        "seeds, expected_seeds, where_clause, or_clauses",
        [
            (
                    generate_seeds(1, {"id": uuid4, "int_f": 50}),
                    generate_seeds(1, ({"id": uuid4, "int_f": 60})) + generate_seeds(1, ({"id": uuid4, "int_f": 70})),
                    {"int_f": 60}, [{"int_f": 70}]
            ),
            (
                    generate_seeds(1, {"id": uuid4, "int_f": 50}) + generate_seeds(1, {"id": uuid4, "int_f": 70}),
                    generate_seeds(1, ({"id": uuid4, "str_f": "apple"})) +
                    generate_seeds(1, {"id": uuid4, "int_f": 70, "float_f": 80.2}),
                    {"str_f": "apple"}, [{"int_f": 70, "float_f": 80.2}]
            ),
            (
                    generate_seeds(1, {"id": uuid4, "int_f": 50}),
                    generate_seeds(1, ({"id": uuid4, "int_f": 60})) +
                    generate_seeds(1, {"id": uuid4, "int_f": 70}) +
                    generate_seeds(1, {"id": uuid4, "float_f": 90}),
                    {"int_f": 60}, [{"int_f": 70}, {"float_f": 90}]
            ),
        ],
        indirect=True,
    )
    def test_query_and_fetch_with_a_where_or_clause_should_return_one_or_more_filtered_entities(
            self,
            seeds,
            expected_seeds,
            expected_entities,
            seeded_entities,
            unit_of_work,
            base_query,
            where_clause,
            or_clauses,
            unregister_entity_classes,
    ):
        query = base_query.where(where_clause)
        for or_clause in or_clauses:
            query.or_(or_clause)
        result = query.fetch()
        assert_that(
            result,
            equal_to(expected_entities)
        )

    @pytest.mark.parametrize(
        "seeds, expected_seeds, where_clause, or_clauses",
        [
            (
                    generate_seeds(1, {"id": uuid4, "int_f": 50}),
                    generate_seeds(1, ({"id": uuid4, "int_f": 60})),
                    {"int_f": 60}, [{"int_f": 60}]
            ),
        ],
        indirect=True,
    )
    def test_query_and_fetch_with_a_where_or_clause_should_not_return_duplicates(
            self,
            seeds,
            expected_seeds,
            expected_entities,
            seeded_entities,
            unit_of_work,
            base_query,
            where_clause,
            or_clauses,
            unregister_entity_classes,
    ):
        query = base_query.where(where_clause)
        for or_clause in or_clauses:
            query.or_(or_clause)
        result = query.fetch()
        assert_that(
            result,
            equal_to(expected_entities)
        )
