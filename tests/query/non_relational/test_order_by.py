"""Provides with unit tests to validate the order by feature.
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
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.seeding import generate_seeds
from tests.common_utils.helpers.seeding.strings import (
    random_special_char_str,
    random_alphanum_str
)
from tests.common_utils.fixtures.query.expressions import (
    direction,
    order_by_key,
)
from pymnesia.entities.field import Field


class TestQueryOrderByNumericField:

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
        "seeds, direction, order_by_key",
        [
            (generate_seeds(2, {"id": uuid4, "int_f": partial(random.randint, 1, 2)}), "asc", "int_f"),
            (generate_seeds(5, {"id": uuid4, "int_f": partial(random.randint, 1, 10)}), "desc", "int_f"),
            (generate_seeds(5, {"id": uuid4, "float_f": random.random}), "asc", "float_f"),
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
            direction,
            order_by_key,
    ):
        result = base_query.order_by(direction, order_by_key).fetch()
        sorted_entities = sorted(seeded_entities, key=lambda e: getattr(e, order_by_key), reverse=direction == "desc")
        assert_that(
            result,
            equal_to(sorted_entities)
        )


class TestQueryOrderByStrField:

    @pytest.fixture(scope="class")
    def entity_cls_params(self):
        return generate_entity_cls_params(
            class_name="StrEntity",
            fields_conf={
                "id": UUID,
                "str_f": (str, Field(default_factory=partial(random_alphanum_str, 3))),
            },
            rel_entity_classes_params=[],
        )

    @pytest.mark.parametrize(
        "seeds, direction, order_by_key",
        [
            (generate_seeds(2, {"id": uuid4}), "asc", "str_f"),
            (generate_seeds(2, {"id": uuid4, "str_f": partial(random_special_char_str, 2)}), "desc", "str_f"),
        ],
        indirect=True,
    )
    def test_query_and_order_by_should_return_ordered_entities(
            self,
            entity_cls_params,
            entity_cls,
            seeds,
            seeded_entities,
            unit_of_work,
            unregister_entity_classes,
            base_query,
            direction,
            order_by_key,
    ):
        result = base_query.order_by(direction, order_by_key).fetch()
        sorted_entities = sorted(seeded_entities, key=lambda e: getattr(e, order_by_key), reverse=direction == "desc")
        assert_that(
            result,
            equal_to(sorted_entities)
        )
