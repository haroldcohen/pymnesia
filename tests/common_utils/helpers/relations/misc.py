"""Provides with miscellaneous relational test functions.
"""
import re

from tests.common_utils.helpers.relations.types import RelatedEntityClsParams
from tests.common_utils.helpers.types import FieldsConf

__all__ = ["generate_rel_entity_cls_params"]


def generate_rel_entity_cls_params(
        class_name: str,
        fields_conf: FieldsConf
) -> RelatedEntityClsParams:
    """
    :param class_name:
    :param fields_conf:
    :return:
    """
    lower_name = class_name.replace("InMemory", "")
    lower_name = re.sub(r'(?<!^)(?=[A-Z])', '_', lower_name).lower()

    return RelatedEntityClsParams(
        name=class_name,
        table_name=lower_name + "s",
        single_form=lower_name,
        fields_conf=fields_conf,
        cls_resolver=None,
    )
