"""Provides with unit tests to validate the query with where clause feature.
"""
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
from tests.common_utils.fixtures.query.expressions import where_clause, or_clauses
from tests.common_utils.helpers.entities.make.relations.generate import generate_rel_entity_cls_params
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.seeding import generate_seeds, generate_seed, generate_rel_seeds
from pymnesia.core.entities.field import Field


class TestOneToOneRelationalQueryWithWhereOrClause:

    @pytest.fixture(scope="class")
    def entity_cls_params(self):
        return generate_entity_cls_params(
            class_name="EntityWithRelation",
            fields_conf={
                "id": UUID,
            },
            rel_entity_classes_params=[
                generate_rel_entity_cls_params(
                    class_name="RelatedEntity",
                    fields_conf={
                        "id": UUID,
                        "int_f": (int, Field(default=1))
                    },
                ),
            ],
        )

    @pytest.mark.parametrize(
        "seeds, expected_seeds, where_clause, or_clauses",
        [
            (
                    generate_seeds(1, {"id": uuid4, "rels": partial(generate_rel_seeds, {
                        "related_entity": partial(generate_seed, {"id": uuid4})
                    })}),
                    generate_seeds(1, {"id": uuid4, "rels": partial(generate_rel_seeds, {
                        "related_entity": partial(generate_seed, {"id": uuid4, "int_f": 2})
                    })}) +
                    generate_seeds(1, {"id": uuid4, "rels": partial(generate_rel_seeds, {
                        "related_entity": partial(generate_seed, {"id": uuid4, "int_f": 3})
                    })}),
                    {"related_entity.int_f": 2},
                    [{"related_entity.int_f": 3}]
            )
        ],
        indirect=True,
    )
    def test_query_with_a_where_or_clause_should_return_one_or_more_entity_with_loaded_relations(
            self,
            entity_cls_params,
            fields_conf,
            entity_cls,
            seeds,
            seeded_entities,
            expected_seeds,
            expected_entities,
            where_clause,
            or_clauses,
            unit_of_work,
            rel_entity_classes,
            base_query,
            unregister_entity_classes,
    ):
        query = base_query.where(where_clause)
        for or_clause in or_clauses:
            query.or_(or_clause)
        result = query.fetch()
        assert_that(
            list(result),
            equal_to(expected_entities)
        )
