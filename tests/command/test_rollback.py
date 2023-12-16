"""Provides with unit tests to validate the rollback feature.
"""
from uuid import UUID, uuid4

import pytest
from hamcrest import assert_that, equal_to

from tests.common_utils.fixtures.misc import *
from tests.common_utils.fixtures.unit_of_work import *
from tests.common_utils.fixtures.entities.make import *
from tests.common_utils.fixtures.entities.expected import *
from tests.common_utils.fixtures.transaction import *
from tests.common_utils.fixtures.entities.seed import *
from tests.common_utils.fixtures.query.query import base_query
from tests.common_utils.fixtures.registry import unregister_entity_classes
from tests.common_utils.helpers.entities.make.generate import generate_entity_cls_params
from tests.common_utils.helpers.entities.make.relations.generate import generate_rel_entity_cls_params
from tests.common_utils.helpers.entities.seeding import generate_seeds


@pytest.mark.parametrize(
    "entity_cls_params, use_properties, use_properties_for_rel_entities, seeds",
    [
        (
                generate_entity_cls_params(
                    class_name="SimpleEntity",
                    fields_conf={
                        "id": UUID,
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4()}, {}, []
        ),
        (
                generate_entity_cls_params(
                    class_name="AnotherSimpleEntity",
                    fields_conf={
                        "id": UUID,
                    },
                    rel_entity_classes_params=[
                        generate_rel_entity_cls_params(
                            class_name="RelatedEntity",
                            fields_conf={"id": UUID},
                        )
                    ],
                ),
                {"id": uuid4()}, {"related_entity": {"id": uuid4()}}, []
        ),
        (
                generate_entity_cls_params(
                    class_name="YetAnotherSimpleEntity",
                    fields_conf={
                        "id": UUID,
                    },
                    rel_entity_classes_params=[],
                ),
                {"id": uuid4()}, {}, generate_seeds(1, {"id": uuid4})
        ),
    ],
    indirect=True,
)
def test_save_one_or_more_entities_and_rollback_should_restore_the_unit_of_work_to_its_previous_state(
        entity_cls_params,
        fields_conf,
        entity_cls,
        rel_entity_classes,
        use_properties,
        use_properties_for_rel_entities,
        unit_of_work,
        transaction,
        base_query,
        unregister_entity_classes,
        seeds,
        seeded_entities,
):
    # Act
    entity = entity_cls(**use_properties)
    rel_entities = []
    for rel_name, use_rel_properties in use_properties_for_rel_entities.items():
        rel_conf = entity_cls.__conf__.relations[rel_name]
        use_rel_properties[rel_conf.reverse + "_id"] = entity.id
        rel_entity = rel_conf.entity_cls_resolver(**use_rel_properties)
        rel_entities.append(rel_entity)
        unit_of_work.save_entity(rel_entity)
    unit_of_work.save_entity(entity)
    transaction.rollback()
    transaction.commit()

    # Assert
    result = base_query.where({"id": entity.id}).fetch()
    assert_that(
        result,
        equal_to([])
    )
    for rel_entity in rel_entities:
        retrieved_rel_entity = getattr(
            unit_of_work.query(),
            rel_entity.__tablename__,
        )().where({"id": rel_entity.id}).fetch()
        assert_that(
            retrieved_rel_entity,
            equal_to([])
        )
