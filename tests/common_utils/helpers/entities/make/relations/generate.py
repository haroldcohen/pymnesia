"""Provides with miscellaneous relational test functions.
"""
import re

from pymnesia.core.entities.relations import Relation
from tests.common_utils.helpers.entities.make.relations.types import RelatedEntityClsParams
from tests.common_utils.helpers.types import FieldsConf

__all__ = ["generate_rel_entity_cls_params"]


def generate_rel_entity_cls_params(
        class_name: str,
        fields_conf: FieldsConf,
        relation_type: str = "one_to_one",
        owner_rel_api: Relation = None,
) -> RelatedEntityClsParams:
    """
    :param class_name:
    :param fields_conf:
    :param relation_type:
    :param owner_rel_api:
    :return:
    """
    lower_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()

    return RelatedEntityClsParams(
        name=class_name,
        table_name=lower_name + "s",
        single_form=lower_name,
        fields_conf=fields_conf,
        cls_resolver=None,
        relation_type=relation_type,
        owner_rel_api=owner_rel_api,
    )
