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
from tests.common_utils.fixtures.query.expressions import where_clause, or_clauses
from tests.common_utils.helpers.entities.make.relations.generate import generate_rel_entity_cls_params
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.seeding import generate_seeds, generate_seed, generate_rel_seeds
from pymnesia.entities.field import Field


class TestOneToOneRelationalQueryWithWhereClause:

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
        "seeds, expected_seeds, where_clause",
        [
            (
                    generate_seeds(1, {"id": uuid4, "rels": partial(generate_rel_seeds, {
                        "related_entity": partial(generate_seed, {"id": uuid4})
                    })}),
                    generate_seeds(1, {"id": uuid4, "rels": partial(generate_rel_seeds, {
                        "related_entity": partial(generate_seed, {"id": uuid4, "int_f": 2})
                    })}),
                    {"related_entity.int_f": 2}
            ),
            (
                    generate_seeds(2, {"id": uuid4, "rels": partial(generate_rel_seeds, {
                        "related_entity": partial(generate_seed, {
                            "id": uuid4,
                            "int_f": partial(random.randint, 1, 5)
                        })
                    })}),
                    generate_seeds(3, {"id": uuid4, "rels": partial(generate_rel_seeds, {
                        "related_entity": partial(generate_seed, {
                            "id": uuid4,
                            "int_f": partial(random.randint, 6, 10)
                        })
                    })}),
                    {"related_entity.int_f::gte": 6}
            ),
        ],
        indirect=True,
    )
    def test_query_with_a_where_clause_should_return_one_or_more_entity_with_loaded_relations(
            self,
            fields_conf,
            entity_cls,
            seeds,
            seeded_entities,
            expected_seeds,
            expected_entities,
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
